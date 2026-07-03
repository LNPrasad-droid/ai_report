import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.app.agents.gis.gis_service import GISService


@pytest.mark.asyncio
async def test_gis_service_process_job(monkeypatch):
    # Mock JobRepository.get_job to return a job with images
    mock_repo = MagicMock()
    job = MagicMock()
    job.results = {'images': [{'image_id': 'img1', 'satellite': 'SENTINEL_2'}]}
    mock_repo.get_job = AsyncMock(return_value=job)
    mock_repo.update_job = AsyncMock(return_value=True)

    # Mock provider and raster processor behaviour
    class DummyProvider:
        def get_image(self, image_id):
            return 'dummy_image'

        ee = MagicMock()

    provider = DummyProvider()
    svc = GISService(provider=provider, job_repo=mock_repo)

    # monkeypatch processor methods to avoid real ee calls
    svc.processor.clip_to_aoi = MagicMock(return_value='clipped')
    svc.processor.calculate_indices = MagicMock(return_value={'NDVI': 'idx_image'})
    svc.processor.compute_statistics = MagicMock(return_value={'NDVI': {'mean': 0.5}})

    res = await svc.process_job('job123', ['NDVI'], {'type':'Point','coordinates':[0,0]})
    assert 'indices' in res
