from typing import List, Dict, Any
import logging
from backend.app.agents.retrieval.retrieval_interfaces import VectorStoreInterface
from backend.app.agents.retrieval.retrieval_models import RetrievedChunk, DocumentMetadata
from backend.app.config import settings
from backend.app.agents.retrieval.retrieval_exceptions import VectorStoreError

logger = logging.getLogger(__name__)


class ChromaVectorStore(VectorStoreInterface):
    def __init__(self, persist_directory: str = None) -> None:
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings

            persist_dir = persist_directory or settings.CHROMA_PERSIST_DIR
            client_settings = ChromaSettings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir)
            self.client = chromadb.Client(client_settings)
            # Create a collection for documents
            self.collection = self.client.get_or_create_collection(name="documents")
            logger.info("ChromaDB collection ready (persist_dir=%s)", persist_dir)
        except Exception as exc:
            logger.exception("Failed to initialize ChromaDB: %s", exc)
            raise VectorStoreError(str(exc))

    async def add_documents(self, ids: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], texts: List[str]) -> None:
        try:
            # chroma expects sync API; run in executor
            def sync_add():
                self.collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)

            import asyncio
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, sync_add)
            logger.info("Inserted %d documents into ChromaDB", len(ids))
        except Exception as exc:
            logger.exception("Failed to add documents to ChromaDB: %s", exc)
            raise VectorStoreError(str(exc))

    async def similarity_search(self, query_embedding: List[float], top_k: int) -> List[RetrievedChunk]:
        try:
            def sync_query():
                res = self.collection.query(query_embeddings=[query_embedding], n_results=top_k, include=['metadatas','documents','distances'])
                return res

            import asyncio
            loop = asyncio.get_running_loop()
            res = await loop.run_in_executor(None, sync_query)

            results: List[RetrievedChunk] = []
            # res is a dict-like structure
            docs = res.get('documents', [[]])[0]
            metadatas = res.get('metadatas', [[]])[0]
            distances = res.get('distances', [[]])[0]
            ids = res.get('ids', [[]])[0]

            for i, doc in enumerate(docs):
                meta = metadatas[i] if i < len(metadatas) else None
                score = 1.0 - distances[i] if i < len(distances) else 0.0
                chunk = RetrievedChunk(id=ids[i], text=doc, metadata=DocumentMetadata(**(meta or {})), score=score)
                results.append(chunk)

            logger.info("ChromaDB query returned %d results", len(results))
            return results
        except Exception as exc:
            logger.exception("Failed to query ChromaDB: %s", exc)
            raise VectorStoreError(str(exc))
