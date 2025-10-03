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
        self.blacklist_file = "blacklisted_tokens.txt"
        self.blacklisted_tokens = self._load_blacklist()
        
    def create_tokens(self, user_data: Dict[str, Any]) -> TokenResponse:
        """Create access and refresh tokens"""
        import uuid
        now = datetime.now(timezone.utc)
        
        # Generate unique token IDs
        access_jti = str(uuid.uuid4())
        refresh_jti = str(uuid.uuid4())
        
        # Access token
        access_payload = {
            "sub": user_data["username"],
            "type": "access",
            "jti": access_jti,
            "iat": now,
            "exp": now + timedelta(minutes=self.access_token_expire)
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)
        
        # Refresh token
        refresh_payload = {
            "sub": user_data["username"],
            "type": "refresh",
            "jti": refresh_jti,
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
            
            # Check if token is blacklisted
            jti = payload.get("jti")
            if jti and jti in self.blacklisted_tokens:
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
        
        # Blacklist the old refresh token
        old_jti = payload.get("jti")
        if old_jti:
            self.blacklisted_tokens.add(old_jti)
            self._save_blacklist()
        
        return self.create_tokens({"username": payload["sub"]})

    def _load_blacklist(self) -> set:
        """Load blacklisted tokens from file"""
        try:
            if os.path.exists(self.blacklist_file):
                with open(self.blacklist_file, 'r') as f:
                    return set(line.strip() for line in f if line.strip())
        except Exception:
            pass
        return set()
    
    def _save_blacklist(self):
        """Save blacklisted tokens to file"""
        try:
            with open(self.blacklist_file, 'w') as f:
                for jti in self.blacklisted_tokens:
                    f.write(f"{jti}\n")
        except Exception:
            pass
    
    def blacklist_token(self, token: str) -> bool:
        """Manually blacklist a token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": False})
            jti = payload.get("jti")
            if jti:
                self.blacklisted_tokens.add(jti)
                self._save_blacklist()
                return True
        except jwt.InvalidTokenError:
            pass
        return False

# Global instance
jwt_auth = JWTAuth()