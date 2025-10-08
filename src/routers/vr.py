"""VR Bridge endpoints for preview and metadata"""

from fastapi import APIRouter, Depends, HTTPException, Query
from src.auth import verify_api_key
from src.auth.jwt_middleware import verify_token
from src.services.preview_service import preview_service
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter()

class VRPreviewResponse(BaseModel):
    spec_id: str
    preview_url: str
    metadata: Dict[str, Any]
    vr_optimized: bool

class VRSceneRequest(BaseModel):
    prompt: str
    vr_settings: Dict[str, Any] = {}
    room_scale: bool = True

@router.get("/vr/preview", response_model=VRPreviewResponse)
async def get_vr_preview(
    spec_id: str = Query(..., description="Specification ID"),
    api_key: str = Depends(verify_api_key),
    current_user: str = Depends(verify_token)
):
    """Get VR-optimized preview URL and metadata"""
    try:
        # Generate VR-optimized preview URL
        preview_url = preview_service.generate_signed_glb_url(spec_id, expires_in=7200)  # 2 hours for VR
        
        # VR metadata
        metadata = {
            "format": "glb",
            "vr_ready": True,
            "room_scale": True,
            "interaction_points": [
                {"object_id": "obj_001", "type": "material_switch", "position": [0, 1, 0]},
                {"object_id": "floor_001", "type": "texture_change", "position": [0, 0, 0]}
            ],
            "lighting": {
                "ambient": 0.4,
                "directional": {"intensity": 0.8, "position": [10, 10, 5]}
            },
            "physics": {
                "gravity": -9.81,
                "collision_detection": True
            }
        }
        
        return VRPreviewResponse(
            spec_id=spec_id,
            preview_url=preview_url,
            metadata=metadata,
            vr_optimized=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VR preview generation failed: {str(e)}")

@router.post("/vr/scene")
async def create_vr_scene(
    body: VRSceneRequest,
    api_key: str = Depends(verify_api_key),
    current_user: str = Depends(verify_token)
):
    """Create VR scene from prompt"""
    try:
        # Mock VR scene generation
        scene_data = {
            "scene_id": f"vr_{hash(body.prompt) % 10000}",
            "prompt": body.prompt,
            "vr_assets": {
                "environment": "indoor_office",
                "skybox": "office_hdri",
                "floor_plan": "rectangular_10x8"
            },
            "teleport_points": [
                {"name": "entrance", "position": [0, 0, -4]},
                {"name": "desk_area", "position": [2, 0, 0]},
                {"name": "meeting_corner", "position": [-2, 0, 2]}
            ],
            "vr_settings": {
                "comfort_mode": True,
                "snap_turning": True,
                "hand_tracking": body.vr_settings.get("hand_tracking", False)
            }
        }
        
        return {
            "success": True,
            "scene_data": scene_data,
            "message": "VR scene created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VR scene creation failed: {str(e)}")