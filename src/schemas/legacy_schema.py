from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import uuid

class MaterialSpec(BaseModel):
    type: str = Field(description="Material type (steel, concrete, wood, etc.)")
    grade: Optional[str] = Field(default=None, description="Material grade or specification")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Material properties")

class DimensionSpec(BaseModel):
    length: Optional[float] = Field(default=None, description="Length in meters")
    width: Optional[float] = Field(default=None, description="Width in meters")
    height: Optional[float] = Field(default=None, description="Height in meters")
    area: Optional[float] = Field(default=None, description="Area in square meters")

class DesignSpec(BaseModel):
    building_type: str = Field(description="Type of building")
    stories: int = Field(description="Number of stories")
    materials: List[MaterialSpec] = Field(default_factory=list, description="Building materials")
    dimensions: DimensionSpec = Field(default_factory=DimensionSpec, description="Building dimensions")
    features: List[str] = Field(default_factory=list, description="Special features")
    requirements: List[str] = Field(default_factory=list, description="Design requirements")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Generation timestamp")

    @field_validator('stories')
    @classmethod
    def validate_stories(cls, v):
        return max(1, v)

    @field_validator('materials')
    @classmethod
    def validate_materials(cls, v):
        if not v:
            return [MaterialSpec(type="concrete")]
        return v

class EvaluationResult(BaseModel):
    score: float = Field(description="Overall evaluation score (0-100)")
    completeness: float = Field(description="Completeness score (0-100)")
    format_validity: float = Field(description="Format validity score (0-100)")
    feasibility: float = Field(default=85.0, description="Feasibility score (0-100)")
    feedback: List[str] = Field(default_factory=list, description="Feedback comments")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Evaluation timestamp")

    @field_validator('score', 'completeness', 'format_validity', 'feasibility')
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
