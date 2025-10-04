"""Test cases for compliance pipeline functionality"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
import json
import uuid

client = TestClient(app)

# Test credentials
API_KEY = "bhiv-secret-key-2024"
JWT_TOKEN = None

def get_jwt_token():
    """Get JWT token for authentication"""
    global JWT_TOKEN
    if JWT_TOKEN:
        return JWT_TOKEN
    
    response = client.post("/api/v1/auth/login", 
        json={"username": "admin", "password": "bhiv2024"},
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 200
    JWT_TOKEN = response.json()["access_token"]
    return JWT_TOKEN

def get_auth_headers():
    """Get authentication headers"""
    token = get_jwt_token()
    return {
        "X-API-Key": API_KEY,
        "Authorization": f"Bearer {token}"
    }

def test_compliance_run_case():
    """Test compliance case execution"""
    headers = get_auth_headers()
    
    case_data = {
        "project_id": str(uuid.uuid4()),
        "spec_data": {
            "design_type": "building",
            "materials": [{"type": "concrete"}],
            "dimensions": {"length": 20, "width": 15, "height": 10}
        },
        "compliance_rules": ["fire_safety", "structural_integrity"]
    }
    
    response = client.post("/api/v1/compliance/run_case", json=case_data, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] == True
    assert "result" in result
    assert "case_id" in result["result"]

def test_compliance_run_case_with_case_id():
    """Test compliance case with predefined case_id"""
    headers = get_auth_headers()
    
    case_id = str(uuid.uuid4())
    case_data = {
        "case_id": case_id,
        "project_id": str(uuid.uuid4()),
        "spec_data": {
            "design_type": "building",
            "materials": [{"type": "steel"}]
        }
    }
    
    response = client.post("/api/v1/compliance/run_case", json=case_data, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["result"]["case_id"] == case_id

def test_compliance_feedback():
    """Test compliance feedback submission"""
    headers = get_auth_headers()
    
    # First run a compliance case
    case_data = {
        "project_id": str(uuid.uuid4()),
        "spec_data": {"design_type": "building"}
    }
    
    response = client.post("/api/v1/compliance/run_case", json=case_data, headers=headers)
    assert response.status_code == 200
    case_id = response.json()["result"]["case_id"]
    
    # Submit feedback
    feedback_data = {
        "case_id": case_id,
        "feedback_type": "accuracy",
        "rating": 4,
        "comments": "Good compliance analysis"
    }
    
    response = client.post("/api/v1/compliance/feedback", json=feedback_data, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] == True
    assert "message" in result

def test_compliance_geometry_storage():
    """Test geometry file storage in compliance"""
    headers = get_auth_headers()
    
    case_data = {
        "project_id": str(uuid.uuid4()),
        "spec_data": {
            "design_type": "building",
            "geometry_required": True
        }
    }
    
    response = client.post("/api/v1/compliance/run_case", json=case_data, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    # Check if geometry URL is provided when geometry data exists
    if "geometry_data" in result["result"]:
        assert "geometry_url" in result["result"]

def test_compliance_pipeline_end_to_end():
    """Test complete compliance pipeline"""
    headers = get_auth_headers()
    
    # Generate spec first
    response = client.post("/api/v1/generate", 
        json={"prompt": "commercial office building"},
        headers=headers
    )
    assert response.status_code == 200
    spec_data = response.json()["spec_json"]
    
    # Run compliance pipeline
    pipeline_data = {
        "spec_data": spec_data,
        "project_id": str(uuid.uuid4()),
        "compliance_rules": ["building_code", "accessibility"]
    }
    
    response = client.post("/api/v1/pipeline/run", json=pipeline_data, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] == True
    assert "pipeline_id" in result

def test_compliance_without_auth():
    """Test compliance endpoints without authentication"""
    case_data = {"project_id": "test"}
    
    response = client.post("/api/v1/compliance/run_case", json=case_data)
    assert response.status_code == 401
    
    feedback_data = {"case_id": "test", "rating": 5}
    response = client.post("/api/v1/compliance/feedback", json=feedback_data)
    assert response.status_code == 401

def test_compliance_invalid_data():
    """Test compliance with invalid data"""
    headers = get_auth_headers()
    
    # Missing required fields
    case_data = {}
    response = client.post("/api/v1/compliance/run_case", json=case_data, headers=headers)
    # Should return validation error for empty data
    assert response.status_code == 422

def test_geometry_file_retrieval():
    """Test geometry file retrieval"""
    headers = get_auth_headers()
    
    # Run compliance case that might generate geometry
    case_data = {
        "project_id": str(uuid.uuid4()),
        "spec_data": {"design_type": "building"}
    }
    
    response = client.post("/api/v1/compliance/run_case", json=case_data, headers=headers)
    assert response.status_code == 200
    
    case_id = response.json()["result"]["case_id"]
    
    # Try to retrieve geometry file
    response = client.get(f"/geometry/{case_id}")
    # Should return 404 if no geometry file exists, or 200 if it does
    assert response.status_code in [200, 404]

def test_compliance_database_storage():
    """Test that compliance results are stored in database"""
    headers = get_auth_headers()
    
    case_data = {
        "project_id": str(uuid.uuid4()),
        "spec_data": {
            "design_type": "building",
            "test_case": "database_storage"
        }
    }
    
    response = client.post("/api/v1/compliance/run_case", json=case_data, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    case_id = result["result"]["case_id"]
    
    # Verify case was processed
    assert result["success"] == True
    assert case_id is not None

def test_compliance_soham_integration():
    """Test Soham compliance service integration"""
    headers = get_auth_headers()
    
    # Test with realistic building data
    case_data = {
        "project_id": str(uuid.uuid4()),
        "spec_data": {
            "design_type": "building",
            "materials": [{"type": "concrete", "grade": "M25"}],
            "dimensions": {"length": 30, "width": 20, "height": 15},
            "occupancy": "commercial",
            "location": "urban"
        },
        "compliance_rules": [
            "fire_safety",
            "structural_integrity", 
            "accessibility",
            "energy_efficiency"
        ]
    }
    
    response = client.post("/api/v1/compliance/run_case", json=case_data, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] == True
    
    # Check for Soham-specific response fields
    compliance_result = result["result"]
    assert "case_id" in compliance_result
    assert "status" in compliance_result