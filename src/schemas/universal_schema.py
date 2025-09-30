from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import uuid

class MaterialSpec(BaseModel):
    type: str = Field(description="Material type (steel, plastic, wood, fabric, etc.)")
    grade: Optional[str] = Field(default=None, description="Material grade or specification")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Material properties")

class DimensionSpec(BaseModel):
    length: Optional[float] = Field(default=None, description="Length in appropriate units")
    width: Optional[float] = Field(default=None, description="Width in appropriate units")
    height: Optional[float] = Field(default=None, description="Height in appropriate units")
    depth: Optional[float] = Field(default=None, description="Depth in appropriate units")
    diameter: Optional[float] = Field(default=None, description="Diameter for circular objects")
    area: Optional[float] = Field(default=None, description="Area in appropriate units")
    volume: Optional[float] = Field(default=None, description="Volume in appropriate units")
    weight: Optional[float] = Field(default=None, description="Weight in appropriate units")
    units: str = Field(default="metric", description="Unit system (metric, imperial)")

class PerformanceSpec(BaseModel):
    power: Optional[str] = Field(default=None, description="Power specifications")
    efficiency: Optional[str] = Field(default=None, description="Efficiency ratings")
    capacity: Optional[str] = Field(default=None, description="Capacity specifications")
    speed: Optional[str] = Field(default=None, description="Speed specifications")
    other_specs: Dict[str, Any] = Field(default_factory=dict, description="Other performance metrics")

class DesignObject(BaseModel):
    object_id: str = Field(default_factory=lambda: f"obj_{uuid.uuid4().hex[:8]}", description="Unique object identifier")
    type: str = Field(description="Object type (floor, wall, chair, etc.)")
    material: str = Field(description="Primary material")
    dimensions: DimensionSpec = Field(default_factory=DimensionSpec, description="Object dimensions")
    position: Dict[str, float] = Field(default_factory=lambda: {"x": 0.0, "y": 0.0, "z": 0.0}, description="3D position")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")
    editable: bool = Field(default=True, description="Whether object can be edited")

class MetadataSpec(BaseModel):
    editable: bool = Field(default=True, description="Whether entire design is editable")
    version: str = Field(default="1.0", description="Design version")
    author: str = Field(default="system", description="Design author")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Creation timestamp")
    modified_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Last modification")
    tags: List[str] = Field(default_factory=list, description="Design tags")
    notes: str = Field(default="", description="Design notes")

class UniversalDesignSpec(BaseModel):
    design_type: str = Field(description="Type of design (building, vehicle, electronics, furniture, etc.)")
    category: str = Field(description="Specific category within design type")
    objects: List[DesignObject] = Field(default_factory=list, description="Design objects with unique IDs")
    materials: List[MaterialSpec] = Field(default_factory=list, description="Materials used")
    dimensions: DimensionSpec = Field(default_factory=DimensionSpec, description="Physical dimensions")
    performance: PerformanceSpec = Field(default_factory=PerformanceSpec, description="Performance specifications")
    features: List[str] = Field(default_factory=list, description="Special features and capabilities")
    components: List[str] = Field(default_factory=list, description="Main components or parts")
    requirements: List[str] = Field(default_factory=list, description="Design requirements")
    constraints: List[str] = Field(default_factory=list, description="Design constraints")
    use_cases: List[str] = Field(default_factory=list, description="Intended use cases")
    target_audience: Optional[str] = Field(default=None, description="Target user group")
    estimated_cost: Optional[str] = Field(default=None, description="Estimated cost range")
    timeline: Optional[str] = Field(default=None, description="Development/construction timeline")
    metadata: MetadataSpec = Field(default_factory=MetadataSpec, description="Design metadata with editability")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Generation timestamp")

    @field_validator('materials')
    @classmethod
    def validate_materials(cls, v):
        if not v:
            return [MaterialSpec(type="standard")]
        return v

class EvaluationResult(BaseModel):
    score: float = Field(description="Overall evaluation score (0-100)")
    completeness: float = Field(description="Completeness score (0-100)")
    format_validity: float = Field(description="Format validity score (0-100)")
    feasibility: float = Field(default=85.0, description="Feasibility score (0-100)")
    innovation: float = Field(default=70.0, description="Innovation score (0-100)")
    practicality: float = Field(default=80.0, description="Practicality score (0-100)")
    feedback: List[str] = Field(default_factory=list, description="Feedback comments")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Evaluation timestamp")

    @field_validator('score', 'completeness', 'format_validity', 'feasibility', 'innovation', 'practicality')
    @classmethod
    def validate_scores(cls, v):
        return max(0, min(100, v))

class RLIterationResult(BaseModel):
    iteration: int = Field(description="Iteration number")
    iteration_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique iteration ID")
    spec_before: Optional[Dict[str, Any]] = Field(default=None, description="Spec before improvement")
    spec_after: Dict[str, Any] = Field(description="Spec after improvement")
    score_before: float = Field(default=0.0, description="Score before improvement")
    score_after: float = Field(description="Score after improvement")
    evaluation: Dict[str, Any] = Field(description="Evaluation details")
    feedback: str = Field(description="Feedback for improvement")
    reward: float = Field(description="RL reward signal")
    improvement: float = Field(default=0.0, description="Score improvement")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Iteration timestamp")

class CoordinationResult(BaseModel):
    success: bool = Field(description="Coordination success status")
    agents_used: List[str] = Field(description="List of agents involved")
    iterations: int = Field(description="Number of coordination iterations")
    final_spec: Dict[str, Any] = Field(description="Final coordinated specification")
    improvements: List[str] = Field(description="List of improvements made")
    coordination_time: float = Field(description="Time taken for coordination")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Coordination timestamp")
