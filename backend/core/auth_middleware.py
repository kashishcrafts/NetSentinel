from fastapi import Request, HTTPException, status
from core.security import decode_token
from typing import Callable

async def verify_token(request: Request, call_next: Callable) -> Callable:
    """Middleware to verify JWT token."""
    
    token = None
    auth_header = request.headers.get("Authorization")
    
    if auth_header:
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header"
            )
    
    if token:
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        request.state.user_id = payload.get("sub")
        request.state.user_role = payload.get("role")
    
    return await call_next(request)

def get_current_user_id(request: Request) -> int:
    """Get current user ID from request state."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user_id

def get_current_user_role(request: Request) -> str:
    """Get current user role from request state."""
    role = getattr(request.state, "user_role", None)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return role

def require_role(required_roles: list[str]):
    """Dependency to check if user has required role."""
    def check_role(request: Request):
        role = get_current_user_role(request)
        if role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return role
    return check_role

def require_admin(request: Request) -> str:
    """Dependency to check if user is admin."""
    return require_role(["admin"])(request)
