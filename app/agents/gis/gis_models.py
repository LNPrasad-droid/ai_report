from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class IndexName(str, Enum):
    NDVI = "NDVI"
    NDWI = "NDWI"
    NDMI = "NDMI"
    SAVI = "SAVI"
    EVI = "EVI"
    NDBI = "NDBI"


class ProcessRequest(BaseModel):
    job_id: str
    indices: List[IndexName]
    aoi: Dict[str, Any]


class BandStats(BaseModel):
    min: float
    max: float
    mean: float
    median: float
    stddev: float
    histogram: Optional[List[int]] = None


class ProcessResult(BaseModel):
    image_id: str
    indices: Dict[str, Dict[str, Any]]
    band_metadata: Dict[str, Any]
    stats: Dict[str, BandStats]
    execution_time_seconds: float
