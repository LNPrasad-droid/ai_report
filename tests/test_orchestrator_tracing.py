import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from backend.app.orchestrator.orchestrator import Orchestrator
from backend.app.orchestrator.execution_context import ExecutionContext
from backend.app.agents.planner.planner_models import PlannerOutput, AgentType, Intent, Priority
from backend.app.orchestrator.execution_result import ExecutionResult, AgentStatus


class FakeAgent:
    def __init__(self, name, status=AgentStatus.success, output=None):
        self.name = name
        self._status = status
        self._output = output or {"msg": f"output-{name}"}

    async def run(self, context):
        start = datetime.utcnow()
        end = datetime.utcnow()
        return ExecutionResult(agent_name=self.name, status=self._status, start_time=start, end_time=end, duration_seconds=(end - start).total_seconds(), output=self._output)


@pytest.mark.asyncio
async def test_orchestrator_records_traces(monkeypatch):
    # prepare planner output with three agents in order
    po = PlannerOutput(query="q", intent=Intent.generate_report, agents=[AgentType.RetrievalAgent, AgentType.SatelliteAgent, AgentType.GISAgent], reasoning=None, priority=Priority.medium)
    ctx = ExecutionContext(query="q", planner_output=po, job_id="job-123", request_id="req-1")

    # fake agent factory
    class AF:
        def get_agent(self, name):
            # return FakeAgent with name string representation
            return FakeAgent(str(name))

    af = AF()
    orch = Orchestrator(af)

    # monkeypatch ExecutionTraceRepository to capture calls
    calls = {"start": False, "steps": [], "finish": False}

    async def fake_start_trace(job_id, request_id=None):
        calls["start"] = True

    async def fake_record_step(job_id, order, agent_name, status, start_time, end_time, input_summary=None, output_summary=None, error=None, retry_count=0, metadata=None):
        calls["steps"].append((order, agent_name, status))

    async def fake_finish_trace(job_id):
        calls["finish"] = True

    monkeypatch.setattr('backend.app.monitoring.execution_trace.ExecutionTraceRepository.start_trace', fake_start_trace)
    monkeypatch.setattr('backend.app.monitoring.execution_trace.ExecutionTraceRepository.record_step', fake_record_step)
    monkeypatch.setattr('backend.app.monitoring.execution_trace.ExecutionTraceRepository.finish_trace', fake_finish_trace)

    results = await orch.execute_plan(ctx)

    assert calls["start"] is True
    # three steps recorded
    assert len(calls["steps"]) == 3
    # order preserved
    orders = [s[0] for s in calls["steps"]]
    assert orders == [1, 2, 3]
    # finish called
    assert calls["finish"] is True
