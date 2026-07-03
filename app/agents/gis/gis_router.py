from fastapi import APIRouter, HTTPException, Depends
from backend.app.agents.gis.gis_models import ProcessRequest
from backend.app.agents.gis.gis_service import GISService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_gis_service() -> GISService:
    # For now, instantiate with a Google Earth Engine provider from satellite module
    from backend.app.agents.satellite.gee_provider import GoogleEarthEngineProvider

    provider = GoogleEarthEngineProvider()
    return GISService(provider=provider)


@router.post("/process")
async def process(request: ProcessRequest, service: GISService = Depends(get_gis_service)):
    try:
        result = await service.process_job(request.job_id, [i.value for i in request.indices], request.aoi)
        return {"result": result}
    except Exception as exc:
        logger.exception("GIS processing failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
