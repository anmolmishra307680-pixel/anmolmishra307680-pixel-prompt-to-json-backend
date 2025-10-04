"""Test cases for Three.js frontend integration"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
import json

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

def test_three_js_data_generation():
    """Test Three.js data generation for spec"""
    headers = get_auth_headers()
    
    # Generate spec first
    response = client.post("/api/v1/generate", 
        json={"prompt": "modern office building with glass walls"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Get Three.js data
    response = client.get(f"/api/v1/three-js/{spec_id}", headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] == True
    assert "three_js_data" in result
    
    three_js_data = result["three_js_data"]
    assert "scene" in three_js_data
    assert "objects" in three_js_data
    assert "camera" in three_js_data
    assert "lights" in three_js_data

def test_three_js_object_structure():
    """Test Three.js object structure"""
    headers = get_auth_headers()
    
    # Generate spec with multiple objects
    response = client.post("/api/v1/generate", 
        json={"prompt": "building with walls, floor, and roof"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Get Three.js data
    response = client.get(f"/api/v1/three-js/{spec_id}", headers=headers)
    assert response.status_code == 200
    
    three_js_data = response.json()["three_js_data"]
    objects = three_js_data["objects"]
    
    # Check object structure
    for obj in objects:
        assert "id" in obj
        assert "type" in obj
        assert "geometry" in obj
        assert "material" in obj
        assert "position" in obj
        assert "editable" in obj

def test_react_three_fiber_code_generation():
    """Test React Three Fiber component code generation"""
    headers = get_auth_headers()
    
    # Generate spec
    response = client.post("/api/v1/generate", 
        json={"prompt": "simple building"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Get React Three Fiber code
    response = client.get(f"/api/v1/react-three-fiber/{spec_id}", headers=headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] == True
    assert "component_code" in result
    assert "dependencies" in result
    
    # Check dependencies
    dependencies = result["dependencies"]
    assert "@react-three/fiber" in dependencies
    assert "@react-three/drei" in dependencies
    assert "three" in dependencies

def test_preview_refresh_with_threejs():
    """Test preview refresh updates Three.js data"""
    headers = get_auth_headers()
    
    # Generate spec
    response = client.post("/api/v1/generate", 
        json={"prompt": "office building"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Switch material to trigger refresh
    response = client.post("/api/v1/switch", 
        json={"spec_id": spec_id, "instruction": "change walls to glass"},
        headers=headers
    )
    assert response.status_code == 200
    
    # Refresh preview and Three.js data
    response = client.post("/api/v1/preview/refresh", 
        json={"spec_id": spec_id},
        headers=headers
    )
    assert response.status_code == 200
    
    result = response.json()
    assert result["success"] == True
    assert "three_js_data" in result
    assert "preview_url" in result
    assert "refreshed_at" in result

def test_html_viewer_generation():
    """Test HTML viewer generation"""
    headers = get_auth_headers()
    
    # Generate spec
    response = client.post("/api/v1/generate", 
        json={"prompt": "modern building"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Get HTML viewer
    response = client.get(f"/api/v1/viewer/{spec_id}")
    assert response.status_code == 200
    
    # Check that HTML content is returned
    content = response.content.decode()
    assert "<!DOCTYPE html>" in content
    assert "three.min.js" in content
    assert spec_id in content

def test_three_js_material_colors():
    """Test material to color mapping in Three.js data"""
    headers = get_auth_headers()
    
    # Generate spec with specific materials
    response = client.post("/api/v1/generate", 
        json={"prompt": "building with wood floors and steel walls"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Get Three.js data
    response = client.get(f"/api/v1/three-js/{spec_id}", headers=headers)
    assert response.status_code == 200
    
    three_js_data = response.json()["three_js_data"]
    objects = three_js_data["objects"]
    
    # Check that materials have color mappings
    for obj in objects:
        material = obj["material"]
        assert "color" in material
        assert material["color"].startswith("#")  # Hex color format

def test_three_js_nonexistent_spec():
    """Test Three.js data for non-existent spec"""
    headers = get_auth_headers()
    
    response = client.get("/api/v1/three-js/nonexistent-spec", headers=headers)
    assert response.status_code == 404

def test_three_js_scene_configuration():
    """Test Three.js scene configuration"""
    headers = get_auth_headers()
    
    # Generate spec
    response = client.post("/api/v1/generate", 
        json={"prompt": "large office complex"},
        headers=headers
    )
    assert response.status_code == 200
    spec_id = response.json()["spec_id"]
    
    # Get Three.js data
    response = client.get(f"/api/v1/three-js/{spec_id}", headers=headers)
    assert response.status_code == 200
    
    three_js_data = response.json()["three_js_data"]
    
    # Check scene configuration
    scene = three_js_data["scene"]
    assert "background" in scene
    assert "fog" in scene
    
    # Check camera configuration
    camera = three_js_data["camera"]
    assert "position" in camera
    assert "fov" in camera
    
    # Check lighting
    lights = three_js_data["lights"]
    assert len(lights) > 0
    assert any(light["type"] == "ambient" for light in lights)
    assert any(light["type"] == "directional" for light in lights)

def test_three_js_without_auth():
    """Test Three.js endpoints without authentication"""
    response = client.get("/api/v1/three-js/test-spec")
    assert response.status_code == 401
    
    response = client.get("/api/v1/react-three-fiber/test-spec")
    assert response.status_code == 401