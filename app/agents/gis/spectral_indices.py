import logging
from typing import Dict
from backend.app.agents.satellite.satellite_models import SatelliteType

logger = logging.getLogger(__name__)


def ndvi(image, nir_band: str, red_band: str):
    # (NIR - RED) / (NIR + RED)
    return image.normalizedDifference([nir_band, red_band]).rename('NDVI')


def ndwi(image, green_band: str, nir_band: str):
    # (GREEN - NIR) / (GREEN + NIR)
    return image.normalizedDifference([green_band, nir_band]).rename('NDWI')


def ndmi(image, nir_band: str, swir_band: str):
    return image.normalizedDifference([nir_band, swir_band]).rename('NDMI')


def savi(image, nir_band: str, red_band: str, L: float = 0.5):
    # SAVI = ((NIR - RED) / (NIR + RED + L)) * (1 + L)
    expr = image.expression(
        '((NIR - RED) / (NIR + RED + L)) * (1 + L)',
        {'NIR': image.select(nir_band), 'RED': image.select(red_band), 'L': L},
    )
    return expr.rename('SAVI')


def evi(image, nir_band: str, red_band: str, blue_band: str):
    # EVI = 2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)
    expr = image.expression(
        '2.5 * (NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1)',
        {'NIR': image.select(nir_band), 'RED': image.select(red_band), 'BLUE': image.select(blue_band)},
    )
    return expr.rename('EVI')


def ndbi(image, swir_band: str, nir_band: str):
    # (SWIR - NIR) / (SWIR + NIR)
    return image.normalizedDifference([swir_band, nir_band]).rename('NDBI')
