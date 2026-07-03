import pytest
from backend.app.agents.planner.planner import RuleBasedPlanner
from backend.app.agents.planner.planner_service import PlannerService
from backend.app.agents.planner.planner_models import PlannerRequest, AgentType, Intent


@pytest.mark.asyncio
async def test_rule_based_planner_analyze_area():
    planner = RuleBasedPlanner()
    service = PlannerService(planner)
    req = PlannerRequest(query="Show unhealthy cotton farms in Karnataka.")
    plan = await service.create_plan(req)
    assert plan.intent == Intent.analyze_area
    assert AgentType.SatelliteAgent in plan.agents
    assert AgentType.MLAgent in plan.agents


@pytest.mark.asyncio
async def test_rule_based_planner_explain():
    planner = RuleBasedPlanner()
    service = PlannerService(planner)
    req = PlannerRequest(query="Explain NDVI")
    plan = await service.create_plan(req)
    assert plan.intent == Intent.explain_concept
    assert plan.agents == [AgentType.RetrievalAgent, AgentType.ReportAgent]
