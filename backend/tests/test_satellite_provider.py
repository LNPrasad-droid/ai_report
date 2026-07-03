import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_gee_provider_search(monkeypatch):
    # Mock ee module and its methods
    mock_ee = MagicMock()
    mock_ImageCollection = MagicMock()
    mock_ImageCollection.filterDate.return_value = mock_ImageCollection
    mock_ImageCollection.filterBounds.return_value = mock_ImageCollection
    mock_ImageCollection.limit.return_value = mock_ImageCollection
    mock_ImageCollection.toList.return_value = MagicMock(size=MagicMock(return_value=1), get=MagicMock(return_value=0))

    import sys
    monkeypatch.setitem(sys.modules, 'ee', mock_ee)
    monkeypatch.setattr(mock_ee, 'ImageCollection', lambda name: mock_ImageCollection)
    monkeypatch.setattr(mock_ee, 'Geometry', lambda geo: geo)
    # mock Image and getInfo
    mock_img = MagicMock()
    mock_img.getInfo.return_value = {'id': 'img1', 'properties': {'CLOUD_COVER': 10}, 'bands': [{'id': 'B1'}], 'geometry': {}}
    mock_images = MagicMock()
    mock_images.size.return_value.getInfo.return_value = 1
    mock_images.get.return_value = 0
    mock_ImageCollection.toList.return_value = mock_images
    monkeypatch.setattr(mock_ee, 'Image', lambda x: mock_img)

    from backend.app.agents.satellite.gee_provider import GoogleEarthEngineProvider

    provider = GoogleEarthEngineProvider(project='ee-leo913173')
    # monkeypatch initialize to skip real ee.Initialize
    monkeypatch.setattr(provider, 'initialize', lambda: None)
    provider.initialized = True
    results = provider.search_imagery(aoi={'type':'Point','coordinates':[0,0]}, start_date='2020-01-01', end_date='2020-12-31', max_cloud_cover=20, max_results=1, satellite='SENTINEL_2')
    assert isinstance(results, list)
