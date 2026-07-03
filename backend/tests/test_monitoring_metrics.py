import pytest
from backend.app.monitoring.metrics import MetricsCollector


@pytest.mark.asyncio
async def test_metrics_record_and_aggregate(monkeypatch):
    # Patch db collection methods
    class FakeColl:
        def __init__(self):
            self.docs = []

        async def insert_one(self, doc):
            self.docs.append(doc)

        def aggregate(self, pipeline):
            async def _gen():
                yield {"_id": "request_duration_seconds", "avg": 0.5, "count": 1}

            return _gen()

    monkeypatch.setattr('backend.app.monitoring.metrics.db', {MetricsCollector.COLLECTION: FakeColl()})

    await MetricsCollector.record(agent_name='test', metric_type='request_duration_seconds', value=0.42)
    summary = await MetricsCollector.aggregate_summary()
    assert 'request_duration_seconds' in summary
