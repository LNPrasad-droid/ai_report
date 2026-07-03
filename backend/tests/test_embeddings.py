import pytest


class DummyModel:
    def __init__(self, *args, **kwargs):
        pass

    def encode(self, texts, convert_to_numpy=False):
        # return list of vectors of length 3
        return [[float(len(t)), 0.0, 1.0] for t in texts]


@pytest.mark.asyncio
async def test_embedding_service_monkeypatch(monkeypatch):
    # Monkeypatch SentenceTransformer used in embeddings.EmbeddingService
    import backend.app.agents.retrieval.embeddings as emb_mod

    monkeypatch.setattr(emb_mod, 'SentenceTransformer', DummyModel)
    svc = emb_mod.EmbeddingService(model_name='dummy')
    embs = await svc.embed_texts(['a', 'bb', 'ccc'])
    assert isinstance(embs, list)
    assert len(embs) == 3
    assert embs[0][0] == 1.0
