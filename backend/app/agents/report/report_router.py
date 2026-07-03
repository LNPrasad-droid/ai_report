from fastapi import APIRouter, Depends, HTTPException
from backend.app.agents.report.report_models import ReportRequest
from backend.app.agents.report.report_service import ReportService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_report_service() -> ReportService:
    return ReportService()


@router.post('/generate')
async def generate(request: ReportRequest, service: ReportService = Depends(get_report_service)):
    try:
        report = await service.generate_report(request.job_id, prompt_type=request.prompt_type)
        return report.dict()
    except Exception as exc:
        logger.exception('Report generation failed: %s', exc)
        raise HTTPException(status_code=500, detail=str(exc))
