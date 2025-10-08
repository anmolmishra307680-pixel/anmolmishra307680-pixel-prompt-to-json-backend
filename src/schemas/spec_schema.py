"""Extended Spec Schema with ObjectSpec and SceneSpec"""

from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ObjectSpec(BaseModel):
    id: str
    type: str
    material: str
    editable: bool = True
    properties: Dict[str, Any]

class SceneSpec(BaseModel):
    environment: str = "indoor"
    lighting: str = "natural"
    scale: float = 1.0
    background: Optional[str] = None

class Spec(BaseModel):
    spec_id: str
    objects: List[ObjectSpec]
    scene: SceneSpec
    design_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class GenerateRequest(BaseModel):
    prompt: str
    context: Optional[Dict[str, Any]] = None
    design_type: Optional[str] = None

class GenerateResponse(BaseModel):
    spec_id: str
    spec_json: Dict[str, Any]
    preview_url: Optional[str] = None
    status: str = "success"