from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from backend.app.agents.retrieval.retrieval_models import RetrievedChunk


class VectorStoreInterface(ABC):
    @abstractmethod
    async def add_documents(self, ids: List[str], embeddings: List[list], metadatas: List[dict], texts: List[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def similarity_search(self, query_embedding: list, top_k: int) -> List[RetrievedChunk]:
        raise NotImplementedError
