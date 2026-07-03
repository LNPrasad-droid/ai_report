from typing import Optional
from backend.app.auth.firebase import initialize_firebase, verify_id_token
from backend.app.auth.auth_repository import AuthRepository
from backend.app.auth.auth_models import AuthenticatedUser, UserCreatePayload, UserProfileUpdate
from backend.app.auth.auth_exceptions import TokenVerificationError, AuthError
from backend.app.config import settings
from datetime import datetime


class AuthService:
    def __init__(self, auth_repo: AuthRepository = None):
        self.auth_repo = auth_repo or AuthRepository()

    async def verify_token(self, token: str) -> AuthenticatedUser:
        try:
            payload = verify_id_token(token)
+        except TokenVerificationError as exc:
+            raise
         except Exception as exc:
             raise TokenVerificationError(str(exc)) from exc

        user_payload = UserCreatePayload(
            uid=payload.get("uid"),
            email=payload.get("email"),
            display_name=payload.get("name"),
            photo_url=payload.get("picture"),
            provider=payload.get("firebase", {}).get("sign_in_provider"),
            email_verified=payload.get("email_verified", False),
        )
        user = await self.auth_repo.sync_user(user_payload, role=settings.AUTH_DEFAULT_ROLE)
        await self.auth_repo.update_last_login(user.uid)
        return user

    async def get_current_user(self, uid: str) -> Optional[AuthenticatedUser]:
        return await self.auth_repo.get_user_by_uid(uid)

    async def get_profile(self, uid: str) -> Optional[AuthenticatedUser]:
        return await self.get_current_user(uid)

    async def update_profile(self, uid: str, profile_update: UserProfileUpdate) -> AuthenticatedUser:
        update_data = profile_update.model_dump(exclude_none=True)
        return await self.auth_repo.update_profile(uid, update_data)

    async def sync_user(self, payload: UserCreatePayload) -> AuthenticatedUser:
        return await self.auth_repo.sync_user(payload)
