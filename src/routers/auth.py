"""Authentication router with JWT login"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.jwt_middleware import create_jwt_token, verify_token
from src.core.auth import verify_api_key
from pydantic import BaseModel
import os

router = APIRouter()

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str

class UserInfo(BaseModel):
    user_id: str
    username: str

@router.post("/auth/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    api_key: str = Depends(verify_api_key)
):
    """JWT login endpoint"""
    # Validate credentials
    demo_username = os.getenv("DEMO_USERNAME", "admin")
    demo_password = os.getenv("DEMO_PASSWORD", "bhiv2024")
    
    if form_data.username != demo_username or form_data.password != demo_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    access_token = create_jwt_token({"sub": form_data.username})
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=form_data.username
    )

@router.get("/auth/me", response_model=UserInfo)
async def get_current_user_info(
    current_user: str = Depends(verify_token),
    api_key: str = Depends(verify_api_key)
):
    """Get current user information"""
    return UserInfo(
        user_id=current_user,
        username=current_user
    )