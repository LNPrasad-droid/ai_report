from fastapi import APIRouter, HTTPException
from backend.app.monitoring.health import perform_health_check
from backend.app.monitoring.metrics import MetricsCollector
from backend.app.monitoring.execution_trace import ExecutionTraceRepository
from backend.app.monitoring.monitoring_models import HealthStatus
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health() -> HealthStatus:
    try:
        status = await perform_health_check()
        return status
    except Exception as exc:
        logger.exception("Health endpoint failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/metrics")
async def metrics():
    try:
        summary = await MetricsCollector.aggregate_summary()
        return {"summary": summary}
    except Exception as exc:
        logger.exception("Metrics endpoint failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/executions/{job_id}")
async def get_execution(job_id: str):
    try:
        trace = await ExecutionTraceRepository.get_trace(job_id)
        if not trace:
            raise HTTPException(status_code=404, detail="Trace not found")
        return trace
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Execution retrieval failed")
        raise HTTPException(status_code=500, detail=str(exc))
