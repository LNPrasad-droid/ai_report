import pytest
from unittest.mock import AsyncMock
from backend.app.orchestrator.orchestrator_service import OrchestratorService
from backend.app.orchestrator.agent_factory import AgentFactory
from backend.app.orchestrator.execution_result import ExecutionResult, AgentStatus
from backend.app.agents.planner.planner_models import PlannerOutput, Intent
from backend.app.agents.planner.planner_models import AgentType
from datetime import datetime


class DummyPlannerService:
    async def create_plan(self, request):
        # return a simple PlannerOutput-like object
        return PlannerOutput(query=request.query, intent=Intent.analyze_area, agents=[AgentType.RetrievalAgent, 'SatelliteAgent', 'ReportAgent'], reasoning='test', priority='high')


class DummyAgent:
    def __init__(self, name):
        self.name = name

    async def run(self, context):
        now = datetime.utcnow()
        return ExecutionResult(agent_name=self.name, status=AgentStatus.success, start_time=now, end_time=now, duration_seconds=0.0, output={"ok": True})


@pytest.mark.asyncio
async def test_orchestrator_sequence(monkeypatch):
    planner = DummyPlannerService()
    factory = AgentFactory()
    # monkeypatch factory.get_agent to return DummyAgent instances
    monkeypatch.setattr(factory, 'get_agent', lambda name: DummyAgent(name))
    svc = OrchestratorService(planner_service=planner, agent_factory=factory)
    resp = await svc.run_query('test query')
    assert 'planner_output' in resp
    assert 'execution_trace' in resp
    assert len(resp['execution_trace']) == 3


@pytest.mark.asyncio
async def test_orchestrator_handles_agent_failure(monkeypatch):
    planner = DummyPlannerService()
    factory = AgentFactory()

    async def failing_get_agent(name):
        class FailingAgent:
            async def run(self, context):
                raise RuntimeError('agent failed')

        return FailingAgent()

    monkeypatch.setattr(factory, 'get_agent', failing_get_agent)
    svc = OrchestratorService(planner_service=planner, agent_factory=factory)
    resp = await svc.run_query('test query')
    assert len(resp['execution_trace']) == 3
    # at least one failed status present
    assert any(r.get('status') == 'failed' for r in resp['execution_trace'])
