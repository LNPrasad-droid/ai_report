from typing import List
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap must be >= 0")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> List[str]:
        """Split text into overlapping chunks based on character counts.

        This is a simple, language-agnostic chunker. Token-aware chunking
        can be added later.
        """
        text = text.strip()
        if not text:
            return []

        chunks: List[str] = []
        start = 0
        length = len(text)
        while start < length:
            end = min(start + self.chunk_size, length)
            chunk = text[start:end]
            chunks.append(chunk)
            if end == length:
                break
            start = end - self.chunk_overlap
            if start < 0:
                start = 0

        logger.debug("Generated %d chunks (chunk_size=%d, overlap=%d)", len(chunks), self.chunk_size, self.chunk_overlap)
        return chunks
