from enum import Enum
from typing import Optional, Set

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import decode_access_token
from models.user import User


class Role(str, Enum):
    """Enterprise user roles."""
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    SECURITY_ANALYST = "security_analyst"
    INCIDENT_RESPONDER = "incident_responder"
    VIEWER = "viewer"


class Resource(str, Enum):
    USERS = "users"
    THREATS = "threats"
    ALERTS = "alerts"
    REPORTS = "reports"
    INCIDENTS = "incidents"
    IOCS = "iocs"
    THREAT_INTEL = "threat_intel"
    AUDIT = "audit"
    SETTINGS = "settings"
    DETECTION = "detection"


class Action(str, Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"


# Legacy role aliases mapped to enterprise roles
LEGACY_ROLE_MAP = {
    "super admin": Role.SUPERADMIN,
    "superadmin": Role.SUPERADMIN,
    "admin": Role.ADMIN,
    "analyst": Role.SECURITY_ANALYST,
    "soc analyst": Role.SECURITY_ANALYST,
    "security analyst": Role.SECURITY_ANALYST,
    "security_analyst": Role.SECURITY_ANALYST,
    "operator": Role.INCIDENT_RESPONDER,
    "incident responder": Role.INCIDENT_RESPONDER,
    "incident_responder": Role.INCIDENT_RESPONDER,
    "viewer": Role.VIEWER,
}


def normalize_role(role: str) -> Role:
    """Normalize role string to enterprise Role enum."""
    if not role:
        return Role.VIEWER
    key = role.strip().lower().replace("-", "_")
    if key in Role._value2member_map_:
        return Role(key)
    return LEGACY_ROLE_MAP.get(key, LEGACY_ROLE_MAP.get(role.strip().lower(), Role.VIEWER))


def _perm(resource: Resource, action: Action) -> str:
    return f"{resource.value}:{action.value}"


ROLE_PERMISSIONS: dict[Role, Set[str]] = {
    Role.SUPERADMIN: set(),  # SuperAdmin bypasses checks
    Role.ADMIN: {
        _perm(Resource.USERS, Action.READ),
        _perm(Resource.USERS, Action.CREATE),
        _perm(Resource.USERS, Action.UPDATE),
        _perm(Resource.USERS, Action.DELETE),
        _perm(Resource.USERS, Action.EXECUTE),
        _perm(Resource.THREATS, Action.READ),
        _perm(Resource.THREATS, Action.CREATE),
        _perm(Resource.THREATS, Action.UPDATE),
        _perm(Resource.THREATS, Action.DELETE),
        _perm(Resource.ALERTS, Action.READ),
        _perm(Resource.ALERTS, Action.CREATE),
        _perm(Resource.ALERTS, Action.UPDATE),
        _perm(Resource.ALERTS, Action.DELETE),
        _perm(Resource.ALERTS, Action.EXECUTE),
        _perm(Resource.REPORTS, Action.READ),
        _perm(Resource.REPORTS, Action.CREATE),
        _perm(Resource.REPORTS, Action.UPDATE),
        _perm(Resource.REPORTS, Action.DELETE),
        _perm(Resource.INCIDENTS, Action.READ),
        _perm(Resource.INCIDENTS, Action.CREATE),
        _perm(Resource.INCIDENTS, Action.UPDATE),
        _perm(Resource.INCIDENTS, Action.DELETE),
        _perm(Resource.INCIDENTS, Action.EXECUTE),
        _perm(Resource.IOCS, Action.READ),
        _perm(Resource.IOCS, Action.CREATE),
        _perm(Resource.IOCS, Action.UPDATE),
        _perm(Resource.IOCS, Action.DELETE),
        _perm(Resource.THREAT_INTEL, Action.READ),
        _perm(Resource.THREAT_INTEL, Action.CREATE),
        _perm(Resource.THREAT_INTEL, Action.UPDATE),
        _perm(Resource.THREAT_INTEL, Action.DELETE),
        _perm(Resource.AUDIT, Action.READ),
        _perm(Resource.SETTINGS, Action.READ),
        _perm(Resource.SETTINGS, Action.UPDATE),
        _perm(Resource.DETECTION, Action.READ),
        _perm(Resource.DETECTION, Action.EXECUTE),
    },
    Role.SECURITY_ANALYST: {
        _perm(Resource.USERS, Action.READ),
        _perm(Resource.THREATS, Action.READ),
        _perm(Resource.THREATS, Action.CREATE),
        _perm(Resource.THREATS, Action.UPDATE),
        _perm(Resource.ALERTS, Action.READ),
        _perm(Resource.ALERTS, Action.CREATE),
        _perm(Resource.ALERTS, Action.UPDATE),
        _perm(Resource.ALERTS, Action.EXECUTE),
        _perm(Resource.REPORTS, Action.READ),
        _perm(Resource.REPORTS, Action.CREATE),
        _perm(Resource.INCIDENTS, Action.READ),
        _perm(Resource.IOCS, Action.READ),
        _perm(Resource.IOCS, Action.CREATE),
        _perm(Resource.IOCS, Action.UPDATE),
        _perm(Resource.THREAT_INTEL, Action.READ),
        _perm(Resource.THREAT_INTEL, Action.CREATE),
        _perm(Resource.THREAT_INTEL, Action.UPDATE),
        _perm(Resource.AUDIT, Action.READ),
        _perm(Resource.SETTINGS, Action.READ),
        _perm(Resource.DETECTION, Action.READ),
        _perm(Resource.DETECTION, Action.EXECUTE),
    },
    Role.INCIDENT_RESPONDER: {
        _perm(Resource.USERS, Action.READ),
        _perm(Resource.THREATS, Action.READ),
        _perm(Resource.ALERTS, Action.READ),
        _perm(Resource.ALERTS, Action.CREATE),
        _perm(Resource.ALERTS, Action.UPDATE),
        _perm(Resource.ALERTS, Action.EXECUTE),
        _perm(Resource.REPORTS, Action.READ),
        _perm(Resource.INCIDENTS, Action.READ),
        _perm(Resource.INCIDENTS, Action.CREATE),
        _perm(Resource.INCIDENTS, Action.UPDATE),
        _perm(Resource.INCIDENTS, Action.EXECUTE),
        _perm(Resource.IOCS, Action.READ),
        _perm(Resource.THREAT_INTEL, Action.READ),
        _perm(Resource.DETECTION, Action.READ),
        _perm(Resource.DETECTION, Action.EXECUTE),
    },
    Role.VIEWER: {
        _perm(Resource.USERS, Action.READ),
        _perm(Resource.THREATS, Action.READ),
        _perm(Resource.ALERTS, Action.READ),
        _perm(Resource.REPORTS, Action.READ),
        _perm(Resource.INCIDENTS, Action.READ),
        _perm(Resource.IOCS, Action.READ),
        _perm(Resource.THREAT_INTEL, Action.READ),
        _perm(Resource.SETTINGS, Action.READ),
        _perm(Resource.DETECTION, Action.READ),
    },
}


def has_permission(role: str, resource: Resource, action: Action) -> bool:
    """Check if a role has permission for a resource action."""
    normalized = normalize_role(role)
    if normalized == Role.SUPERADMIN:
        return True
    permission = _perm(resource, action)
    return permission in ROLE_PERMISSIONS.get(normalized, set())


def get_role_permissions(role: str) -> list[str]:
    """Get all permissions for a role."""
    normalized = normalize_role(role)
    if normalized == Role.SUPERADMIN:
        return ["*:*"]
    return sorted(ROLE_PERMISSIONS.get(normalized, set()))


def get_permission_matrix() -> dict:
    """Return the full RBAC permission matrix for documentation/API."""
    matrix = {}
    for role in Role:
        matrix[role.value] = get_role_permissions(role.value)
    return matrix


bearer_scheme = HTTPBearer(auto_error=False)


def get_client_ip(request: Request) -> Optional[str]:
    """Extract client IP from request, honoring X-Forwarded-For."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI dependency: authenticate user from Bearer token."""
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    request.state.user_id = user.id
    request.state.user_role = user.role
    request.state.user = user
    return user


def require_permission(resource: Resource, action: Action):
    """FastAPI dependency factory: require specific RBAC permission."""
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_permission(current_user.role, resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions: {resource.value}:{action.value}",
            )
        return current_user
    return checker


def require_role(*roles: Role):
    """FastAPI dependency factory: require one of the specified roles."""
    allowed = {r.value for r in roles}

    def checker(current_user: User = Depends(get_current_user)) -> User:
        normalized = normalize_role(current_user.role)
        if normalized.value not in allowed and normalized != Role.SUPERADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges",
            )
        return current_user
    return checker


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require Admin or SuperAdmin role."""
    normalized = normalize_role(current_user.role)
    if normalized not in (Role.ADMIN, Role.SUPERADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user
