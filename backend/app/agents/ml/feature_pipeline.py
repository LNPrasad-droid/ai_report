from typing import Dict, Any
import math


def safe_div(a, b):
    try:
        return a / b
    except Exception:
        return None


def compute_indices(gis_results: Dict[str, Any]) -> Dict[str, float]:
    """Compute a standard set of features from GIS outputs.

    Expected gis_results is a dict that may include band values or precomputed indices.
    """
    features = {}

    # If provided directly, use supplied indices
    for idx in ["ndvi", "ndwi", "ndmi", "savi", "evi", "ndre", "lst", "albedo"]:
        v = gis_results.get(idx)
        if v is not None:
            features[idx] = float(v)

    # If bands provided, compute common indices
    red = gis_results.get("red")
    nir = gis_results.get("nir")
    swir = gis_results.get("swir")
    green = gis_results.get("green")

    if red is not None and nir is not None:
        ndvi = safe_div((nir - red), (nir + red))
        if ndvi is not None:
            features.setdefault("ndvi", ndvi)

    if green is not None and nir is not None:
        ndwi = safe_div((green - nir), (green + nir))
        if ndwi is not None:
            features.setdefault("ndwi", ndwi)

    if nir is not None and swir is not None:
        ndmi = safe_div((nir - swir), (nir + swir))
        if ndmi is not None:
            features.setdefault("ndmi", ndmi)

    # Elevation-derived features
    elevation = gis_results.get("elevation")
    if elevation is not None:
        features["elevation"] = float(elevation)

    slope = gis_results.get("slope")
    if slope is not None:
        features["slope"] = float(slope)

    aspect = gis_results.get("aspect")
    if aspect is not None:
        features["aspect"] = float(aspect)

    # Climate features
    for key in ["rainfall", "temperature", "humidity"]:
        v = gis_results.get(key)
        if v is not None:
            features[key] = float(v)

    return features
