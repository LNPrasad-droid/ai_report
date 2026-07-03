import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.app.providers.llm.ollama_provider import OllamaProvider


@pytest.mark.asyncio
async def test_ollama_health_check(monkeypatch):
    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=MagicMock(status_code=200, json=lambda: {'models': []}, raise_for_status=lambda: None))
    monkeypatch.setattr('httpx.AsyncClient', lambda base_url, timeout: mock_client)

    provider = OllamaProvider(base_url='http://localhost:11434')
    res = await provider.health_check()
    assert 'models' in res


@pytest.mark.asyncio
async def test_ollama_generate(monkeypatch):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.raise_for_status = lambda: None
    mock_response.json = lambda: {'text': 'result text'}
    mock_client.post = AsyncMock(return_value=mock_response)
    monkeypatch.setattr('httpx.AsyncClient', lambda base_url, timeout: mock_client)

    provider = OllamaProvider(base_url='http://localhost:11434')
    # set internal client to our mock to avoid creating real client
    provider.client = mock_client
    req = type('R', (), {'prompt': 'hello', 'model': None, 'temperature': None, 'top_p': None, 'max_tokens': None})
    resp = await provider.generate(req)
    assert resp.text == 'result text'
