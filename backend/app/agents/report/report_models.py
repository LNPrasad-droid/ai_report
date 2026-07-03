from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class ReportRequest(BaseModel):
    job_id: str
    prompt_type: Optional[str] = 'general'


class AIReport(BaseModel):
    executive_summary: str
    technical_analysis: str
    findings: List[str]
    recommendations: List[str]
    confidence: str
    generated_by: str
    generation_time: Optional[float]
    job_id: str
    model_version: Optional[str]
    metadata: Optional[Dict[str, Any]]
