from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend.app.auth.auth_service import AuthService
from backend.app.auth.auth_models import AuthenticatedUser, UserProfileUpdate, AuthResponse
from backend.app.auth.dependencies import require_auth, get_auth_service
from backend.app.auth.auth_exceptions import AuthError
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class LoginRequest(BaseModel):
    token: str


def get_service() -> AuthService:
    return AuthService()


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, auth_service: AuthService = Depends(get_service)) -> AuthResponse:
    try:
        user = await auth_service.verify_token(request.token)
        return AuthResponse(**user.model_dump())
    except AuthError as exc:
        logger.exception("Login failed")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


@router.get("/me", response_model=AuthResponse)
async def me(user: AuthenticatedUser = Depends(require_auth)) -> AuthResponse:
    return AuthResponse(**user.model_dump())


@router.put("/profile", response_model=AuthResponse)
async def update_profile(profile: UserProfileUpdate, user: AuthenticatedUser = Depends(require_auth), auth_service: AuthService = Depends(get_service)) -> AuthResponse:
    updated = await auth_service.update_profile(user.uid, profile)
    return AuthResponse(**updated.model_dump())


@router.get("/roles")
async def roles(user: AuthenticatedUser = Depends(require_auth)) -> dict:
    return {"role": user.role}
