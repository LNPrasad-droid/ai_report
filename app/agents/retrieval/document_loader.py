from typing import Tuple
from fastapi import UploadFile
from backend.app.agents.retrieval.retrieval_exceptions import InvalidDocumentError
import logging
from io import BytesIO
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


async def load_document(upload_file: UploadFile) -> Tuple[str, str]:
    """Load document content from UploadFile.

    Returns a tuple of (text, filename).
    Supports PDF, .txt, .md
    """
    filename = upload_file.filename
    content = await upload_file.read()

    if filename.lower().endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(content))
            text_parts = []
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
            text = "\n".join(text_parts)
            return text, filename
        except Exception as exc:
            logger.exception("Failed to parse PDF %s: %s", filename, exc)
            raise InvalidDocumentError(f"Failed to parse PDF: {exc}")

    if filename.lower().endswith(".txt") or filename.lower().endswith(".md"):
        try:
            text = content.decode("utf-8")
            return text, filename
        except Exception as exc:
            logger.exception("Failed to decode text file %s: %s", filename, exc)
            raise InvalidDocumentError(f"Failed to decode text file: {exc}")

    logger.error("Unsupported file type: %s", filename)
    raise InvalidDocumentError("Unsupported file type")
