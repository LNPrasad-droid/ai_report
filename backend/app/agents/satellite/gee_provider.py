import logging
from typing import Any, Dict, List
from backend.app.agents.satellite.satellite_interfaces import SatelliteProvider
from backend.app.agents.satellite.satellite_models import ImageMetadata
from backend.app.agents.satellite.satellite_exceptions import EarthEngineInitializationError, NoImageryFoundError, DatasetNotFoundError
from backend.app.config import settings
import datetime

logger = logging.getLogger(__name__)


class GoogleEarthEngineProvider(SatelliteProvider):
    def __init__(self, project: str = None):
        self.project = project or settings.GEE_PROJECT
        self.initialized = False
        self.ee = None

    def initialize(self) -> None:
        try:
            import ee

            self.ee = ee
            # Initialize with a specific project
            self.ee.Initialize(project=self.project)
            self.initialized = True
            logger.info("Initialized Google Earth Engine project=%s", self.project)
        except Exception as exc:
            logger.exception("Failed to initialize Earth Engine: %s", exc)
            raise EarthEngineInitializationError(str(exc))

    def _get_collection_for_satellite(self, satellite: str):
        mapping = {
            "SENTINEL_2": "COPERNICUS/S2_SR_HARMONIZED",
            "LANDSAT_8": "LANDSAT/LC08/C02/T1_L2",
            "LANDSAT_9": "LANDSAT/LC09/C02/T1_L2",
        }
        coll = mapping.get(satellite)
        if not coll:
            raise DatasetNotFoundError(f"Unsupported satellite: {satellite}")
        return coll

    def search_imagery(self, aoi: Dict[str, Any], start_date: str, end_date: str, max_cloud_cover: float, max_results: int, satellite: str) -> List[ImageMetadata]:
        if not self.initialized:
            self.initialize()

        coll_name = self._get_collection_for_satellite(satellite)
        try:
            collection = self.ee.ImageCollection(coll_name)
            # Filter by date
            collection = collection.filterDate(start_date, end_date)
            # Filter by bounds
            if isinstance(aoi, dict):
                geom = self.ee.Geometry(aoi)
                collection = collection.filterBounds(geom)
            # Cloud cover property varies; try common property names
            def cloud_filter(img):
                # Many collections use CLOUD_COVER or CLOUDY_PIXEL_PERCENTAGE
                return img

            # Limit and sort by cloud cover if available
            try:
                collection = collection.sort('CLOUD_COVER').limit(max_results)
            except Exception:
                collection = collection.limit(max_results)

            images = collection.toList(max_results)
            results = []
            for i in range(images.size().getInfo()):
                img = self.ee.Image(images.get(i))
                info = img.getInfo()
                props = info.get('properties', {})
                image_id = info.get('id') or props.get('system:index')
                date_str = props.get('DATE_ACQUIRED') or props.get('SENSING_TIME') or info.get('properties', {}).get('system:time_start')
                try:
                    if isinstance(date_str, (int, float)):
                        acquisition = datetime.datetime.utcfromtimestamp(int(date_str) / 1000)
                    else:
                        acquisition = datetime.datetime.fromisoformat(date_str) if date_str else None
                except Exception:
                    acquisition = None

                cloud = props.get('CLOUD_COVER') or props.get('CLOUDY_PIXEL_PERCENTAGE') or None
                bands = list(info.get('bands', []))
                band_names = [b.get('id') for b in bands]
                geometry = info.get('geometry')

                meta = ImageMetadata(
                    image_id=str(image_id),
                    satellite=satellite,
                    acquisition_date=acquisition,
                    cloud_percentage=float(cloud) if cloud is not None else None,
                    resolution=None,
                    bbox=None,
                    projection=None,
                    available_bands=band_names,
                    thumbnail_url=None,
                    metadata=props,
                )
                results.append(meta)

            if not results:
                raise NoImageryFoundError("No imagery found for given AOI and date range")
            logger.info("Found %d images for %s", len(results), coll_name)
            return results
        except NoImageryFoundError:
            raise
        except DatasetNotFoundError:
            raise
        except Exception as exc:
            logger.exception("Error searching imagery: %s", exc)
            raise

    def retrieve_metadata(self, image_id: str) -> Dict[str, Any]:
        if not self.initialized:
            self.initialize()
        try:
            img = self.ee.Image(image_id)
            info = img.getInfo()
            return info
        except Exception as exc:
            logger.exception("Failed to retrieve metadata for %s: %s", image_id, exc)
            raise

    def list_available_bands(self, satellite: str) -> List[str]:
        coll_name = self._get_collection_for_satellite(satellite)
        try:
            collection = self.ee.ImageCollection(coll_name)
            img = self.ee.Image(collection.first())
            info = img.getInfo()
            bands = info.get('bands', [])
            return [b.get('id') for b in bands]

    def get_image(self, image_id: str):
        if not self.initialized:
            self.initialize()
        try:
            return self.ee.Image(image_id)
        except Exception as exc:
            logger.exception("Failed to get image %s: %s", image_id, exc)
            raise
        except Exception as exc:
            logger.exception("Failed to list bands for %s: %s", satellite, exc)
            raise
