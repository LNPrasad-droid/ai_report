from fastapi import Depends, HTTPException, Request, status
from backend.app.auth.auth_models import AuthenticatedUser
from backend.app.auth.auth_service import AuthService
from backend.app.auth.auth_exceptions import UnauthorizedError, RoleMismatchError


def get_auth_service() -> AuthService:
    return AuthService()


async def get_current_user(request: Request) -> AuthenticatedUser | None:
    return getattr(request.state, "user", None)


async def require_auth(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return user


def require_role(role: str):
    async def _require_role(user: AuthenticatedUser = Depends(require_auth)) -> AuthenticatedUser:
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User requires role {role}")
        return user
    return _require_role
