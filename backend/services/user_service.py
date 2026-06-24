from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import hash_password, verify_password, create_access_token, create_refresh_token
from core.rbac import normalize_role
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from typing import Optional, Tuple


class UserService:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        hashed_password = hash_password(user.password)
        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
            role=normalize_role(user.role).value,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        if "role" in update_data and update_data["role"]:
            update_data["role"] = normalize_role(update_data["role"]).value

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def issue_tokens(db: Session, user: User) -> Tuple[str, str, int]:
        """Issue access and refresh tokens, persisting refresh JTI on user."""
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role, "email": user.email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token, jti, expires_at = create_refresh_token(user.id)
        user.refresh_token_jti = jti
        user.refresh_token_expires_at = expires_at
        user.last_login = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return access_token, refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Optional[Tuple[str, str, int, User]]:
        """Validate refresh token and rotate tokens."""
        from core.security import decode_refresh_token

        payload = decode_refresh_token(refresh_token)
        if not payload:
            return None

        user_id = int(payload["sub"])
        jti = payload.get("jti")
        user = UserService.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            return None
        if not user.refresh_token_jti or user.refresh_token_jti != jti:
            return None
        if user.refresh_token_expires_at and user.refresh_token_expires_at < datetime.utcnow():
            return None

        return UserService.issue_tokens(db, user) + (user,)

    @staticmethod
    def revoke_refresh_token(db: Session, user: User) -> None:
        """Invalidate refresh token on logout."""
        user.refresh_token_jti = None
        user.refresh_token_expires_at = None
        db.add(user)
        db.commit()

    @staticmethod
    def revoke_refresh_token_by_value(db: Session, refresh_token: str) -> bool:
        """Revoke refresh token using the token string."""
        from core.security import decode_refresh_token

        payload = decode_refresh_token(refresh_token)
        if not payload:
            return False
        user = UserService.get_user_by_id(db, int(payload["sub"]))
        if not user:
            return False
        if user.refresh_token_jti != payload.get("jti"):
            return False
        UserService.revoke_refresh_token(db, user)
        return True
