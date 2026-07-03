from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.orchestrator.orchestrator_service import OrchestratorService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class RunRequest(BaseModel):
    query: str


@router.post("/run")
async def run_orchestration(request: RunRequest, service: OrchestratorService = None):
    try:
        svc = service or OrchestratorService()
        resp = await svc.run_query(request.query)
        return resp
    except Exception as exc:
        logger.exception("Failed to run orchestrator: %s", exc)
        raise HTTPException(status_code=500, detail="Orchestration failed")
