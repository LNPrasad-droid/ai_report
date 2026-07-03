from typing import Optional, Dict, Any
from backend.app.repositories.base import BaseRepository
from backend.app.models.user import UserInDB
from backend.app import database


class UserRepository(BaseRepository[UserInDB]):
    def __init__(self):
        collection = database.db.get_collection("users")
        super().__init__(collection, UserInDB)

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        doc = await self.collection.find_one({"email": email})
        if not doc:
            return None
        return self.model(**doc)

    async def upsert_by_email(self, email: str, data: Dict[str, Any]) -> UserInDB:
        await self.collection.update_one({"email": email}, {"$set": data}, upsert=True)
        doc = await self.collection.find_one({"email": email})
        return self.model(**doc)
