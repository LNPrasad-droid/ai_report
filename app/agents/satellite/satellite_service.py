import logging
from backend.app.agents.satellite.satellite_interfaces import SatelliteProvider
from backend.app.agents.satellite.task_manager import TaskManager
from backend.app.agents.satellite.job_repository import JobRepository
from backend.app.agents.satellite.satellite_models import SearchRequest
from backend.app.agents.satellite.gee_provider import GoogleEarthEngineProvider

logger = logging.getLogger(__name__)


class SatelliteService:
    def __init__(self, provider: SatelliteProvider = None, job_repo: JobRepository = None):
        self.provider = provider or GoogleEarthEngineProvider()
        self.job_repo = job_repo or JobRepository()
        self.task_manager = TaskManager(job_repo=self.job_repo, provider=self.provider)

    async def create_search_job(self, request: SearchRequest, user_id: str = None, user_email: str = None, user_role: str = None) -> str:
        return await self.task_manager.create_search_job(request, user_id=user_id, user_email=user_email, user_role=user_role)

    def get_metadata(self, image_id: str):
        return self.provider.retrieve_metadata(image_id)
