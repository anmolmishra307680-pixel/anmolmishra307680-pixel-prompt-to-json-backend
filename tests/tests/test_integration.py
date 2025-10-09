import pytest
import os
import requests
from fastapi.testclient import TestClient
from src.main import app

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
        # Use new auth endpoint
        token_response = client.post("/api/v1/auth/login", 
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

class TestFullWorkflow:
    def test_complete_user_journey(self):
        """Test: Generate → Evaluate → Iterate → Report"""
        headers = get_auth_headers()
        
        # Step 1: Generate specification
        generate_response = client.post(
            "/generate",
            json={"prompt": "Sustainable office building"},
            headers=headers
        )
        assert generate_response.status_code == 200
        spec = generate_response.json()["spec"]
        
        # Step 2: Evaluate specification  
        eval_response = client.post(
            "/evaluate",
            json={"spec": spec, "prompt": "Sustainable office building"},
            headers=headers
        )
        assert eval_response.status_code == 200
        report_id = eval_response.json()["report_id"]
        
        # Step 3: RL iteration
        rl_response = client.post(
            "/iterate", 
            json={"prompt": "Sustainable office building", "n_iter": 2},
            headers=headers
        )
        assert rl_response.status_code == 200
        session_id = rl_response.json()["session_id"]
        
        # Step 4: Retrieve reports
        report_response = client.get(f"/reports/{report_id}", headers=headers)
        assert report_response.status_code == 200
        
        iteration_response = client.get(f"/iterations/{session_id}", headers=headers)
        assert iteration_response.status_code == 200

    def test_batch_processing_workflow(self):
        """Test batch evaluation functionality"""
        headers = get_auth_headers()
        
        prompts = ["Office building", "Warehouse facility", "Residential complex"]
        
        response = client.post("/batch-evaluate", json=prompts, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] == True
        assert data["count"] == 3
        assert len(data["results"]) == 3

    def test_health_and_metrics_endpoints(self):
        """Test monitoring endpoints"""
        headers = get_auth_headers()
        
        # Health check (now requires dual auth)
        health_response = client.get("/health", headers=headers)
        assert health_response.status_code == 200
        assert "status" in health_response.json()
        
        # Metrics (requires dual auth)
        metrics_response = client.get("/metrics", headers=headers)
        assert metrics_response.status_code == 200

    def test_authentication_workflow(self):
        """Test API key authentication"""
        # Without API key - should fail
        no_auth_response = client.post(
            "/generate",
            json={"prompt": "Test building"}
        )
        assert no_auth_response.status_code == 401
        
        # With wrong API key - should fail
        wrong_auth_response = client.post(
            "/generate",
            json={"prompt": "Test building"},
            headers={"X-API-Key": "wrong-key"}
        )
        assert wrong_auth_response.status_code == 401
        
        # With correct API key and JWT token - should succeed
        headers = get_auth_headers()
        correct_auth_response = client.post(
            "/generate",
            json={"prompt": "Test building"},
            headers=headers
        )
        assert correct_auth_response.status_code == 200