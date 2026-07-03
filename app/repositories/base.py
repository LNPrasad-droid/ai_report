from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, collection: AsyncIOMotorCollection, model: Type[T]):
        self.collection = collection
        self.model = model

    async def create(self, data: Dict[str, Any]) -> T:
        result = await self.collection.insert_one(data)
        doc = await self.collection.find_one({"_id": result.inserted_id})
        return self.model(**doc)

    async def get_by_id(self, id: Any) -> Optional[T]:
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
        doc = await self.collection.find_one({"_id": id})
        if not doc:
            return None
        return self.model(**doc)

    async def find(self, filter: Dict[str, Any], limit: int = 100) -> List[T]:
        cursor = self.collection.find(filter).limit(limit)
        results = []
        async for doc in cursor:
            results.append(self.model(**doc))
        return results

    async def update(self, id: Any, data: Dict[str, Any]) -> Optional[T]:
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
        await self.collection.update_one({"_id": id}, {"$set": data})
        return await self.get_by_id(id)

    async def delete(self, id: Any) -> bool:
        if isinstance(id, str) and ObjectId.is_valid(id):
            id = ObjectId(id)
        result = await self.collection.delete_one({"_id": id})
        return result.deleted_count == 1
