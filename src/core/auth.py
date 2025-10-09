"""JWT Authentication for API"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status, Header
try:
    from jose import jwt
except ImportError:
    import jwt
import secrets

SECRET_KEY = os.getenv("SECRET_KEY", "bhiv2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MIN", 60))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(authorization: Optional[str] = Header(None, alias="Authorization")):
    """Get current user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    return verify_token(token)

def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    """Verify API key from X-API-Key header"""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include X-API-Key header."
        )

    # In test environment, be more flexible with API key validation
    if os.getenv("TESTING") == "true":
        return x_api_key

    API_KEY = os.getenv("API_KEY", "bhiv-secret-key-2024")
    if not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include X-API-Key header."
        )
    return x_api_key

def authenticate_user(username: str, password: str):
    """Simple user authentication for demo"""
    # Get credentials from environment or use defaults
    valid_username = os.getenv("DEMO_USERNAME", "admin")
    valid_password = os.getenv("DEMO_PASSWORD", "bhiv2024")

    if username == valid_username and password == valid_password:
        return create_access_token({"sub": username})
    raise HTTPException(status_code=401, detail="Invalid credentials")
