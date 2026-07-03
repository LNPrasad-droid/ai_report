from fastapi import APIRouter, HTTPException, Depends
from backend.app.agents.satellite.satellite_service import SatelliteService
from backend.app.agents.satellite.satellite_models import SearchRequest
from backend.app.agents.satellite.job_repository import JobRepository
from backend.app.auth.dependencies import require_auth
from backend.app.auth.auth_models import AuthenticatedUser
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_satellite_service() -> SatelliteService:
    return SatelliteService()


@router.post("/search")
async def search(request: SearchRequest, current_user: AuthenticatedUser = Depends(require_auth), service: SatelliteService = Depends(get_satellite_service)):
    try:
        job_id = await service.create_search_job(
            request,
            user_id=current_user.uid,
            user_email=current_user.email,
            user_role=current_user.role,
        )
        return {"job_id": job_id}
    except Exception as exc:
        logger.exception("Failed to create search job: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/jobs/{job_id}")
async def get_job(job_id: str, repo: JobRepository = Depends(JobRepository)):
    job = await repo.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.dict()


@router.post("/metadata")
async def metadata(image_id: str, service: SatelliteService = Depends(get_satellite_service)):
    try:
        meta = service.get_metadata(image_id)
        return meta
    except Exception as exc:
        logger.exception("Failed to retrieve metadata: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
