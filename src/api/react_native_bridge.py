"""React Native Bridge - Mobile-optimized API endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import base64
from datetime import datetime

from ..core.auth import verify_api_key_and_jwt
from ..schemas.universal_schema import UniversalDesignSpec
from ..agents.main_agent import MainAgent
from ..services.preview_manager import PreviewManager

router = APIRouter(prefix="/api/v1/mobile", tags=["Mobile"])

class MobileGenerateRequest(BaseModel):
    prompt: str
    platform: str = "react-native"
    device_info: Optional[Dict[str, Any]] = None
    optimize_for_mobile: bool = True

class MobilePreviewRequest(BaseModel):
    spec_id: str
    format: str = "base64"  # base64, url, thumbnail
    size: str = "mobile"    # mobile, tablet, desktop

class MobileResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    mobile_optimized: bool = True

@router.post("/generate", response_model=MobileResponse)
async def mobile_generate(
    request: MobileGenerateRequest,
    auth_data: dict = Depends(verify_api_key_and_jwt)
):
    """Mobile-optimized design generation"""
    try:
        agent = MainAgent()
        
        # Mobile optimization: simplified prompt processing
        mobile_prompt = f"Mobile-optimized: {request.prompt}"
        if request.optimize_for_mobile:
            mobile_prompt += " (compact, touch-friendly, responsive)"
        
        spec = await agent.process_prompt(mobile_prompt)
        
        # Mobile-specific metadata
        spec.metadata.update({
            "platform": request.platform,
            "device_info": request.device_info or {},
            "mobile_optimized": True,
            "generated_for": "mobile_app"
        })
        
        return MobileResponse(
            success=True,
            data={
                "spec": spec.dict(),
                "mobile_features": {
                    "touch_optimized": True,
                    "responsive_design": True,
                    "offline_capable": False
                }
            }
        )
    except Exception as e:
        return MobileResponse(success=False, error=str(e))

@router.post("/preview", response_model=MobileResponse)
async def mobile_preview(
    request: MobilePreviewRequest,
    auth_data: dict = Depends(verify_api_key_and_jwt)
):
    """Mobile-optimized preview generation"""
    try:
        preview_manager = PreviewManager()
        
        # Generate mobile-sized preview
        preview_data = await preview_manager.generate_mobile_preview(
            request.spec_id,
            size=request.size
        )
        
        if request.format == "base64":
            # Convert to base64 for React Native Image component
            with open(preview_data["file_path"], "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            
            return MobileResponse(
                success=True,
                data={
                    "preview_base64": f"data:image/jpeg;base64,{image_data}",
                    "dimensions": preview_data.get("dimensions", {}),
                    "mobile_optimized": True
                }
            )
        else:
            return MobileResponse(
                success=True,
                data=preview_data
            )
    except Exception as e:
        return MobileResponse(success=False, error=str(e))

@router.get("/specs", response_model=MobileResponse)
async def mobile_specs_list(
    limit: int = 10,
    offset: int = 0,
    auth_data: dict = Depends(verify_api_key_and_jwt)
):
    """Mobile-optimized specs listing"""
    try:
        # Simplified spec listing for mobile
        specs = []  # Would fetch from database
        
        return MobileResponse(
            success=True,
            data={
                "specs": specs,
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "total": len(specs)
                },
                "mobile_optimized": True
            }
        )
    except Exception as e:
        return MobileResponse(success=False, error=str(e))

@router.post("/sync", response_model=MobileResponse)
async def mobile_sync(
    auth_data: dict = Depends(verify_api_key_and_jwt)
):
    """Mobile app sync endpoint"""
    try:
        sync_data = {
            "last_sync": datetime.now().isoformat(),
            "pending_uploads": 0,
            "cached_specs": 0,
            "app_version": "1.0.0"
        }
        
        return MobileResponse(
            success=True,
            data=sync_data
        )
    except Exception as e:
        return MobileResponse(success=False, error=str(e))