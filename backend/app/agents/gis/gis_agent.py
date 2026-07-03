import logging
from backend.app.orchestrator.agent_interface import AgentInterface
from backend.app.orchestrator.execution_context import ExecutionContext
from backend.app.orchestrator.execution_result import ExecutionResult, AgentStatus
from backend.app.agents.gis.raster_processor import RasterProcessor
from backend.app.agents.satellite.job_repository import JobRepository
from datetime import datetime

logger = logging.getLogger(__name__)


class GISAgent(AgentInterface):
    def __init__(self, provider, job_repo: JobRepository = None):
        self.provider = provider
        self.job_repo = job_repo or JobRepository()
        self.processor = RasterProcessor(provider)
        self.name = 'GISAgent'

    async def run(self, context: ExecutionContext) -> ExecutionResult:
        start = datetime.utcnow()
        try:
            # Expecting context to contain a SatelliteAgent output or job reference
            sat_output = context.intermediate_results.get('SatelliteAgent') or context.intermediate_results.get('RetrievalAgent')
            if not sat_output:
                raise ValueError('No satellite output found in context')

            # Pick first image
            images = sat_output.get('results') if isinstance(sat_output, dict) else sat_output
            if not images:
                raise ValueError('No images available for processing')
            first = images[0]
            image_id = first.get('image_id') or first.get('id') or first.get('imageId')
            aoi = context.metadata or context.planner_output

            # Retrieve ee.Image via provider
            img = self.provider.get_image(image_id)

            # Clip
            clipped = self.processor.clip_to_aoi(img, aoi)

            # Compute default indices (for demo we'll compute NDVI)
            indices = self.processor.calculate_indices(clipped, first.get('satellite') or 'SENTINEL_2', ['NDVI'])

            end = datetime.utcnow()
            duration = (end - start).total_seconds()
            output = {
                'image_id': image_id,
                'indices': {k: 'ee.Image' for k in indices.keys()},
            }
            return ExecutionResult(agent_name=self.name, status=AgentStatus.success, start_time=start, end_time=end, duration_seconds=duration, output=output)
        except Exception as exc:
            end = datetime.utcnow()
            duration = (end - start).total_seconds()
            logger.exception('GISAgent failed: %s', exc)
            return ExecutionResult(agent_name=self.name, status=AgentStatus.failed, start_time=start, end_time=end, duration_seconds=duration, output=None, error=str(exc))
