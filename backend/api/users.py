from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    LogoutRequest,
)
from services.user_service import UserService
from services.audit_service import AuditService
from core.database import get_db
from core.rbac import (
    Resource,
    Action,
    get_current_user,
    require_permission,
    get_permission_matrix,
    get_client_ip,
    normalize_role,
    Role,
)
from core.audit_actions import AuditAction, AuditStatus
from models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


def _client_meta(request: Request) -> dict:
    return {
        "ip_address": get_client_ip(request),
        "user_agent": request.headers.get("User-Agent"),
    }


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.USERS, Action.CREATE)),
):
    """Register a new user (admin only)."""
    existing_user = UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    if normalize_role(current_user.role) != Role.SUPERADMIN:
        if normalize_role(user.role) in (Role.SUPERADMIN, Role.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only SuperAdmin can assign admin roles",
            )

    new_user = UserService.create_user(db, user)
    meta = _client_meta(request)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.USER_CREATE.value,
        entity_type="User",
        entity_id=new_user.id,
        new_value={"email": new_user.email, "role": new_user.role},
        **meta,
    )
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(request_body: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Login user and return access + refresh tokens."""
    meta = _client_meta(request)
    user = UserService.authenticate_user(db, request_body.email, request_body.password)

    if not user:
        AuditService.log_event(
            db,
            AuditAction.LOGIN_FAILED.value,
            username=request_body.email,
            entity_type="Auth",
            status=AuditStatus.FAILURE.value,
            new_value={"email": request_body.email},
            **meta,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        AuditService.log_from_user(
            db,
            user,
            AuditAction.LOGIN_FAILED.value,
            entity_type="Auth",
            status=AuditStatus.FAILURE.value,
            new_value={"reason": "inactive_account"},
            **meta,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token, refresh_token, expires_in = UserService.issue_tokens(db, user)
    AuditService.log_from_user(
        db,
        user,
        AuditAction.LOGIN.value,
        entity_type="Auth",
        **meta,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "user": user,
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request_body: RefreshTokenRequest, request: Request, db: Session = Depends(get_db)):
    """Exchange a refresh token for new access and refresh tokens."""
    meta = _client_meta(request)
    result = UserService.refresh_access_token(db, request_body.refresh_token)
    if not result:
        AuditService.log_event(
            db,
            AuditAction.TOKEN_REFRESH.value,
            entity_type="Auth",
            status=AuditStatus.FAILURE.value,
            **meta,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    access_token, refresh_token, expires_in, user = result
    AuditService.log_from_user(
        db,
        user,
        AuditAction.TOKEN_REFRESH.value,
        entity_type="Auth",
        **meta,
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "user": user,
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request_body: LogoutRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Logout user and revoke refresh token."""
    meta = _client_meta(request)
    if request_body.refresh_token:
        UserService.revoke_refresh_token_by_value(db, request_body.refresh_token)
    else:
        UserService.revoke_refresh_token(db, current_user)

    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.LOGOUT.value,
        entity_type="Auth",
        **meta,
    )
    return None


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user


@router.get("/permissions/matrix")
def get_rbac_matrix(current_user: User = Depends(require_permission(Resource.USERS, Action.READ))):
    """Get RBAC permission matrix."""
    return get_permission_matrix()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.USERS, Action.READ)),
):
    """Get user by ID."""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=list[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.USERS, Action.READ)),
):
    """Get all users."""
    return UserService.get_all_users(db, skip, limit)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.USERS, Action.UPDATE)),
):
    """Update user by ID."""
    existing = UserService.get_user_by_id(db, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    old_role = existing.role
    update_data = user_update.model_dump(exclude_unset=True)

    if normalize_role(current_user.role) != Role.SUPERADMIN:
        if "role" in update_data and normalize_role(update_data["role"]) in (
            Role.SUPERADMIN,
            Role.ADMIN,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only SuperAdmin can assign admin roles",
            )

    user = UserService.update_user(db, user_id, user_update)
    meta = _client_meta(request)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.USER_UPDATE.value,
        entity_type="User",
        entity_id=user_id,
        old_value={"role": old_role} if "role" in update_data else None,
        new_value=update_data,
        **meta,
    )

    if "role" in update_data and update_data["role"] != old_role:
        AuditService.log_from_user(
            db,
            current_user,
            AuditAction.ROLE_CHANGE.value,
            entity_type="User",
            entity_id=user_id,
            old_value={"role": old_role},
            new_value={"role": user.role},
            **meta,
        )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Resource.USERS, Action.DELETE)),
):
    """Delete user by ID."""
    existing = UserService.get_user_by_id(db, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    if existing.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    if normalize_role(existing.role) == Role.SUPERADMIN:
        raise HTTPException(status_code=403, detail="Cannot delete SuperAdmin account")

    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    meta = _client_meta(request)
    AuditService.log_from_user(
        db,
        current_user,
        AuditAction.USER_DELETE.value,
        entity_type="User",
        entity_id=user_id,
        old_value={"email": existing.email, "role": existing.role},
        **meta,
    )
    return None
