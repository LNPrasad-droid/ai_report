import logging
import asyncio
from backend.app.agents.satellite.job_repository import JobRepository
from backend.app.agents.satellite.job_models import Job, JobStatus
from backend.app.agents.satellite.satellite_models import SearchRequest
from backend.app.agents.satellite.satellite_exceptions import InvalidAOIError
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, job_repo: JobRepository = None, provider=None):
        self.job_repo = job_repo or JobRepository()
        self.provider = provider

    async def create_search_job(self, request: SearchRequest, user_id: str = None, user_email: str = None, user_role: str = None) -> str:
        # Validate AOI basic
        if not request.aoi:
            raise InvalidAOIError("AOI is required")

        job = Job(
            user_id=user_id,
            user_email=user_email,
            user_role=user_role,
            query=None,
            request=request.dict(),
            status=JobStatus.queued,
            logs=["Job created"],
        )
        job_id = await self.job_repo.create_job(job)

        # Schedule background task to execute
        asyncio.create_task(self._run_search_job(job_id, request))
        logger.info("Scheduled search job %s", job_id)
        return job_id

    async def _run_search_job(self, job_id: str, request: SearchRequest) -> None:
        start = datetime.utcnow()
        await self.job_repo.update_job(job_id, {"status": JobStatus.running, "started_at": start, "current_agent": "SatelliteAgent"})
        try:
            # Execute provider search in thread executor to avoid blocking event loop
            loop = asyncio.get_running_loop()
            results = await loop.run_in_executor(
                None,
                lambda: self.provider.search_imagery(
                    aoi=request.aoi,
                    start_date=request.start_date,
                    end_date=request.end_date,
                    max_cloud_cover=request.max_cloud_cover,
                    max_results=request.max_results,
                    satellite=request.satellite.value,
                ),
            )

            # Persist results
            await self.job_repo.update_job(job_id, {"status": JobStatus.completed, "finished_at": datetime.utcnow(), "results": {"images": [r.dict() for r in results]}, "logs": ["Search completed"]})
            logger.info("Job %s completed", job_id)
        except Exception as exc:
            logger.exception("Job %s failed: %s", job_id, exc)
            await self.job_repo.update_job(job_id, {"status": JobStatus.failed, "finished_at": datetime.utcnow(), "errors": [str(exc)]})
