from pydantic import BaseModel, Field, root_validator
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from datetime import datetime, timedelta


class SatelliteType(str, Enum):
    sentinel2 = "SENTINEL_2"
    landsat8 = "LANDSAT_8"
    landsat9 = "LANDSAT_9"


class SearchRequest(BaseModel):
    # AOI can be GeoJSON, bbox [minx,miny,maxx,maxy], or WKT string
    aoi: Optional[Dict[str, Any]] = None
    bbox: Optional[Union[str, List[float]]] = None
    start_date: str = Field(default_factory=lambda: (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d"))
    end_date: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))
    max_cloud_cover: Optional[float] = Field(20.0, ge=0.0, le=100.0)
    satellite: SatelliteType = SatelliteType.sentinel2
    max_results: int = Field(10, ge=1, le=100)

    @root_validator(pre=True)
    def normalize_aoi(cls, values):
        aoi = values.get("aoi")
        bbox = values.get("bbox")
        if not aoi and bbox is not None:
            coords = None
            if isinstance(bbox, str):
                parts = [p.strip() for p in bbox.split(",") if p.strip()]
                if len(parts) == 4:
                    try:
                        coords = [float(p) for p in parts]
                    except ValueError:
                        raise ValueError("bbox must be four comma-separated numbers")
                else:
                    raise ValueError("bbox must contain four values")
            elif isinstance(bbox, list):
                coords = bbox
            else:
                raise ValueError("bbox must be a list or comma-separated string")

            if coords is None or len(coords) != 4:
                raise ValueError("bbox must contain exactly four numeric values")

            aoi = {
                "type": "Polygon",
                "coordinates": [
                    [
                        [coords[0], coords[1]],
                        [coords[2], coords[1]],
                        [coords[2], coords[3]],
                        [coords[0], coords[3]],
                        [coords[0], coords[1]],
                    ]
                ],
            }
            values["aoi"] = aoi

        if not values.get("start_date"):
            values["start_date"] = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not values.get("end_date"):
            values["end_date"] = datetime.utcnow().strftime("%Y-%m-%d")
        return values


class ImageMetadata(BaseModel):
    image_id: str
    satellite: str
    acquisition_date: datetime
    cloud_percentage: Optional[float]
    resolution: Optional[float]
    bbox: Optional[List[float]]
    projection: Optional[str]
    available_bands: Optional[List[str]]
    thumbnail_url: Optional[str]
    metadata: Optional[Dict[str, Any]]
