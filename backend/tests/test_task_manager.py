import pytest
from unittest.mock import AsyncMock, MagicMock
from backend.app.agents.satellite.task_manager import TaskManager
from backend.app.agents.satellite.job_repository import JobRepository
from backend.app.agents.satellite.job_models import Job
from backend.app.agents.satellite.satellite_models import SearchRequest, SatelliteType


@pytest.mark.asyncio
async def test_create_search_job(monkeypatch):
    mock_repo = MagicMock()
    mock_repo.create_job = AsyncMock(return_value='job123')
    mock_repo.update_job = AsyncMock(return_value=True)
    mock_provider = MagicMock()
    mock_provider.search_imagery = MagicMock(return_value=[])

    tm = TaskManager(job_repo=mock_repo, provider=mock_provider)
    req = SearchRequest(aoi={'type':'Point','coordinates':[0,0]}, start_date='2020-01-01', end_date='2020-01-02')
    job_id = await tm.create_search_job(req)
    assert job_id == 'job123'
