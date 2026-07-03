from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.app.agents.planner.planner_models import PlannerOutput


class ExecutionContext(BaseModel):
    query: str
    planner_output: PlannerOutput
    intermediate_results: Dict[str, Any] = {}
    execution_history: List[Dict[str, Any]] = []
    errors: List[str] = []
    metadata: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    # Optional correlation identifiers propagated from middleware
    job_id: Optional[str] = None
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
