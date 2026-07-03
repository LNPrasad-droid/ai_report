import os
import json
import logging
from pathlib import Path
from typing import Optional
import firebase_admin
from firebase_admin import credentials, auth
from backend.app.config import settings
from backend.app.auth.auth_exceptions import FirebaseInitializationError, TokenVerificationError, AuthError

logger = logging.getLogger(__name__)

FIREBASE_APP_NAME = "agentic_geoai_platform"


def initialize_firebase() -> firebase_admin.App:
    if firebase_admin._apps:
        # Use existing app if already initialized
        return list(firebase_admin._apps.values())[0]

    base_dir = Path(__file__).resolve().parent.parent.parent
    service_account_path = base_dir / settings.FIREBASE_SERVICE_ACCOUNT

    if not service_account_path.exists():
        raise FirebaseInitializationError(f"Firebase service account file not found: {service_account_path}")

    try:
        with service_account_path.open("r", encoding="utf-8") as f:
            json.load(f)
    except json.JSONDecodeError as exc:
        raise FirebaseInitializationError(f"Invalid Firebase service account JSON: {exc}") from exc
    except Exception as exc:
        raise FirebaseInitializationError(f"Unable to load Firebase service account: {exc}") from exc

    try:
        cred = credentials.Certificate(str(service_account_path))
        app = firebase_admin.initialize_app(cred, {"projectId": settings.FIREBASE_PROJECT_ID}, name=FIREBASE_APP_NAME)
        logger.info("Firebase Admin initialized for project %s", settings.FIREBASE_PROJECT_ID)
        return app
    except ValueError as exc:
        # Duplicate initialization is okay; use existing app
        if "already exists" in str(exc):
            return list(firebase_admin._apps.values())[0]
        raise FirebaseInitializationError(str(exc)) from exc
    except Exception as exc:
        raise FirebaseInitializationError(f"Firebase initialization failed: {exc}") from exc


def verify_id_token(token: str) -> dict:
    initialize_firebase()
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception as exc:
        raise TokenVerificationError(str(exc)) from exc


def get_user(uid: str) -> dict:
    initialize_firebase()
    try:
        user_record = auth.get_user(uid)
        return user_record.__dict__
    except Exception as exc:
        raise AuthError(str(exc)) from exc
