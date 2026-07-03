from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class PredictRequest(BaseModel):
    job_id: Optional[str]
    features: Dict[str, float]
    crop: str
    model_version: Optional[str] = None


class BatchPredictRequest(BaseModel):
    job_id: Optional[str]
    items: List[PredictRequest]


class PredictResponse(BaseModel):
    prediction: Any
    confidence: Optional[float]
    probability: Optional[Dict[str, float]] = None
    inference_time_seconds: float
    model_name: Optional[str]
    model_version: Optional[str]
    feature_importance: Optional[Dict[str, float]] = None


class ModelMetadata(BaseModel):
    crop: str
    model_name: str
    version: str
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    storage_path: str
