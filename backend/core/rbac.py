from enum import Enum

class Role(str, Enum):
    """User roles for RBAC."""
    ADMIN = "admin"
    ANALYST = "analyst"
    OPERATOR = "operator"
    VIEWER = "viewer"

class Permission(str, Enum):
    """Permission types."""
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"

ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.DELETE, Permission.EXECUTE],
    Role.ANALYST: [Permission.READ, Permission.CREATE, Permission.UPDATE],
    Role.OPERATOR: [Permission.READ, Permission.UPDATE],
    Role.VIEWER: [Permission.READ],
}

def has_permission(role: Role, permission: Permission) -> bool:
    """Check if role has permission."""
    return permission in ROLE_PERMISSIONS.get(role, [])

def get_role_permissions(role: Role) -> list:
    """Get all permissions for a role."""
    return ROLE_PERMISSIONS.get(role, [])
