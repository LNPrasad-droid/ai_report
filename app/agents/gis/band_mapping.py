from typing import Dict
from backend.app.agents.satellite.satellite_models import SatelliteType


DEFAULT_BAND_MAP: Dict[SatelliteType, Dict[str, str]] = {
    SatelliteType.sentinel2: {
        "RED": "B4",
        "NIR": "B8",
        "SWIR": "B11",
        "GREEN": "B3",
        "BLUE": "B2",
    },
    SatelliteType.landsat8: {
        "RED": "SR_B4",
        "NIR": "SR_B5",
        "SWIR": "SR_B6",
        "GREEN": "SR_B3",
        "BLUE": "SR_B2",
    },
    SatelliteType.landsat9: {
        "RED": "SR_B4",
        "NIR": "SR_B5",
        "SWIR": "SR_B6",
        "GREEN": "SR_B3",
        "BLUE": "SR_B2",
    },
}


def get_band_name(satellite: SatelliteType, logical_band: str) -> str:
    mapping = DEFAULT_BAND_MAP.get(satellite)
    if not mapping:
        raise ValueError(f"Unsupported satellite for band mapping: {satellite}")
    name = mapping.get(logical_band.upper())
    if not name:
        raise ValueError(f"Logical band {logical_band} not found for satellite {satellite}")
    return name
