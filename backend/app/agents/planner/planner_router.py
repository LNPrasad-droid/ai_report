from fastapi import APIRouter, Depends, HTTPException
from backend.app.agents.planner.planner_models import PlannerRequest, PlannerOutput
from backend.app.agents.planner.planner_service import PlannerService
from backend.app.agents.planner.planner import RuleBasedPlanner
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_planner_service() -> PlannerService:
    # For now we return a RuleBasedPlanner wrapped by the service.
    # Later this factory can be extended to select different strategies.
    strategy = RuleBasedPlanner()
    return PlannerService(strategy)


@router.post("/plan", response_model=PlannerOutput)
async def create_plan(request: PlannerRequest, service: PlannerService = Depends(get_planner_service)) -> PlannerOutput:
    try:
        plan = await service.create_plan(request)
        return plan
    except ValueError as ve:
        logger.debug("Validation error creating plan: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as exc:
        logger.exception("Unexpected error in planner endpoint: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to generate plan")
