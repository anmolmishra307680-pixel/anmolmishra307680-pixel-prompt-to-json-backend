"""Compliance API Request/Response Models"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional


class ComplianceRunCaseRequest(BaseModel):
    """Request model for /api/v1/compliance/run_case"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "case_id": "case-123",
            "project_id": "proj-456",
            "spec_data": {
                "design_type": "building",
                "materials": ["concrete", "steel"],
                "dimensions": {"height": 50, "width": 30}
            },
            "compliance_rules": ["fire_safety", "accessibility", "structural"]
        }
    })
    
    case_id: Optional[str] = Field(None, description="Unique case identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    spec_data: Dict[str, Any] = Field(..., description="Design specification data")
    compliance_rules: List[str] = Field(default=[], description="List of compliance rules to check")
    geometry_data: Optional[str] = Field(None, description="Base64 encoded geometry data")


class ComplianceRunCaseResponse(BaseModel):
    """Response model for /api/v1/compliance/run_case"""
    success: bool
    result: Dict[str, Any]


class ComplianceFeedbackRequest(BaseModel):
    """Request model for /api/v1/compliance/feedback"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "case_id": "case-123",
            "feedback_type": "approval",
            "rating": 4.5,
            "comments": "Design meets all compliance requirements",
            "user_id": "user-789",
            "compliance_issues": []
        }
    })
    
    case_id: str = Field(..., description="Case identifier for feedback")
    feedback_type: str = Field(..., description="Type of feedback (approval, rejection, modification)")
    rating: Optional[float] = Field(None, ge=1, le=5, description="Rating from 1-5")
    comments: Optional[str] = Field(None, description="Additional comments")
    user_id: Optional[str] = Field(None, description="User providing feedback")
    compliance_issues: Optional[List[str]] = Field(default=[], description="List of compliance issues found")


class ComplianceFeedbackResponse(BaseModel):
    """Response model for /api/v1/compliance/feedback"""
    success: bool
    result: Dict[str, Any]
    message: str
