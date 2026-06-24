from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

from core.config import PUBLIC_PATHS
from core.security import decode_access_token


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Cache-Control"] = "no-store"
        return response


class AuthContextMiddleware(BaseHTTPMiddleware):
    """
    Populate request.state with authenticated user context when a valid
    Bearer token is present. Route-level dependencies enforce authorization.
    """

    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path.rstrip("/") or "/"
        request.state.is_public = path in PUBLIC_PATHS or path.startswith("/docs")

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            if token:
                payload = decode_access_token(token)
                if payload and payload.get("sub"):
                    request.state.user_id = int(payload["sub"])
                    request.state.user_role = payload.get("role")
                elif not request.state.is_public:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Invalid or expired token"},
                        headers={"WWW-Authenticate": "Bearer"},
                    )

        return await call_next(request)


def get_current_user_id(request: Request) -> int:
    """Get current user ID from request state."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return int(user_id)


def get_current_user_role(request: Request) -> str:
    """Get current user role from request state."""
    role = getattr(request.state, "user_role", None)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return role
