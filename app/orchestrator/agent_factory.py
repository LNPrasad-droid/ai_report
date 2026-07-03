from typing import Dict
import logging
from backend.app.orchestrator.agent_interface import AgentInterface
from backend.app.agents.retrieval.retrieval_service import RetrievalService
from backend.app.agents.planner.planner import RuleBasedPlanner
from backend.app.agents.planner.planner_service import PlannerService
from backend.app.agents.planner.planner_models import AgentType
from backend.app.orchestrator import execution_result

logger = logging.getLogger(__name__)


class PlaceholderAgent(AgentInterface):
    def __init__(self, name: str) -> None:
        self.name = name

    async def run(self, context):
        # Placeholder that returns a skipped result
        from datetime import datetime
        start = datetime.utcnow()
        end = datetime.utcnow()
        return execution_result.ExecutionResult(
            agent_name=self.name,
            status=execution_result.AgentStatus.skipped,
            start_time=start,
            end_time=end,
            duration_seconds=(end - start).total_seconds(),
            output={"message": "placeholder"},
        )


class AgentFactory:
    """Factory for creating agent instances by name.

    The orchestrator only depends on AgentInterface instances produced
    by this factory, so concrete implementations can be swapped.
    """

    def __init__(self, dependencies: Dict = None) -> None:
        self.dependencies = dependencies or {}

    def get_agent(self, name: str) -> AgentInterface:
        logger.debug("Resolving agent: %s", name)
        if name == AgentType.RetrievalAgent:
            # Return a RetrievalService wrapper implementing AgentInterface
            # We'll wrap the service with an adapter
            return RetrievalAgentAdapter(self.dependencies.get("retrieval_service") or RetrievalService())

        # For non-implemented agents, return placeholders
        return PlaceholderAgent(name)


class RetrievalAgentAdapter(AgentInterface):
    def __init__(self, service: RetrievalService) -> None:
        self.service = service
        self.name = "RetrievalAgent"

    async def run(self, context):
        # Use context.query to perform a search and attach results to context
        from datetime import datetime
        start = datetime.utcnow()
        try:
            # Simple search; top_k can be chosen from metadata or default
            top_k = 5
            from backend.app.agents.retrieval.retrieval_models import SearchRequest

            req = SearchRequest(query=context.query, top_k=top_k)
            results = await self.service.search(req)
            end = datetime.utcnow()
            return execution_result.ExecutionResult(
                agent_name=self.name,
                status=execution_result.AgentStatus.success,
                start_time=start,
                end_time=end,
                duration_seconds=(end - start).total_seconds(),
                output={"results": [r.dict() for r in results.results]},
            )
        except Exception as exc:
            end = datetime.utcnow()
            return execution_result.ExecutionResult(
                agent_name=self.name,
                status=execution_result.AgentStatus.failed,
                start_time=start,
                end_time=end,
                duration_seconds=(end - start).total_seconds(),
                output=None,
                error=str(exc),
            )
