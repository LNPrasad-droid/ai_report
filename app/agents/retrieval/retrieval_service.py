from backend.app.agents.retrieval.retrieval import RetrievalAgent
from backend.app.agents.retrieval.chunking import TextChunker
from backend.app.agents.retrieval.embeddings import EmbeddingService
from backend.app.agents.retrieval.vector_store import ChromaVectorStore
from backend.app.agents.retrieval.retrieval_models import SearchRequest, SearchResponse, RetrievedChunk
from typing import List
import logging

logger = logging.getLogger(__name__)


class RetrievalService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, model_name: str = None, persist_dir: str = None) -> None:
        chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        embedder = EmbeddingService(model_name=model_name)
        store = ChromaVectorStore(persist_directory=persist_dir)
        self.agent = RetrievalAgent(chunker=chunker, embedder=embedder, store=store)

    async def index_document(self, text: str, metadata: dict, doc_id: str) -> int:
        return await self.agent.index_document(text=text, metadata=metadata, doc_id=doc_id)

    async def search(self, request: SearchRequest) -> SearchResponse:
        results: List[RetrievedChunk] = await self.agent.search(request.query, top_k=request.top_k)
        return SearchResponse(query=request.query, results=results)
