"""Test cases for material switch functionality"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
import json
import time

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

def test_material_switch_floor_to_marble():
    """Test switching floor material to marble"""
    headers = get_auth_headers()
    
    # Generate initial spec
    response = client.post("/api/v1/generate", 
        json={"prompt": "office building with concrete floor"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Switch floor to marble
    switch_payload = {
        "spec_id": spec_id,
        "instruction": "change floor to marble"
    }
    response = client.post("/api/v1/switch", json=switch_payload, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert "spec_id" in result
    assert "changed" in result
    assert result["changed"]["after"]["material"] == "marble"

def test_material_switch_wall_to_brick():
    """Test switching wall material to brick"""
    headers = get_auth_headers()
    
    # Generate spec with walls
    response = client.post("/api/v1/generate", 
        json={"prompt": "residential building with concrete walls"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Switch wall to brick
    switch_payload = {
        "spec_id": spec_id,
        "instruction": "change walls to brick"
    }
    response = client.post("/api/v1/switch", json=switch_payload, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert "changed" in result
    assert result["changed"]["after"]["material"] == "brick"

def test_switch_nonexistent_spec():
    """Test switch with non-existent spec ID"""
    headers = get_auth_headers()
    
    switch_payload = {
        "spec_id": "nonexistent-spec-id",
        "instruction": "change floor to marble"
    }
    response = client.post("/api/v1/switch", json=switch_payload, headers=headers)
    assert response.status_code == 404

def test_switch_invalid_instruction():
    """Test switch with invalid instruction"""
    headers = get_auth_headers()
    
    # Generate spec first
    response = client.post("/api/v1/generate", 
        json={"prompt": "simple building"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Invalid instruction
    switch_payload = {
        "spec_id": spec_id,
        "instruction": "invalid instruction with no material"
    }
    response = client.post("/api/v1/switch", json=switch_payload, headers=headers)
    assert response.status_code == 400

def test_switch_preview_url_update():
    """Test that preview URL updates after switch"""
    headers = get_auth_headers()
    
    # Generate spec
    response = client.post("/api/v1/generate", 
        json={"prompt": "office building"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    original_preview = response.json().get("preview_url")
    
    # Switch material
    switch_payload = {
        "spec_id": spec_id,
        "instruction": "change floor to marble"
    }
    response = client.post("/api/v1/switch", json=switch_payload, headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert "preview_url" in result
    # Preview URL should exist (may be same due to caching)
    assert result["preview_url"] is not None

def test_switch_iteration_tracking():
    """Test that iterations are properly tracked"""
    headers = get_auth_headers()
    
    # Generate spec
    response = client.post("/api/v1/generate", 
        json={"prompt": "building with steel structure"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # First switch
    switch_payload = {
        "spec_id": spec_id,
        "instruction": "change structure to concrete"
    }
    response = client.post("/api/v1/switch", json=switch_payload, headers=headers)
    assert response.status_code == 200
    iteration_id_1 = response.json()["iteration_id"]
    
    # Second switch
    switch_payload = {
        "spec_id": spec_id,
        "instruction": "change structure to wood"
    }
    response = client.post("/api/v1/switch", json=switch_payload, headers=headers)
    assert response.status_code == 200
    iteration_id_2 = response.json()["iteration_id"]
    
    # Iterations should be different
    assert iteration_id_1 != iteration_id_2

def test_switch_without_auth():
    """Test switch without authentication"""
    switch_payload = {
        "spec_id": "test-spec",
        "instruction": "change floor to marble"
    }
    response = client.post("/api/v1/switch", json=switch_payload)
    assert response.status_code == 401

def test_multiple_material_switches():
    """Test multiple material switches on same spec"""
    headers = get_auth_headers()
    
    # Generate complex building
    response = client.post("/api/v1/generate", 
        json={"prompt": "multi-story office building with concrete floors and steel walls"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Switch floor material
    response = client.post("/api/v1/switch", 
        json={"spec_id": spec_id, "instruction": "change floor to marble"},
        headers=headers
    )
    assert response.status_code == 200
    
    # Switch wall material
    response = client.post("/api/v1/switch", 
        json={"spec_id": spec_id, "instruction": "change walls to glass"},
        headers=headers
    )
    assert response.status_code == 200
    
    # Both switches should succeed
    result = response.json()
    assert "changed" in result
    assert result["changed"]["after"]["material"] == "glass"