import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.app.agents.ml.ml_service import MLService
from backend.app.agents.ml.ml_models import PredictRequest


class DummyModel:
    def predict(self, X):
        return [1]

    def predict_proba(self, X):
        return [[0.2, 0.8]]


@pytest.mark.asyncio
async def test_predict_success(monkeypatch):
    dummy = DummyModel()

    async def fake_get_model(crop, version=None):
        return {"storage_path": "./nonexistent.pkl", "model_name": "dummy", "version": "v1"}

    async def fake_load(path):
        return dummy

    service = MLService()
    monkeypatch.setattr('backend.app.agents.ml.ml_repository.MLRepository.get_model', fake_get_model)
    monkeypatch.setattr('backend.app.agents.ml.model_loader.ModelLoader.load', fake_load)

    req = PredictRequest(job_id="j1", features={"f1": 0.1, "f2": 0.2}, crop="rice")
    res = await service.predict(req)
    assert res.prediction == 1
    assert res.probability is not None
    assert res.inference_time_seconds >= 0


@pytest.mark.asyncio
async def test_predict_model_not_found(monkeypatch):
    async def fake_get_model(crop, version=None):
        return None

    service = MLService()
    monkeypatch.setattr('backend.app.agents.ml.ml_repository.MLRepository.get_model', fake_get_model)

    req = PredictRequest(job_id="j1", features={"f1": 0.1}, crop="unknown")
    with pytest.raises(Exception):
        await service.predict(req)
