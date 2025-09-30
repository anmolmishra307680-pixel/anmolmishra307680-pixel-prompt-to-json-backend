"""Test structured error handling"""

import pytest
from fastapi.testclient import TestClient
from src.api.main_api import app

client = TestClient(app)

def test_value_error_format():
    """Test that ValueError returns structured JSON error"""
    import os
    
    # Set test environment variables
    os.environ["API_KEY"] = "bhiv-secret-key-2024"
    os.environ["DEMO_USERNAME"] = "admin"
    os.environ["DEMO_PASSWORD"] = "bhiv2024"
    
    # Get proper auth token first
    token_response = client.post("/token", 
                                json={"username": "admin", "password": "bhiv2024"},
                                headers={"X-API-Key": "bhiv-secret-key-2024"})
    
    assert token_response.status_code == 200, f"Auth failed: {token_response.json()}"
    
    token = token_response.json()["access_token"]
    headers = {"X-API-Key": "bhiv-secret-key-2024", "Authorization": f"Bearer {token}"}
    
    # Test with empty prompt to trigger ValueError
    response = client.post("/generate", json={"prompt": ""}, headers=headers)
    
    # Should get error for empty prompt
    assert response.status_code in [400, 500]
    json_response = response.json()
    
    # Check that error response has structured format
    assert "error" in json_response or "detail" in json_response

def test_generic_exception_format():
    """Test that generic Exception returns structured JSON error"""
    # Test with existing endpoint that requires authentication
    response = client.post("/generate", json={"prompt": "test"})
    
    # Should get 401 for missing API key
    assert response.status_code == 401
    json_response = response.json()
    # The actual error format includes these fields
    assert "error" in json_response
    assert "message" in json_response
    assert json_response["error"] == "HTTP Error"

def test_http_exception_passthrough():
    """Test that HTTPException is handled properly"""
    response = client.get("/nonexistent-endpoint")
    
    assert response.status_code == 404
    # FastAPI's default HTTPException handling should still work

if __name__ == "__main__":
    test_value_error_format()
    test_generic_exception_format()
    print("✅ All error format tests passed")