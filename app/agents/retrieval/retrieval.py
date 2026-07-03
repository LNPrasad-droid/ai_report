import logging
from typing import List, Dict
from backend.app.agents.retrieval.chunking import TextChunker
from backend.app.agents.retrieval.embeddings import EmbeddingService
from backend.app.agents.retrieval.vector_store import ChromaVectorStore
from backend.app.agents.retrieval.retrieval_models import DocumentMetadata, RetrievedChunk
from backend.app.agents.retrieval.retrieval_exceptions import RetrievalError

logger = logging.getLogger(__name__)


class RetrievalAgent:
    def __init__(self, chunker: TextChunker, embedder: EmbeddingService, store: ChromaVectorStore) -> None:
        self.chunker = chunker
        self.embedder = embedder
        self.store = store

    async def index_document(self, text: str, metadata: Dict, doc_id: str) -> int:
        try:
            chunks = self.chunker.chunk(text)
            if not chunks:
                logger.warning("No chunks created for document %s", doc_id)
                return 0

            embeddings = await self.embedder.embed_texts(chunks)
            metadatas = [metadata for _ in chunks]
            ids = [f"{doc_id}::chunk::{i}" for i in range(len(chunks))]
            await self.store.add_documents(ids=ids, embeddings=embeddings, metadatas=metadatas, texts=chunks)
            logger.info("Indexed %d chunks for document %s", len(chunks), doc_id)
            return len(chunks)
        except Exception as exc:
            logger.exception("Indexing failed for doc %s: %s", doc_id, exc)
            raise RetrievalError(str(exc))

    async def search(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        try:
            q_emb = (await self.embedder.embed_texts([query]))[0]
            results = await self.store.similarity_search(query_embedding=q_emb, top_k=top_k)
            logger.info("Search returned %d results for query", len(results))
            return results
        except Exception as exc:
            logger.exception("Search failed: %s", exc)
            raise RetrievalError(str(exc))
