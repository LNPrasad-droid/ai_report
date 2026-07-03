import os
import pickle
import joblib
import logging
from typing import Any
from backend.app.agents.ml.ml_exceptions import ModelLoadError

logger = logging.getLogger(__name__)


class ModelLoader:
    """Generic model loader supporting joblib and pickle files.

    Future: add ONNX and other formats.
    """

    @staticmethod
    async def load(storage_path: str) -> Any:
        if not os.path.exists(storage_path):
            raise ModelLoadError(f"Model file not found: {storage_path}")

        # infer loader by extension
        _, ext = os.path.splitext(storage_path.lower())
        try:
            if ext in (".joblib", ".jl"):
                model = joblib.load(storage_path)
                return model
            elif ext in (".pkl", ".pickle"):
                with open(storage_path, "rb") as f:
                    model = pickle.load(f)
                return model
            else:
                # fallback: try joblib then pickle
                try:
                    return joblib.load(storage_path)
                except Exception:
                    with open(storage_path, "rb") as f:
                        return pickle.load(f)
        except Exception as exc:
            logger.exception("Failed to load model %s", storage_path)
            raise ModelLoadError(str(exc)) from exc
