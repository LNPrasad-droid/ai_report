from pydantic import BaseModel
from typing import Any, Dict, Optional
from enum import Enum
from datetime import datetime


class AgentStatus(str, Enum):
    success = "success"
    failed = "failed"
    skipped = "skipped"


class ExecutionResult(BaseModel):
    agent_name: str
    status: AgentStatus
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    output: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
