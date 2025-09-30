from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from typing import Dict, Any

class Position3D(BaseModel):
    x: float = Field(default=0.0, description="X coordinate")
    y: float = Field(default=0.0, description="Y coordinate") 
    z: float = Field(default=0.0, description="Z coordinate")

class Dimensions3D(BaseModel):
    width: float = Field(description="Width dimension")
    height: float = Field(description="Height dimension")
    depth: float = Field(description="Depth dimension")
    units: str = Field(default="meters", description="Unit of measurement")

class DesignObject(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique object ID")
    type: str = Field(description="Object type (wall, door, window, etc.)")
    material: str = Field(description="Primary material")
    position: Position3D = Field(default_factory=Position3D, description="3D position")
    dimensions: Dimensions3D = Field(description="Object dimensions")
    editable: bool = Field(default=True, description="Whether object can be edited")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")

class SceneInfo(BaseModel):
    name: str = Field(description="Scene/design name")
    description: str = Field(description="Scene description")
    total_objects: int = Field(description="Total number of objects")
    bounding_box: Dimensions3D = Field(description="Overall scene dimensions")

class VersionInfo(BaseModel):
    version: str = Field(default="1.0", description="Design version")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    author: str = Field(default="system", description="Design author")

class EnhancedDesignSpec(BaseModel):
    spec_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique spec ID")
    objects: List[DesignObject] = Field(description="List of design objects")
    scene: SceneInfo = Field(description="Scene information")
    version: VersionInfo = Field(default_factory=VersionInfo, description="Version information")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class GenerateRequestV2(BaseModel):
    prompt: str = Field(description="Design generation prompt")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    style: Optional[str] = Field(default=None, description="Design style preference")
    constraints: Optional[List[str]] = Field(default=None, description="Design constraints")

class GenerateResponseV2(BaseModel):
    spec_id: str = Field(description="Generated specification ID")
    spec_json: EnhancedDesignSpec = Field(description="Generated design specification")
    preview_url: Optional[str] = Field(default=None, description="Preview image URL")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    processing_time: Optional[float] = Field(default=None, description="Generation time in seconds")

class SwitchRequest(BaseModel):
    spec_id: str = Field(description="Specification ID to modify")
    instruction: str = Field(description="Change instruction (e.g., 'change floor to marble')")

class ChangeInfo(BaseModel):
    object_id: str = Field(description="ID of changed object")
    before: Dict[str, Any] = Field(description="Object state before change")
    after: Dict[str, Any] = Field(description="Object state after change")

class SwitchResponse(BaseModel):
    spec_id: str = Field(description="Updated specification ID")
    updated_spec_json: EnhancedDesignSpec = Field(description="Updated design specification")
    preview_url: Optional[str] = Field(default=None, description="Updated preview URL")
    iteration_id: str = Field(description="Iteration/change ID")
    changed: ChangeInfo = Field(description="Details of what changed")
    saved_at: str = Field(default_factory=lambda: datetime.now().isoformat())