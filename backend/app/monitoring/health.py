"""Health check endpoints for external dependencies."""
import asyncio
from typing import Dict, Any
from backend.app.database import client as mongo_client, db
from backend.app.providers.llm.llm_factory import get_llm_provider
from backend.app.monitoring.monitoring_models import HealthComponent, HealthStatus
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def check_mongo() -> HealthComponent:
    try:
        if mongo_client is None:
            raise RuntimeError("Mongo client not initialized")
        await mongo_client.admin.command("ping")
        return HealthComponent(name="mongodb", healthy=True, detail={"db": db.name})
    except Exception as exc:
        logger.exception("Mongo health check failed")
        return HealthComponent(name="mongodb", healthy=False, detail={"error": str(exc)})


async def check_ollama() -> HealthComponent:
    try:
        provider = get_llm_provider()
        await provider.initialize()
        models = await provider.list_models()
        return HealthComponent(name="ollama", healthy=True, detail={"models": models})
    except Exception as exc:
        logger.exception("Ollama health check failed")
        return HealthComponent(name="ollama", healthy=False, detail={"error": str(exc)})


async def check_chromadb() -> HealthComponent:
    try:
        import chromadb

        # attempt to create a client (may be memory-only)
        c = chromadb.Client()
        return HealthComponent(name="chromadb", healthy=True, detail={"info": "ok"})
    except Exception as exc:
        logger.exception("ChromaDB health check failed")
        return HealthComponent(name="chromadb", healthy=False, detail={"error": str(exc)})


async def check_gee() -> HealthComponent:
    try:
        from backend.app.agents.satellite.gee_provider import GoogleEarthEngineProvider

        provider = GoogleEarthEngineProvider()
        await provider.initialize()
        return HealthComponent(name="google_earth_engine", healthy=True, detail={"info": "initialized"})
    except Exception as exc:
        logger.exception("GEE health check failed")
        return HealthComponent(name="google_earth_engine", healthy=False, detail={"error": str(exc)})


async def perform_health_check() -> HealthStatus:
    tasks = [check_mongo(), check_ollama(), check_chromadb(), check_gee()]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    overall = all(r.healthy for r in results)
    return HealthStatus(overall=overall, checked_at=datetime.utcnow(), components=results)
