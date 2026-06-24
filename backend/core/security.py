import secrets
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional, Tuple
from core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a short-lived JWT access token with explicit expiration."""
    to_encode = data.copy()
    expire = _utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update(
        {
            "exp": expire,
            "iat": _utcnow(),
            "type": TOKEN_TYPE_ACCESS,
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: int, expires_delta: Optional[timedelta] = None) -> Tuple[str, str, datetime]:
    """Create a refresh token. Returns (token, jti, expires_at)."""
    jti = secrets.token_urlsafe(32)
    expires_at = _utcnow() + (
        expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "exp": expires_at,
        "iat": _utcnow(),
        "type": TOKEN_TYPE_REFRESH,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti, expires_at


def _decode_token(token: str, expected_type: str) -> Optional[dict]:
    """Decode and validate a JWT, enforcing token type and expiration."""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require_exp": True},
        )
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate an access token."""
    return _decode_token(token, TOKEN_TYPE_ACCESS)


def decode_refresh_token(token: str) -> Optional[dict]:
    """Decode and validate a refresh token."""
    return _decode_token(token, TOKEN_TYPE_REFRESH)


def decode_token(token: str) -> Optional[dict]:
    """Decode any valid token (access or refresh). Prefer typed decoders."""
    payload = decode_access_token(token)
    if payload:
        return payload
    return decode_refresh_token(token)
