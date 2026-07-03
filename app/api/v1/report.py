import logging
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from backend.app.auth.dependencies import require_auth
from backend.app.auth.auth_models import AuthenticatedUser
from backend.app.agents.satellite.job_repository import JobRepository

logger = logging.getLogger(__name__)
router = APIRouter()


def _report_summary(job_doc: Dict[str, Any]) -> Dict[str, Any]:
    generated = job_doc.get("generated_report", {}) or {}
    job_id = str(job_doc.get("_id"))
    return {
        "id": job_id,
        "job_id": job_id,
        "title": generated.get("title") or job_doc.get("name") or f"Report for {job_id}",
        "summary": generated.get("executive_summary") or generated.get("summary"),
        "created_at": job_doc.get("created_at"),
        "generated_by": generated.get("generated_by") or generated.get("model"),
    }


@router.get("/")
async def list_reports(
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    current_user: AuthenticatedUser = Depends(require_auth),
    repo: JobRepository = Depends(JobRepository),
):
    collection = repo.collection
    filter: Dict[str, Any] = {"generated_report": {"$exists": True}, "user_id": current_user.uid}
    if status:
        filter["status"] = status
    cursor = collection.find(filter).sort("created_at", -1).limit(limit)
    reports = []
    async for doc in cursor:
        reports.append(_report_summary(doc))
    return reports


@router.get("/{report_id}")
async def get_report(
    report_id: str,
    current_user: AuthenticatedUser = Depends(require_auth),
    repo: JobRepository = Depends(JobRepository),
):
    job = await repo.get_job(report_id)
    if not job or job.user_id != current_user.uid or not getattr(job, "generated_report", None):
        raise HTTPException(status_code=404, detail="Report not found")
    generated = getattr(job, "generated_report") or {}
    return {
        "id": job.id,
        "job_id": job.id,
        "title": generated.get("title") or f"Report for {job.id}",
        "executive_summary": generated.get("executive_summary"),
        "technical_analysis": generated.get("technical_analysis"),
        "recommendations": generated.get("recommendations") or ["See technical analysis"],
        "confidence": generated.get("confidence") or "Medium",
        "generated_by": generated.get("model") or generated.get("generated_by"),
        "generation_time": generated.get("generation_time_seconds") or generated.get("generation_time"),
        "metadata": generated.get("metadata") or {},
        "created_at": job.created_at,
        "job": job.dict(),
    }
