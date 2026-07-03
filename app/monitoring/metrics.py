"""Metrics collection and aggregation stored in MongoDB."""
from typing import Optional, Dict, Any
from datetime import datetime
from backend.app.database import db


class MetricsCollector:
    COLLECTION = "agent_metrics"

    @classmethod
    async def record(cls, *, agent_name: Optional[str], metric_type: str, value: Any, job_id: Optional[str] = None, request_id: Optional[str] = None, tags: Optional[Dict[str, Any]] = None) -> None:
        doc = {
            "agent_name": agent_name,
            "metric_type": metric_type,
            "value": value,
            "job_id": job_id,
            "request_id": request_id,
            "tags": tags or {},
            "timestamp": datetime.utcnow(),
        }
        await db[cls.COLLECTION].insert_one(doc)

    @classmethod
    async def aggregate_summary(cls) -> Dict[str, Any]:
        pipeline = [
            {"$group": {"_id": "$metric_type", "avg": {"$avg": "$value"}, "count": {"$sum": 1}}}
        ]
        cursor = db[cls.COLLECTION].aggregate(pipeline)
        res = {}
        async for row in cursor:
            res[row["_id"]] = {"avg": row["avg"], "count": row["count"]}
        return res
