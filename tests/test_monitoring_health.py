import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_health_checks(monkeypatch):
    # Patch Mongo, Ollama, Chroma, GEE checks to return healthy components
    from backend.app.monitoring.health import check_mongo, check_ollama, check_chromadb, check_gee, perform_health_check

    monkeypatch.setattr('backend.app.monitoring.health.check_mongo', AsyncMock(return_value=AsyncMock(healthy=True, name='mongodb')))
    monkeypatch.setattr('backend.app.monitoring.health.check_ollama', AsyncMock(return_value=AsyncMock(healthy=True, name='ollama')))
    monkeypatch.setattr('backend.app.monitoring.health.check_chromadb', AsyncMock(return_value=AsyncMock(healthy=True, name='chromadb')))
    monkeypatch.setattr('backend.app.monitoring.health.check_gee', AsyncMock(return_value=AsyncMock(healthy=True, name='gee')))

    status = await perform_health_check()
    assert status.overall is True
