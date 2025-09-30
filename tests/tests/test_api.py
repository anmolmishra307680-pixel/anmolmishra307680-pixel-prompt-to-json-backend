# tests/test_api.py
import pytest
import os
from fastapi.testclient import TestClient
from src.api.main_api import app

client = TestClient(app)

# Set test environment variables
os.environ["API_KEY"] = "bhiv-secret-key-2024"
os.environ["DEMO_USERNAME"] = "admin"
os.environ["DEMO_PASSWORD"] = "bhiv2024"

# Use environment variables
API_KEY = "bhiv-secret-key-2024"
USERNAME = "admin"
PASSWORD = "bhiv2024"

# Global token cache to avoid rate limiting
_cached_token = None

def get_auth_headers():
    """Get JWT token and return headers with API key and token"""
    global _cached_token
    if _cached_token:
        return {
            "X-API-Key": API_KEY,
            "Authorization": f"Bearer {_cached_token}"
        }
    
    try:
        # Token endpoint now requires API key
        token_response = client.post("/token", 
                                   json={"username": USERNAME, "password": PASSWORD},
                                   headers={"X-API-Key": API_KEY})
        if token_response.status_code == 200:
            _cached_token = token_response.json()["access_token"]
            return {
                "X-API-Key": API_KEY,
                "Authorization": f"Bearer {_cached_token}"
            }
    except Exception:
        pass
    return {"X-API-Key": API_KEY}

def test_health():
    headers = get_auth_headers()
    r = client.get("/health", headers=headers)
    assert r.status_code == 200
    assert "status" in r.json()

def test_generate_missing_prompt():
    headers = get_auth_headers()
    r = client.post("/generate", json={}, headers=headers)
    assert r.status_code == 422  # Missing prompt field

def test_generate_valid_prompt():
    headers = get_auth_headers()
    r = client.post("/generate", json={"prompt": "Modern office building"}, headers=headers)
    assert r.status_code == 200
    assert "spec" in r.json()

def test_evaluate_missing_spec():
    headers = get_auth_headers()
    r = client.post("/evaluate", json={}, headers=headers)
    assert r.status_code == 422  # Missing required fields

def test_generate_no_auth():
    # Test without any authentication
    r = client.post("/generate", json={"prompt": "test"})
    assert r.status_code == 401  # No API key

def test_evaluate_no_auth():
    # Test without any authentication
    r = client.post("/evaluate", json={})
    assert r.status_code == 401  # No API key