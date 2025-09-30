"""Enhanced JWT authentication with refresh tokens"""

import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshRequest(BaseModel):
    refresh_token: str

class JWTAuth:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET", "dev-secret-key")
        self.algorithm = "HS256"
        self.access_token_expire = 15  # 15 minutes
        self.refresh_token_expire = 7 * 24 * 60  # 7 days in minutes
        
    def create_tokens(self, user_data: Dict[str, Any]) -> TokenResponse:
        """Create access and refresh tokens"""
        now = datetime.now(timezone.utc)
        
        # Access token
        access_payload = {
            "sub": user_data["username"],
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=self.access_token_expire)
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)
        
        # Refresh token
        refresh_payload = {
            "sub": user_data["username"],
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(minutes=self.refresh_token_expire)
        }
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.access_token_expire * 60
        )
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != token_type:
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """Create new access token from refresh token"""
        payload = self.verify_token(refresh_token, "refresh")
        if not payload:
            return None
        
        return self.create_tokens({"username": payload["sub"]})

# Global instance
jwt_auth = JWTAuth()