"""Store and retrieve execution traces for jobs."""
from typing import Optional, Dict, Any
from datetime import datetime
from backend.app.database import db


class ExecutionTraceRepository:
    COLLECTION = "execution_logs"

    @classmethod
    async def start_trace(cls, job_id: str, request_id: Optional[str] = None) -> None:
        doc = {
            "job_id": job_id,
            "request_id": request_id,
            "correlation_id": None,
            "started_at": datetime.utcnow(),
            "finished_at": None,
            "overall_status": "running",
            "steps": [],
        }
        await db[cls.COLLECTION].insert_one(doc)

    @classmethod
    async def record_step(
        cls,
        job_id: str,
        order: int,
        agent_name: str,
        status: str,
        start_time: datetime,
        end_time: datetime,
        input_summary: Optional[Dict[str, Any]] = None,
        output_summary: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        retry_count: Optional[int] = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        duration = (end_time - start_time).total_seconds()
        step = {
            "order": order,
            "agent_name": agent_name,
            "status": status,
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": duration,
            "input_summary": input_summary,
            "output_summary": output_summary,
            "error": error,
            "retry_count": retry_count,
            "metadata": metadata or {},
        }
        await db[cls.COLLECTION].update_one({"job_id": job_id}, {"$push": {"steps": step}})

    @classmethod
    async def finish_trace(cls, job_id: str) -> None:
        # compute overall status based on steps
        doc = await db[cls.COLLECTION].find_one({"job_id": job_id})
        overall = "completed"
        if doc:
            for s in doc.get("steps", []):
                if s.get("status") == "failed":
                    overall = "failed"
                    break
        await db[cls.COLLECTION].update_one({"job_id": job_id}, {"$set": {"finished_at": datetime.utcnow(), "overall_status": overall}})

    @classmethod
    async def get_trace(cls, job_id: str) -> Optional[Dict[str, Any]]:
        return await db[cls.COLLECTION].find_one({"job_id": job_id})
