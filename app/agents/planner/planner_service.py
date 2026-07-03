import logging
from typing import Optional
from backend.app.agents.planner.planner_interfaces import PlannerStrategy
from backend.app.agents.planner.planner_models import PlannerRequest, PlannerOutput

logger = logging.getLogger(__name__)


class PlannerService:
    """Service layer for planner operations.

    Accepts a PlannerStrategy implementation, enabling DI and the
    Strategy pattern so planners can be swapped without changing callers.
    """

    def __init__(self, strategy: PlannerStrategy) -> None:
        self.strategy = strategy

    async def create_plan(self, request: PlannerRequest) -> PlannerOutput:
        logger.info("PlannerService.create_plan called")
        # Basic validation
        if not request or not request.query:
            logger.warning("Invalid planner request: %s", request)
            raise ValueError("Invalid planner request: 'query' is required")

        plan = await self.strategy.generate_plan(request)
        logger.info("Plan created for query: %s", request.query)
        return plan
