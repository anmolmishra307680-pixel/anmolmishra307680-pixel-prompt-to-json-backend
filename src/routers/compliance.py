"""Compliance router for Soham's service integration"""

from fastapi import APIRouter, Depends, HTTPException
from src.auth import verify_api_key, verify_jwt_token
from src.data.database import Database
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import httpx
import os

router = APIRouter()

# Soham's service URLs
SOHAM_RUN_CASE_URL = os.getenv("SOHAM_RUN_CASE_URL", "https://soham-compliance.example.com/run_case")
SOHAM_FEEDBACK_URL = os.getenv("SOHAM_FEEDBACK_URL", "https://soham-compliance.example.com/feedback")

class ComplianceRequest(BaseModel):
    case_id: str
    project_id: str
    spec_data: Dict[str, Any]
    compliance_rules: List[str] = []
    parameters: Optional[Dict[str, Any]] = None

class ComplianceFeedbackRequest(BaseModel):
    case_id: str
    feedback_type: str
    feedback_data: Dict[str, Any]
    user_id: Optional[str] = None

def get_database():
    return Database()

async def store_geometry_file(case_id: str, geometry_url: str, db: Database) -> str:
    """Store geometry file and return local URL"""
    try:
        # Download geometry file
        async with httpx.AsyncClient() as client:
            response = await client.get(geometry_url)
            response.raise_for_status()
            
        # Save to local storage (mock BHIV bucket)
        from pathlib import Path
        geometry_dir = Path("geometry")
        geometry_dir.mkdir(exist_ok=True)
        
        # Determine file extension
        file_ext = "stl" if geometry_url.endswith(".stl") else "zip"
        local_path = geometry_dir / f"{case_id}.{file_ext}"
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        local_url = f"/geometry/{case_id}.{file_ext}"
        
        # Store in compliance_cases table
        await db.store_geometry_reference(case_id, geometry_url, local_url)
        
        return local_url
        
    except Exception as e:
        print(f"Geometry storage failed: {e}")
        return geometry_url  # Return original URL as fallback

@router.post("/compliance/run_case")
async def run_case(
    body: ComplianceRequest,
    api_key: str = Depends(verify_api_key),
    token: str = Depends(verify_jwt_token),
    db: Database = Depends(get_database)
):
    """Run compliance case via Soham's service"""
    try:
        # Call Soham's run_case endpoint
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(SOHAM_RUN_CASE_URL, json=body.dict())
            resp.raise_for_status()
            data = resp.json()
        
        # Store geometry if provided
        if "geometry_url" in data:
            local_geometry_url = await store_geometry_file(body.case_id, data["geometry_url"], db)
            data["local_geometry_url"] = local_geometry_url
        
        # Save compliance case to database
        await db.save_compliance_case(
            case_id=body.case_id,
            project_id=body.project_id,
            case_data=body.dict(),
            result=data
        )
        
        return {
            "success": True,
            "case_id": body.case_id,
            "result": data,
            "message": "Compliance case processed successfully"
        }
        
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Compliance service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.post("/compliance/feedback")
async def feedback(
    body: ComplianceFeedbackRequest,
    api_key: str = Depends(verify_api_key),
    token: str = Depends(verify_jwt_token),
    db: Database = Depends(get_database)
):
    """Send feedback to Soham's service"""
    try:
        # Call Soham's feedback endpoint
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(SOHAM_FEEDBACK_URL, json=body.dict())
            resp.raise_for_status()
            data = resp.json()
        
        # Save feedback to database
        await db.save_compliance_feedback(
            case_id=body.case_id,
            feedback_data=body.dict(),
            result=data
        )
        
        return {
            "success": True,
            "case_id": body.case_id,
            "result": data,
            "message": "Compliance feedback sent successfully"
        }
        
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Compliance service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")