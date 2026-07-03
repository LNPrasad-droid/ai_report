from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from backend.app.agents.planner.planner_models import AgentType


class DocumentMetadata(BaseModel):
    source: Optional[str] = None
    title: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None


class RetrievedChunk(BaseModel):
    id: str
    text: str
    metadata: Optional[DocumentMetadata] = None
    score: float


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(5, ge=1, le=100)


class SearchResponse(BaseModel):
    query: str
    results: List[RetrievedChunk]
