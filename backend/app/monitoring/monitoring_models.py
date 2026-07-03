from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime


class HealthComponent(BaseModel):
    name: str
    healthy: bool
    detail: Optional[Dict[str, Any]] = None


class HealthStatus(BaseModel):
    overall: bool
    checked_at: datetime = Field(default_factory=datetime.utcnow)
    components: List[HealthComponent]


class MetricSample(BaseModel):
    agent_name: Optional[str]
    metric_type: str
    value: Any
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ExecutionStep(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    result: Optional[Any]
    error: Optional[str]


class ExecutionTrace(BaseModel):
    job_id: str
    request_id: Optional[str]
    started_at: datetime
    finished_at: Optional[datetime]
    steps: List[ExecutionStep] = []
