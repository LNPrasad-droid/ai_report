import logging
from typing import Dict, Any
from backend.app.agents.satellite.satellite_interfaces import SatelliteProvider
from backend.app.agents.gis.band_mapping import get_band_name
from backend.app.agents.gis.spectral_indices import ndvi, ndwi, ndmi, savi, evi, ndbi
from backend.app.agents.gis.gis_exceptions import MissingBandError, RasterProcessingError

logger = logging.getLogger(__name__)


class RasterProcessor:
    def __init__(self, provider: SatelliteProvider):
        self.provider = provider

    def clip_to_aoi(self, image, aoi):
        try:
            geom = self.provider.ee.Geometry(aoi)
            return image.clip(geom)
        except Exception as exc:
            logger.exception("Failed to clip image: %s", exc)
            raise RasterProcessingError(str(exc))

    def select_bands(self, image, satellite, logical_bands: Dict[str, str]):
        # Map logical band names to dataset-specific names
        selected = []
        for logical, _ in logical_bands.items():
            band_name = get_band_name(satellite, logical)
            if not band_name:
                raise MissingBandError(f"Missing band mapping for {logical}")
            selected.append(band_name)
        return image.select(selected)

    def cloud_mask(self, image, satellite):
        # Basic cloud mask examples; actual masks depend on collection
        try:
            if satellite == 'SENTINEL_2':
                qa = image.select('QA60')
                mask = qa.eq(0)
                return image.updateMask(mask)
            # For Landsat, use pixel_qa or similar
            return image
        except Exception as exc:
            logger.exception("Cloud masking failed: %s", exc)
            raise RasterProcessingError(str(exc))

    def resample(self, image, scale: int = None):
        # Placeholder: use nearest neighbor resample if requested
        try:
            if scale:
                return image.resample('bilinear')
            return image
        except Exception as exc:
            logger.exception("Resampling failed: %s", exc)
            raise RasterProcessingError(str(exc))

    def calculate_indices(self, image, satellite, requested_indices):
        # Build index images dict
        results = {}
        # mapping logical bands
        # RED, NIR, SWIR, GREEN, BLUE
        try:
            # Use band mapping helper to infer names
            red = get_band_name(satellite, 'RED')
            nir = get_band_name(satellite, 'NIR')
            swir = get_band_name(satellite, 'SWIR')
            green = get_band_name(satellite, 'GREEN')
            blue = get_band_name(satellite, 'BLUE')
        except Exception as exc:
            raise MissingBandError(str(exc))

        for idx in requested_indices:
            if idx == 'NDVI':
                results['NDVI'] = ndvi(image, nir, red)
            elif idx == 'NDWI':
                results['NDWI'] = ndwi(image, green, nir)
            elif idx == 'NDMI':
                results['NDMI'] = ndmi(image, nir, swir)
            elif idx == 'SAVI':
                results['SAVI'] = savi(image, nir, red)
            elif idx == 'EVI':
                results['EVI'] = evi(image, nir, red, blue)
            elif idx == 'NDBI':
                results['NDBI'] = ndbi(image, swir, nir)
            else:
                logger.warning("Requested unsupported index: %s", idx)
        return results

    def compute_statistics(self, image, region):
        try:
            # Use ee reducers to compute stats. This will block when calling getInfo(); caller must run in executor.
            stat = image.reduceRegion(reducer=self.provider.ee.Reducer.mean(), geometry=self.provider.ee.Geometry(region), scale=30)
            info = stat.getInfo()
            return info
        except Exception as exc:
            logger.exception("Statistics computation failed: %s", exc)
            raise RasterProcessingError(str(exc))
