class RetrievalError(Exception):
    """Base exception for retrieval-related errors."""


class InvalidDocumentError(RetrievalError):
    """Raised when an uploaded document cannot be parsed."""


class EmbeddingError(RetrievalError):
    """Raised when embedding generation fails."""


class VectorStoreError(RetrievalError):
    """Raised for vector store related failures."""
