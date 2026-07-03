import logging
from typing import List
from datetime import datetime
from backend.app.orchestrator.agent_interface import AgentInterface
from backend.app.orchestrator.execution_context import ExecutionContext
from backend.app.orchestrator.execution_result import ExecutionResult, AgentStatus
from backend.app.monitoring.execution_trace import ExecutionTraceRepository
from backend.app.monitoring.performance import get_memory_usage_bytes
from backend.app.monitoring.logger import get_logger

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, agent_factory) -> None:
        self.agent_factory = agent_factory
        self.logger = get_logger("Orchestrator")

    async def execute_plan(self, context: ExecutionContext) -> List[ExecutionResult]:
        results: List[ExecutionResult] = []
        context.started_at = datetime.utcnow()
        # Start execution trace if job_id provided
        job_id = context.job_id or (context.metadata or {}).get("job_id")
        request_id = context.request_id or (context.metadata or {}).get("request_id")
        if job_id:
            await ExecutionTraceRepository.start_trace(job_id=job_id, request_id=request_id)
        for agent_name in context.planner_output.agents:
            logger.info("Executing agent: %s", agent_name)
            agent: AgentInterface = self.agent_factory.get_agent(agent_name)
            start = datetime.utcnow()
            mem_before = get_memory_usage_bytes()
            try:
                result = await agent.run(context)
                end = datetime.utcnow()
                mem_after = get_memory_usage_bytes()
                duration = (end - start).total_seconds()

                # Merge outputs into context intermediate_results
                if result and result.output:
                    context.intermediate_results[agent_name] = result.output

                # build summaries
                input_summary = None
                # try to get prior output as input summary
                if agent_name != list(context.planner_output.agents)[0]:
                    # input is previous agent's output
                    input_summary = context.intermediate_results.get(agent_name)

                output_summary = result.output if result and result.output else None

                # record step in trace
                if job_id:
                    order = len(context.execution_history) + 1
                    await ExecutionTraceRepository.record_step(
                        job_id=job_id,
                        order=order,
                        agent_name=agent_name,
                        status=result.status.name if hasattr(result.status, 'name') else str(result.status),
                        start_time=start,
                        end_time=end,
                        input_summary=input_summary,
                        output_summary=output_summary,
                        error=result.error if hasattr(result, 'error') else None,
                        retry_count=getattr(result, 'retry_count', 0),
                        metadata=result.metadata if hasattr(result, 'metadata') else {},
                    )

                context.execution_history.append({"agent": agent_name, "status": result.status, "metadata": result.metadata})
                results.append(result)
                self.logger.info("Agent %s completed", agent_name, extra={"job_id": job_id, "duration_seconds": duration})
            except Exception as exc:
                end = datetime.utcnow()
                duration = (end - start).total_seconds()
                err_result = ExecutionResult(
                    agent_name=agent_name,
                    status=AgentStatus.failed,
                    start_time=start,
                    end_time=end,
                    duration_seconds=duration,
                    output=None,
                    error=str(exc),
                )
                results.append(err_result)
                context.errors.append(str(exc))
                context.execution_history.append({"agent": agent_name, "status": AgentStatus.failed, "error": str(exc)})
                self.logger.exception("Agent %s failed: %s", agent_name, exc)
                if job_id:
                    order = len(context.execution_history)
                    await ExecutionTraceRepository.record_step(
                        job_id=job_id,
                        order=order,
                        agent_name=agent_name,
                        status='failed',
                        start_time=start,
                        end_time=end,
                        input_summary=None,
                        output_summary=None,
                        error=str(exc),
                    )
                # Continue to next agent (graceful degradation)
        context.finished_at = datetime.utcnow()
        # finish trace
        if job_id:
            await ExecutionTraceRepository.finish_trace(job_id)
        return results
