from typing import Optional, Dict, Any
from backend.app import database
from backend.app.agents.satellite.job_models import Job, JobStatus
from bson import ObjectId
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class JobRepository:
    def __init__(self):
        self.collection = database.db.get_collection("analysis_jobs")

    async def create_job(self, job: Job) -> str:
        doc = job.dict()
        doc.setdefault('created_at', datetime.utcnow())
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)

    async def get_job(self, job_id: str) -> Optional[Job]:
        if not ObjectId.is_valid(job_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(job_id)})
        if not doc:
            return None
        # convert ObjectId to string
        doc['id'] = str(doc.get('_id'))
        return Job(**doc)

    async def find_jobs(self, filter: Dict[str, Any], limit: int = 100) -> list[Job]:
        if filter is None:
            filter = {}
        cursor = self.collection.find(filter).limit(limit)
        jobs = []
        async for doc in cursor:
            doc['id'] = str(doc.get('_id'))
            jobs.append(Job(**doc))
        return jobs

    async def update_job(self, job_id: str, patch: Dict[str, Any]) -> bool:
        if not ObjectId.is_valid(job_id):
            return False
        patch_doc = {k: v for k, v in patch.items()}
        if 'finished_at' in patch_doc and 'started_at' in patch_doc:
            try:
                st = patch_doc.get('started_at')
                fin = patch_doc.get('finished_at')
                patch_doc['duration_seconds'] = (fin - st).total_seconds()
            except Exception:
                pass
        res = await self.collection.update_one({"_id": ObjectId(job_id)}, {"$set": patch_doc})
        return res.modified_count == 1
