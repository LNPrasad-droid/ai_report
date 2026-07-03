from backend.app.agents.gis.band_mapping import get_band_name
from backend.app.agents.satellite.satellite_models import SatelliteType


def test_get_band_name_sentinel2():
    name = get_band_name(SatelliteType.sentinel2, 'RED')
    assert name == 'B4'


def test_get_band_name_landsat8():
    name = get_band_name(SatelliteType.landsat8, 'NIR')
    assert name == 'SR_B5'
