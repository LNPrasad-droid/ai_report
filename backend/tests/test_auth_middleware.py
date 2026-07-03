import pytest
from unittest.mock import patch, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.auth.middleware import FirebaseAuthMiddleware
from backend.app.auth.auth_models import AuthenticatedUser
from backend.app.core.logger import setup_logging

setup_logging()

app = FastAPI()
app.add_middleware(FirebaseAuthMiddleware)

@app.get("/protected")
async def protected(request):
    user = request.state.user
    return {"uid": user.uid, "email": user.email} if user else {"error": "unauthenticated"}


@pytest.mark.asyncio
async def test_auth_middleware_valid_token(monkeypatch):
    fake_user = AuthenticatedUser(
        uid="uid-123",
        email="user@example.com",
        display_name="Test User",
        provider="google.com",
        email_verified=True,
        role="Viewer",
    )

    async def fake_verify_token(token):
        return fake_user

    monkeypatch.setattr('backend.app.auth.auth_service.AuthService.verify_token', fake_verify_token)
    client = TestClient(app)

    response = client.get("/protected", headers={"Authorization": "Bearer valid-token"})
    assert response.status_code == 200
    assert response.json() == {"uid": "uid-123", "email": "user@example.com"}


@pytest.mark.asyncio
async def test_auth_middleware_invalid_token(monkeypatch):
    async def fake_verify_token(token):
        raise Exception("invalid")

    monkeypatch.setattr('backend.app.auth.auth_service.AuthService.verify_token', fake_verify_token)
    client = TestClient(app)

    response = client.get("/protected", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
