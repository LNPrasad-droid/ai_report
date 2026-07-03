from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
from backend.app.agents.retrieval.document_loader import load_document
from backend.app.agents.retrieval.retrieval_service import RetrievalService
from backend.app.agents.retrieval.retrieval_models import SearchRequest, SearchResponse
from backend.app.agents.retrieval.retrieval_exceptions import InvalidDocumentError, RetrievalError
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()


def get_retrieval_service() -> RetrievalService:
    # Use default configuration from settings
    return RetrievalService()


@router.post("/index")
async def index_document(file: UploadFile = File(...), metadata: Optional[str] = Form(None), service: RetrievalService = Depends(get_retrieval_service)):
    try:
        text, filename = await load_document(file)
        meta_obj = json.loads(metadata) if metadata else {"source": filename}
        doc_id = meta_obj.get("id") or filename
        count = await service.index_document(text=text, metadata=meta_obj, doc_id=doc_id)
        return {"indexed_chunks": count, "document_id": doc_id}
    except InvalidDocumentError as ide:
        logger.debug("Invalid document: %s", ide)
        raise HTTPException(status_code=400, detail=str(ide))
    except RetrievalError as re:
        logger.exception("Indexing failed: %s", re)
        raise HTTPException(status_code=500, detail="Indexing failed")


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest, service: RetrievalService = Depends(get_retrieval_service)) -> SearchResponse:
    try:
        resp = await service.search(request)
        return resp
    except RetrievalError as re:
        logger.exception("Search failed: %s", re)
        raise HTTPException(status_code=500, detail="Search failed")
