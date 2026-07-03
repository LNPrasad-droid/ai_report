import logging
import time
from backend.app.providers.llm.llm_factory import get_llm_provider
from backend.app.providers.llm.llm_models import GenerateRequest
from backend.app.agents.report.report_builder import ReportBuilder
from backend.app.agents.report.report_models import AIReport
from backend.app.agents.satellite.job_repository import JobRepository
from backend.app.agents.satellite.job_models import JobStatus
from backend.app.agents.report.report_exceptions import ReportGenerationError

logger = logging.getLogger(__name__)


class ReportService:
    def __init__(self, provider=None, job_repo: JobRepository = None, builder: ReportBuilder = None):
        self.provider = provider or get_llm_provider()
        self.job_repo = job_repo or JobRepository()
        self.builder = builder or ReportBuilder()

    async def generate_report(self, job_id: str, prompt_type: str = 'general') -> AIReport:
        # Load job
        job = await self.job_repo.get_job(job_id)
        if not job:
            raise ReportGenerationError('Job not found')

        # Build inputs
        inputs = {
            'planner': job.request.get('planner') if job.request else None,
            'docs': job.results.get('images') if job.results else None,
            'satellite': job.results.get('images')[0] if job.results and job.results.get('images') else None,
            'gis': job.results.get('gis') if job.results else None,
            'ml': job.results.get('ml') if job.results else None,
            'trace': job.execution_history if hasattr(job, 'execution_history') else None,
        }

        prompt = self.builder.build_prompt(prompt_type, inputs)

        # update job current agent
        await self.job_repo.update_job(job_id, {'current_agent': 'ReportAgent'})

        gen_req = GenerateRequest(prompt=prompt)
        t0 = time.time()
        resp = await self.provider.generate(gen_req)
        elapsed = time.time() - t0

        # Persist report into job
        report_doc = {
            'executive_summary': resp.text[:1000],
            'model': resp.model,
            'full_text': resp.text,
            'generation_time_seconds': resp.generation_time_seconds or elapsed,
        }
        await self.job_repo.update_job(job_id, {'generation_time_seconds': elapsed, 'generated_report': report_doc, 'status': JobStatus.completed})

        # Parse minimal structured output (assume resp.text is JSON-like)
        return AIReport(
            executive_summary=resp.text[:200],
            technical_analysis=resp.text[:500],
            findings=["See executive_summary"],
            recommendations=["See technical_analysis"],
            confidence='Medium',
            generated_by=resp.model or '',
            generation_time=resp.generation_time_seconds or elapsed,
            job_id=job_id,
            model_version=resp.model,
            metadata=resp.metadata,
        )
