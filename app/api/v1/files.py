import logging
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from backend.app import database
from backend.app.auth.dependencies import require_auth
from backend.app.auth.auth_models import AuthenticatedUser

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: AuthenticatedUser = Depends(require_auth),
):
    try:
        content = await file.read()
        collection = database.db.get_collection("uploaded_files")
        doc = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "uploaded_by": current_user.uid,
            "created_at": datetime.utcnow(),
            "content": content,
        }
        result = await collection.insert_one(doc)
        return {
            "id": str(result.inserted_id),
            "file_id": str(result.inserted_id),
            "fileName": file.filename,
            "content_type": file.content_type,
            "size": len(content),
        }
    except Exception as exc:
        logger.exception("Failed to upload file: %s", exc)
        raise HTTPException(status_code=500, detail="File upload failed")
