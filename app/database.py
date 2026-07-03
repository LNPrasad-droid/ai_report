from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.config import settings
import logging


logger = logging.getLogger(__name__)

client: Optional[AsyncIOMotorClient] = None
db = None


async def connect_to_mongo() -> None:
    """Create a singleton Motor client and test connectivity with a ping."""
    global client, db
    if client is not None:
        return

    logger.info("Connecting to MongoDB %s", settings.MONGODB_URI)
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
        maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
    )
    db = client[settings.MONGODB_DB]

    # Basic connectivity check
    try:
        await client.admin.command("ping")
        logger.info("MongoDB ping successful")
    except Exception:
        logger.exception("Failed to ping MongoDB")
        raise


async def close_mongo_connection() -> None:
    """Close the Motor client connection.

    Motor's `close()` is synchronous but safe to call from async context.
    """
    global client
    if client is not None:
        logger.info("Closing MongoDB connection")
        client.close()
        client = None
