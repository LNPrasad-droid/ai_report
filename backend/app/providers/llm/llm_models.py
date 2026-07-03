from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class GenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None


class GenerateResponse(BaseModel):
    text: str
    model: Optional[str] = None
    generation_time_seconds: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
