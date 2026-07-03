import pytest
from unittest.mock import patch, MagicMock
from backend.app.auth.auth_service import AuthService
from backend.app.auth.auth_models import AuthenticatedUser, UserCreatePayload
from backend.app.auth.auth_exceptions import TokenVerificationError


class FakeAuthRepo:
    def __init__(self):
        self.users = {}

    async def sync_user(self, payload, role="Viewer"):
        user = AuthenticatedUser(
            uid=payload.uid,
            email=payload.email,
            display_name=payload.display_name,
            photo_url=payload.photo_url,
            provider=payload.provider,
            email_verified=payload.email_verified,
            role=role,
            status="active",
        )
        self.users[payload.uid] = user
        return user

    async def update_last_login(self, uid):
        pass


@pytest.mark.asyncio
async def test_verify_token_syncs_user(monkeypatch):
    payload = {
        "uid": "uid-123",
        "email": "user@example.com",
        "name": "Test User",
        "picture": "http://example.com/avatar.png",
        "firebase": {"sign_in_provider": "google.com"},
        "email_verified": True,
    }

    async def fake_verify_id_token(token):
        return payload

    monkeypatch.setattr('backend.app.auth.firebase.verify_id_token', fake_verify_id_token)
    auth_service = AuthService(auth_repo=FakeAuthRepo())

    user = await auth_service.verify_token("valid-token")
    assert user.uid == "uid-123"
    assert user.email == "user@example.com"
    assert user.display_name == "Test User"
    assert user.provider == "google.com"


@pytest.mark.asyncio
async def test_verify_token_invalid_raises(monkeypatch):
    async def fake_verify_id_token(token):
        raise Exception("invalid token")

    monkeypatch.setattr('backend.app.auth.firebase.verify_id_token', fake_verify_id_token)
    auth_service = AuthService(auth_repo=FakeAuthRepo())

    with pytest.raises(TokenVerificationError):
        await auth_service.verify_token("invalid-token")
