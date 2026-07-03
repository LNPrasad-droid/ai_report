from fastapi import APIRouter
from backend.app.schemas.health import HealthResponse
from backend.app import database
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint. Verifies application and database connectivity."""
    db_status = "unknown"
    status = "ok"
    try:
        if database.client is None:
            # Attempt to connect lazily if startup didn't run
            await database.connect_to_mongo()
        await database.client.admin.command("ping")
        db_status = "ok"
    except Exception as exc:  # pragma: no cover - returns error state
        logger.exception("Health check failed: %s", exc)
        status = "fail"
        db_status = str(exc)

    return HealthResponse(status=status, db_status=db_status)
