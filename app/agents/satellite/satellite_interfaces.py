from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from backend.app.agents.satellite.satellite_models import ImageMetadata


class SatelliteProvider(ABC):
    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def search_imagery(self, aoi: Dict[str, Any], start_date: str, end_date: str, max_cloud_cover: float, max_results: int, satellite: str) -> List[ImageMetadata]:
        raise NotImplementedError

    @abstractmethod
    def retrieve_metadata(self, image_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list_available_bands(self, satellite: str) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_image(self, image_id: str):
        """Return a provider-specific image handle (e.g., ee.Image)."""
        raise NotImplementedError
