from typing import List, Optional
from backend.app.database import db
from backend.app.agents.ml.ml_models import ModelMetadata


class MLRepository:
    COLLECTION = "ml_models"

    def __init__(self):
        self.collection = db.get_collection(self.COLLECTION)

    async def register_model(self, meta: ModelMetadata) -> str:
        doc = meta.model_dump()
        await self.collection.insert_one(doc)
        return doc.get("storage_path")

    async def list_models(self, crop: Optional[str] = None) -> List[dict]:
        q = {}
        if crop:
            q["crop"] = crop
        cursor = self.collection.find(q)
        res = []
        async for d in cursor:
            res.append(d)
        return res

    async def get_model(self, crop: str, version: Optional[str] = None) -> Optional[dict]:
        q = {"crop": crop}
        if version:
            q["version"] = version
        return await self.collection.find_one(q)
