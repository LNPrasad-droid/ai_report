import logging
from backend.app.agents.gis.gis_models import ProcessRequest, ProcessResult
from backend.app.agents.satellite.job_repository import JobRepository
from backend.app.agents.satellite.job_models import JobStatus
from backend.app.agents.gis.raster_processor import RasterProcessor
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class GISService:
    def __init__(self, provider=None, job_repo: JobRepository = None):
        self.provider = provider
        self.job_repo = job_repo or JobRepository()
        self.processor = RasterProcessor(provider)

    async def process_job(self, job_id: str, indices: list, aoi: dict):
        # Load job to find image id
        job = await self.job_repo.get_job(job_id)
        if not job:
            raise ValueError('Job not found')

        images = job.results.get('images') if job.results else None
        if not images:
            raise ValueError('No images available in job')

        image = images[0]
        image_id = image.get('image_id') or image.get('id')

        # Update job status
        await self.job_repo.update_job(job_id, {'status': JobStatus.running, 'current_agent': 'GISAgent'})

        start = datetime.utcnow()
        try:
            # Run heavy EE operations in executor
            loop = asyncio.get_running_loop()
            def work():
                img = self.provider.get_image(image_id)
                clipped = self.processor.clip_to_aoi(img, aoi)
                idxs = self.processor.calculate_indices(clipped, image.get('satellite') or 'SENTINEL_2', indices)
                # compute stats for each index (blocking)
                stats = {}
                for name, idx_img in idxs.items():
                    s = self.processor.compute_statistics(idx_img, aoi)
                    stats[name] = s
                return {'indices': list(idxs.keys()), 'stats': stats}

            result = await loop.run_in_executor(None, work)
            end = datetime.utcnow()
            await self.job_repo.update_job(job_id, {'status': JobStatus.completed, 'finished_at': end, 'results': {'gis': result}})
            return result
        except Exception as exc:
            end = datetime.utcnow()
            await self.job_repo.update_job(job_id, {'status': JobStatus.failed, 'finished_at': end, 'errors': [str(exc)]})
            logger.exception('GIS processing failed: %s', exc)
            raise
