from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class Job(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    query: Optional[str] = None
    request: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    type: Optional[str] = None
    status: JobStatus = JobStatus.queued
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    current_agent: Optional[str] = None
    logs: List[str] = []
    errors: List[str] = []
    results: Optional[Dict[str, Any]] = None
    generated_report: Optional[Dict[str, Any]] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
