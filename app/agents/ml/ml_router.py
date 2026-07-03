from fastapi import APIRouter, Depends, HTTPException
from backend.app.agents.ml.ml_models import PredictRequest, BatchPredictRequest
from backend.app.agents.ml.ml_service import MLService
from backend.app.auth.dependencies import require_auth
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


def get_ml_service() -> MLService:
    return MLService()


@router.post("/predict")
async def predict(req: PredictRequest, user=Depends(require_auth), service: MLService = Depends(get_ml_service)):
    try:
        res = await service.predict(req, user_context={"uid": user.uid, "email": user.email, "role": user.role})
        return res.model_dump()
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/batch_predict")
async def batch_predict(req: BatchPredictRequest, user=Depends(require_auth), service: MLService = Depends(get_ml_service)):
    try:
        results = await service.batch_predict([i for i in req.items], user_context={"uid": user.uid, "email": user.email, "role": user.role})
        return [r.model_dump() for r in results]
    except Exception as exc:
        logger.exception("Batch prediction failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/models")
async def list_models(crop: str = None, service: MLService = Depends(get_ml_service)):
    try:
        from backend.app.agents.ml.ml_repository import MLRepository

        repo = MLRepository()
        models = await repo.list_models(crop=crop)
        return {"models": models}
    except Exception as exc:
        logger.exception("List models failed")
        raise HTTPException(status_code=500, detail=str(exc))
