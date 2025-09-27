"""Comprehensive endpoint testing for Render deployment with dual authentication"""

import requests
import json
from datetime import datetime

BASE_URL = "https://prompt-to-json-backend.onrender.com"
API_KEY = "bhiv-secret-key-2024"
USERNAME = "admin"
PASSWORD = "bhiv2024"

def get_jwt_token():
    """Get JWT token for authentication"""
    url = BASE_URL + "/token"
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"X-API-Key": API_KEY}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")

def auth_headers(token):
    """Headers with dual authentication"""
    return {
        "Authorization": f"Bearer {token}",
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

# GET endpoints to test
get_endpoints = [
    "/",
    "/agent-status",
    "/cache-stats", 
    "/metrics",
    "/system-test",
    "/system-overview"
]

# POST endpoints with valid payloads
post_endpoints = {
    "/generate": {"prompt": "Modern electric vehicle design"},
    "/evaluate": {
        "spec": {
            "design_type": "vehicle",
            "category": "vehicle",
            "materials": [{"type": "aluminum", "properties": {}}, {"type": "carbon_fiber", "properties": {}}],
            "dimensions": {"length": 4.5, "width": 1.8, "height": 1.4},
            "features": ["electric_motor", "autonomous_driving"],
            "performance_specs": {"range": 400, "top_speed": 200},
            "components": ["battery", "motor", "chassis"]
        },
        "prompt": "Electric sports car"
    },
    "/iterate": {"prompt": "Smart building design", "n_iter": 3},
    "/log-values": {
        "date": "2024-09-24",
        "day": "Tuesday", 
        "task": "Endpoint Testing",
        "values_reflection": {"testing": "comprehensive", "status": "production"}
    },
    "/batch-evaluate": ["Modern office building", "Electric car"],
    "/coordinated-improvement": {"prompt": "Sustainable architecture"},
    "/admin/prune-logs": {}
}

def test_get_endpoints(token):
    """Test all GET endpoints"""
    print("\n[GET] TESTING GET ENDPOINTS")
    print("=" * 40)
    
    for ep in get_endpoints:
        url = BASE_URL + ep
        try:
            resp = requests.get(url, headers=auth_headers(token), timeout=30)
            status = "[OK]" if resp.status_code == 200 else "[FAIL]"
            print(f"{status} GET {ep}: {resp.status_code}")
            if resp.status_code != 200:
                print(f"   Error: {resp.text[:100]}")
        except Exception as e:
            print(f"[FAIL] GET {ep} error: {str(e)[:100]}")

def test_post_endpoints(token):
    """Test all POST endpoints"""
    print("\n[POST] TESTING POST ENDPOINTS")
    print("=" * 40)
    
    for ep, payload in post_endpoints.items():
        url = BASE_URL + ep
        try:
            resp = requests.post(url, json=payload, headers=auth_headers(token), timeout=60)
            status = "[OK]" if resp.status_code == 200 else "[FAIL]"
            print(f"{status} POST {ep}: {resp.status_code}")
            if resp.status_code != 200:
                print(f"   Error: {resp.text[:100]}")
        except Exception as e:
            print(f"[FAIL] POST {ep} error: {str(e)[:100]}")

def test_health_endpoint():
    """Test public health endpoint"""
    print("\n[HEALTH] TESTING PUBLIC ENDPOINT")
    print("=" * 40)
    
    try:
        health_resp = requests.get(BASE_URL + "/health", timeout=10)
        status = "[OK]" if health_resp.status_code == 200 else "[FAIL]"
        print(f"{status} GET /health: {health_resp.status_code}")
        if health_resp.status_code == 200:
            health_data = health_resp.json()
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   Database: {health_data.get('database', 'unknown')}")
    except Exception as e:
        print(f"[FAIL] GET /health error: {str(e)[:100]}")

def main():
    """Run comprehensive endpoint testing"""
    print("COMPREHENSIVE ENDPOINT TESTING")
    print("=" * 50)
    print(f"Target: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test public health endpoint
    test_health_endpoint()
    
    # Get JWT token
    print("\n[AUTH] GETTING JWT TOKEN")
    print("=" * 40)
    try:
        token = get_jwt_token()
        print("[OK] JWT token obtained successfully")
    except Exception as e:
        print(f"[FAIL] Failed to get JWT token: {e}")
        return
    
    # Test secured endpoints
    test_get_endpoints(token)
    test_post_endpoints(token)
    
    print("\n[COMPLETE] TESTING FINISHED")
    print("=" * 50)
    print("All endpoints tested with dual authentication (API Key + JWT)")

if __name__ == "__main__":
    main()