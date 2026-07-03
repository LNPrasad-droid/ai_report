import time
import logging
from typing import Dict, Any, Optional, List
from backend.app.agents.ml.model_loader import ModelLoader
from backend.app.agents.ml.feature_pipeline import compute_indices
from backend.app.agents.ml.ml_repository import MLRepository
from backend.app.agents.ml.ml_models import PredictRequest, PredictResponse
from backend.app.agents.ml.ml_exceptions import ModelNotFoundError, PredictionError
from backend.app.monitoring.metrics import MetricsCollector

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self, loader: ModelLoader = None, repo: MLRepository = None):
        self.loader = loader or ModelLoader()
        self.repo = repo or MLRepository()

    async def _resolve_model(self, crop: str, model_version: Optional[str] = None) -> dict:
        meta = await self.repo.get_model(crop, version=model_version)
        if not meta:
            raise ModelNotFoundError(f"No model found for crop={crop} version={model_version}")
        return meta

    async def predict(self, request: PredictRequest, user_context: Optional[dict] = None) -> PredictResponse:
        meta = await self._resolve_model(request.crop, request.model_version)
        storage = meta.get("storage_path")
        model_name = meta.get("model_name")
        model_version = meta.get("version")

        t0 = time.time()
        model = await self.loader.load(storage)
        # prepare features: accept precomputed features or compute from GIS outputs
        features = request.features
        # ensure features numeric
        X = [float(features[k]) for k in sorted(features.keys())]

        try:
            # try predict_proba for probabilistic models
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba([X])[0]
                # assume binary or multi-class
                prediction = model.predict([X])[0]
                confidence = max(probs) if probs is not None else None
                probability = {str(i): float(p) for i, p in enumerate(probs)}
            else:
                prediction = model.predict([X])[0]
                probability = None
                confidence = None
        except Exception as exc:
            logger.exception("Prediction failed")
            raise PredictionError(str(exc)) from exc

        elapsed = time.time() - t0

        # record metrics
        await MetricsCollector.record(agent_name="MLAgent", metric_type="inference_time_seconds", value=elapsed, tags={"model_name": model_name, "model_version": model_version})
        await MetricsCollector.record(agent_name="MLAgent", metric_type="inference_confidence", value=confidence or 0.0, tags={"model_name": model_name, "model_version": model_version})

        fi = None
        # try to extract feature importance
        if hasattr(model, "feature_importances_"):
            try:
                fi = {str(i): float(v) for i, v in enumerate(model.feature_importances_)}
            except Exception:
                fi = None

        return PredictResponse(
            prediction=prediction,
            confidence=confidence,
            probability=probability,
            inference_time_seconds=elapsed,
            model_name=model_name,
            model_version=model_version,
            feature_importance=fi,
        )

    async def batch_predict(self, requests: List[PredictRequest], user_context: Optional[dict] = None) -> List[PredictResponse]:
        res = []
        for r in requests:
            pr = await self.predict(r, user_context=user_context)
            res.append(pr)
        return res
