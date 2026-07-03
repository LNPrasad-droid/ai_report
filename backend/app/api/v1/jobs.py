import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from backend.app.agents.satellite.job_repository import JobRepository
from backend.app.agents.satellite.job_models import Job, JobStatus
from backend.app.auth.dependencies import require_auth
from backend.app.auth.auth_models import AuthenticatedUser

logger = logging.getLogger(__name__)
router = APIRouter()


def _extract_query(payload: Dict[str, Any]) -> Optional[str]:
    if not isinstance(payload, dict):
        return None
    if payload.get("query"):
        return str(payload["query"])

    messages = payload.get("messages")
    if isinstance(messages, list):
        for message in reversed(messages):
            if isinstance(message, dict) and message.get("type") == "user" and message.get("content"):
                return str(message["content"])
    return None


def _job_summary(job: Job) -> Dict[str, Any]:
    return {
        "id": job.id,
        "name": job.name,
        "type": job.type,
        "status": job.status,
        "query": job.query,
        "created_at": job.created_at,
        "duration": job.duration_seconds,
        "current_agent": job.current_agent,
    }


@router.post("/")
async def create_job(
    payload: Dict[str, Any] = Body(...),
    current_user: AuthenticatedUser = Depends(require_auth),
    repo: JobRepository = Depends(JobRepository),
):
    query = _extract_query(payload)
    title = payload.get("conversation_id") or (query[:120] if query else None) or "Conversation Job"
    job = Job(
        user_id=current_user.uid,
        user_email=current_user.email,
        user_role=current_user.role,
        query=query,
        request=payload,
        status=JobStatus.queued,
        logs=["Job created"],
        name=title,
        type=payload.get("type") or "conversation",
    )
    try:
        job_id = await repo.create_job(job)
        return {"id": job_id}
    except Exception as exc:
        logger.exception("Failed to create job: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to create job")


@router.get("/")
async def list_jobs(
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    current_user: AuthenticatedUser = Depends(require_auth),
    repo: JobRepository = Depends(JobRepository),
):
    filter: Dict[str, Any] = {"user_id": current_user.uid}
    if status:
        filter["status"] = status
    jobs = await repo.find_jobs(filter=filter, limit=limit)
    return [_job_summary(job) for job in jobs]


@router.get("/{job_id}")
async def get_job(
    job_id: str,
    current_user: AuthenticatedUser = Depends(require_auth),
    repo: JobRepository = Depends(JobRepository),
):
    job = await repo.get_job(job_id)
    if not job or job.user_id != current_user.uid:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.dict()
