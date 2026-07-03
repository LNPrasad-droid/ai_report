import pytest


class DummyEmbedder:
    def __init__(self, *args, **kwargs):
        pass

    async def embed_texts(self, texts):
        return [[float(len(t)), 0.0] for t in texts]


class DummyStore:
    def __init__(self, *args, **kwargs):
        self.added = []

    async def add_documents(self, ids, embeddings, metadatas, texts):
        self.added.append((ids, embeddings, metadatas, texts))

    async def similarity_search(self, query_embedding, top_k):
        # return dummy RetrievedChunk-like dicts via model
        from backend.app.agents.retrieval.retrieval_models import RetrievedChunk, DocumentMetadata

        return [RetrievedChunk(id='1', text='doc', metadata=DocumentMetadata(source='test'), score=0.9)]


@pytest.mark.asyncio
async def test_retrieval_service_index_and_search(monkeypatch):
    # Monkeypatch EmbeddingService and ChromaVectorStore used in RetrievalService
    import backend.app.agents.retrieval.retrieval_service as svc_mod
    monkeypatch.setattr(svc_mod, 'EmbeddingService', DummyEmbedder)
    monkeypatch.setattr(svc_mod, 'ChromaVectorStore', DummyStore)

    service = svc_mod.RetrievalService(chunk_size=50, chunk_overlap=10, model_name='dummy')
    # index a small document
    count = await service.index_document("Hello world " * 10, {'source': 'unit_test'}, 'doc1')
    assert count > 0

    # search
    from backend.app.agents.retrieval.retrieval_models import SearchRequest
    resp = await service.search(SearchRequest(query='hello', top_k=3))
    assert resp.query == 'hello'
    assert len(resp.results) == 1
