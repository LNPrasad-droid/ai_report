from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import status
import logging
from backend.app.auth.auth_service import AuthService
from backend.app.auth.auth_models import AuthenticatedUser
from backend.app.auth.auth_exceptions import TokenVerificationError
from backend.app.core.logger import set_request_context, clear_request_context

logger = logging.getLogger(__name__)


class FirebaseAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        authorization = request.headers.get("Authorization")
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            request_id = None

        request.state.user = None
        request.state.request_id = request_id

        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ", 1)[1].strip()
            try:
                auth_service = AuthService()
                user = await auth_service.verify_token(token)
                request.state.user = user
            except TokenVerificationError as exc:
                logger.warning("Invalid Firebase token: %s", exc)
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid authentication token"})
            except Exception as exc:
                logger.exception("Auth middleware failed")
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Authentication failed"})

        set_request_context(
            request_id=request_id or "-",
            user_id=getattr(request.state.user, "uid", "-"),
            user_email=getattr(request.state.user, "email", "-"),
            user_role=getattr(request.state.user, "role", "-")
        )

        try:
            response = await call_next(request)
        finally:
            clear_request_context()

        return response
