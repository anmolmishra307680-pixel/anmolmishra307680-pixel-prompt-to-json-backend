"""Generate router with LM Adapter integration"""

from fastapi import APIRouter, Depends, HTTPException
from src.schemas.spec_schema import GenerateRequest, GenerateResponse, Spec, ObjectSpec, SceneSpec
from src.lm_adapter import LMAdapter
from src.core.auth import verify_api_key, get_current_user as verify_jwt_token
from src.auth.jwt_middleware import verify_token
import uuid
from typing import Dict, Any

router = APIRouter()

def get_lm_adapter():
    """Dependency to provide LM Adapter instance"""
    return LMAdapter()

def build_spec_from_lm(result: dict) -> Spec:
    """Build Spec object from LM result"""
    spec_id = str(uuid.uuid4())
    
    # Extract objects
    objects = []
    if "objects" in result:
        for obj_data in result["objects"]:
            objects.append(ObjectSpec(**obj_data))
    else:
        # Default object if none provided
        objects.append(ObjectSpec(
            id="obj_001",
            type="main_structure",
            material="steel",
            editable=True,
            properties={"width": 10.0, "height": 8.0, "depth": 12.0}
        ))
    
    # Extract scene
    scene_data = result.get("scene", {})
    scene = SceneSpec(**scene_data)
    
    return Spec(
        spec_id=spec_id,
        objects=objects,
        scene=scene,
        design_type=result.get("design_type"),
        metadata={"generated_from": "lm_adapter"}
    )

async def trigger_preview(spec: Spec) -> str:
    """Generate signed GLB preview URL"""
    from src.services.preview_service import preview_service
    return preview_service.trigger_preview(spec.dict())

@router.post("/generate", response_model=GenerateResponse)
async def generate(
    body: GenerateRequest,
    api_key: str = Depends(verify_api_key),
    current_user: str = Depends(verify_token),
    lm: LMAdapter = Depends(get_lm_adapter)
):
    """Generate design specification using LM Adapter"""
    try:
        # Prepare context parameters
        context = body.context or {}
        if body.design_type:
            context["design_type"] = body.design_type
        
        # Generate using LM Adapter
        result = lm.run(body.prompt, params=context)
        
        # Build spec from LM result
        spec = build_spec_from_lm(result)
        
        # Generate preview URL
        preview_url = await trigger_preview(spec)
        
        # Save to database (mock implementation)
        try:
            from src.data.database import Database
            db = Database()
            await db.insert_spec(spec.dict())
        except Exception as e:
            print(f"Database save failed: {e}")
        
        return GenerateResponse(
            spec_id=spec.spec_id,
            spec_json=spec.dict(),
            preview_url=preview_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")