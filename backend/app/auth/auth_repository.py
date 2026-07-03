from typing import Optional, Dict, Any
from datetime import datetime
from backend.app.database import db
from backend.app.auth.auth_models import AuthenticatedUser, UserCreatePayload
from backend.app.auth.auth_exceptions import AuthError


class AuthRepository:
    COLLECTION = "users"

    def __init__(self):
        self.collection = db.get_collection(self.COLLECTION)

    async def create_user(self, payload: UserCreatePayload, role: str = "Viewer") -> AuthenticatedUser:
        now = datetime.utcnow()
        doc = {
            "uid": payload.uid,
            "email": payload.email,
            "display_name": payload.display_name,
            "photo_url": payload.photo_url,
            "provider": payload.provider,
            "email_verified": payload.email_verified,
            "role": role,
            "status": "active",
            "created_at": now,
            "updated_at": now,
            "last_login": now,
        }
        await self.collection.update_one({"uid": payload.uid}, {"$set": doc}, upsert=True)
        return AuthenticatedUser(**doc)

    async def get_user_by_uid(self, uid: str) -> Optional[AuthenticatedUser]:
        doc = await self.collection.find_one({"uid": uid})
        if not doc:
            return None
        return AuthenticatedUser(**doc)

    async def get_user_by_email(self, email: str) -> Optional[AuthenticatedUser]:
        doc = await self.collection.find_one({"email": email})
        if not doc:
            return None
        return AuthenticatedUser(**doc)

    async def update_last_login(self, uid: str) -> None:
        await self.collection.update_one({"uid": uid}, {"$set": {"last_login": datetime.utcnow()}})

    async def update_profile(self, uid: str, profile_data: Dict[str, Any]) -> Optional[AuthenticatedUser]:
        profile_data["updated_at"] = datetime.utcnow()
        await self.collection.update_one({"uid": uid}, {"$set": profile_data})
        return await self.get_user_by_uid(uid)

    async def sync_user(self, payload: UserCreatePayload, role: str = "Viewer") -> AuthenticatedUser:
        user = await self.get_user_by_uid(payload.uid)
        if not user:
            return await self.create_user(payload, role=role)

        update_data = {
            "display_name": payload.display_name,
            "photo_url": payload.photo_url,
            "provider": payload.provider,
            "email_verified": payload.email_verified,
            "updated_at": datetime.utcnow(),
        }
        await self.collection.update_one({"uid": payload.uid}, {"$set": update_data})
        return await self.get_user_by_uid(payload.uid)
