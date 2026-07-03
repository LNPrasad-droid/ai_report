import logging
from backend.app.orchestrator.agent_factory import AgentFactory
from backend.app.orchestrator.orchestrator import Orchestrator
from backend.app.orchestrator.execution_context import ExecutionContext
from backend.app.agents.planner.planner_service import PlannerService
from backend.app.agents.planner.planner import RuleBasedPlanner
from backend.app.agents.planner.planner_models import PlannerRequest
from backend.app.orchestrator.execution_result import ExecutionResult
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)


class OrchestratorService:
    def __init__(self, planner_service: PlannerService = None, agent_factory: AgentFactory = None) -> None:
        self.planner_service = planner_service or PlannerService(RuleBasedPlanner())
        self.agent_factory = agent_factory or AgentFactory()
        self.orchestrator = Orchestrator(self.agent_factory)

    async def run_query(self, query: str) -> dict:
        started = datetime.utcnow()
        plan = await self.planner_service.create_plan(PlannerRequest(query=query))
        context = ExecutionContext(query=query, planner_output=plan, started_at=started)
        results: List[ExecutionResult] = await self.orchestrator.execute_plan(context)
        finished = datetime.utcnow()
        total_time = (finished - started).total_seconds()
        return {
            "query": query,
            "planner_output": plan.dict(),
            "execution_trace": [r.dict() for r in results],
            "intermediate_results": context.intermediate_results,
            "errors": context.errors,
            "execution_time_seconds": total_time,
        }
