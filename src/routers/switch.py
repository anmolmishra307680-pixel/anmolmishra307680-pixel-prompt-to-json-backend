"""Switch router for material and object editing"""

from fastapi import APIRouter, Depends, HTTPException
from src.schemas.spec_schema import Spec, ObjectSpec
from src.auth import verify_api_key, verify_jwt_token
from src.data.database import Database
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid

router = APIRouter()

class TargetObject(BaseModel):
    object_id: str

class MaterialUpdate(BaseModel):
    material: str
    properties: Optional[Dict[str, Any]] = None

class SwitchRequest(BaseModel):
    spec_id: str
    target: TargetObject
    update: MaterialUpdate
    note: Optional[str] = None

class ChangeInfo(BaseModel):
    object_id: str
    before: str
    after: str

class SwitchResponse(BaseModel):
    spec_id: str
    updated_spec_json: Dict[str, Any]
    preview_url: str
    changed: ChangeInfo

def get_database():
    return Database()

def find_object(spec: Spec, object_id: str) -> ObjectSpec:
    """Find object by ID in spec"""
    for obj in spec.objects:
        if obj.id == object_id:
            return obj
    raise HTTPException(status_code=404, detail=f"Object {object_id} not found")

async def trigger_preview(spec: Spec) -> str:
    """Generate signed GLB preview URL for updated spec"""
    from src.services.preview_service import preview_service
    return preview_service.trigger_preview(spec.dict())

@router.post("/switch", response_model=SwitchResponse)
async def switch_material(
    body: SwitchRequest,
    api_key: str = Depends(verify_api_key),
    token: str = Depends(verify_jwt_token),
    db: Database = Depends(get_database)
):
    """Switch object materials with iteration tracking"""
    try:
        # Get existing spec from database
        spec_data = await db.get_spec(body.spec_id)
        if not spec_data:
            raise HTTPException(status_code=404, detail="Spec not found")
        
        # Convert to Spec object
        spec = Spec(**spec_data)
        
        # Find target object
        obj = find_object(spec, body.target.object_id)
        
        # Store before state
        before_material = obj.material
        before_properties = obj.properties.copy() if obj.properties else {}
        
        # Apply material change
        obj.material = body.update.material
        
        # Apply property changes if provided
        if body.update.properties:
            if not obj.properties:
                obj.properties = {}
            obj.properties.update(body.update.properties)
        
        # Save iteration to database
        iteration_id = await db.save_iteration(
            spec_id=body.spec_id,
            before_spec={"material": before_material, "properties": before_properties},
            after_spec={"material": obj.material, "properties": obj.properties},
            feedback=body.note or f"Changed {body.target.object_id} material to {body.update.material}"
        )
        
        # Update spec in database
        await db.update_spec(body.spec_id, spec.dict())
        
        # Generate new preview
        preview_url = await trigger_preview(spec)
        
        # Create response
        change_info = ChangeInfo(
            object_id=body.target.object_id,
            before=before_material,
            after=obj.material
        )
        
        return SwitchResponse(
            spec_id=body.spec_id,
            updated_spec_json=spec.dict(),
            preview_url=preview_url,
            changed=change_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Switch operation failed: {str(e)}")