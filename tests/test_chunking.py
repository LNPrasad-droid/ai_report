from backend.app.agents.retrieval.chunking import TextChunker


def test_chunker_basic():
    text = """This is a test document. " * 200
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    chunks = chunker.chunk(text)
    assert len(chunks) > 0
    # ensure overlap present
    assert any(len(c) <= 100 for c in chunks)


def test_chunker_invalid_params():
    try:
        TextChunker(chunk_size=0)
        assert False, "Expected ValueError for chunk_size=0"
    except ValueError:
        pass
