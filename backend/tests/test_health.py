import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(monkeypatch):
    # Mock motor client and ping behavior
    class DummyAdmin:
        async def command(self, _cmd):
            return {"ok": 1}

    class DummyClient:
        admin = DummyAdmin()

    async def fake_connect():
        import backend.app.database as database

        database.client = DummyClient()

    monkeypatch.setattr("backend.app.database.connect_to_mongo", fake_connect)

    from backend.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/health")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "ok"
