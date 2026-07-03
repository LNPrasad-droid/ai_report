from typing import List
import logging
import asyncio
from sentence_transformers import SentenceTransformer
from backend.app.config import settings
from backend.app.agents.retrieval.retrieval_exceptions import EmbeddingError

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self, model_name: str = None) -> None:
        self.model_name = model_name or settings.EMBEDDING_MODEL
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info("Loaded embedding model: %s", self.model_name)
        except Exception as exc:
            logger.exception("Failed to load embedding model: %s", exc)
            raise EmbeddingError(str(exc))

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        loop = asyncio.get_running_loop()
        try:
            # Run blocking model.encode in executor
            embeddings = await loop.run_in_executor(None, lambda: self.model.encode(texts, convert_to_numpy=True).tolist())
            logger.info("Generated embeddings for %d texts", len(texts))
            return embeddings
        except Exception as exc:
            logger.exception("Embedding generation failed: %s", exc)
            raise EmbeddingError(str(exc))
