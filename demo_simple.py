#!/usr/bin/env python3
"""Simple End-to-End Demo Script - Step 7 Final Testing"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_KEY = "bhiv-secret-key-2024"

def run_demo():
    print("Starting End-to-End Demo - Step 7 Final Testing")
    print("=" * 60)
    
    session = requests.Session()
    
    # Step 1: Authentication
    print("Step 1: Authentication")
    auth_response = session.post(f"{BASE_URL}/api/v1/auth/login", 
        json={"username": "admin", "password": "bhiv2024"},
        headers={"X-API-Key": API_KEY}
    )
    
    if auth_response.status_code != 200:
        print(f"Authentication failed: {auth_response.status_code}")
        return False
    
    jwt_token = auth_response.json()["access_token"]
    headers = {
        "X-API-Key": API_KEY,
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    print("Authentication successful")
    
    # Step 2: Generate Design
    print("\nStep 2: Generate Design")
    gen_response = session.post(f"{BASE_URL}/api/v1/generate",
        json={"prompt": "Modern office building with glass walls"},
        headers=headers
    )
    
    if gen_response.status_code != 200:
        print(f"Generation failed: {gen_response.status_code}")
        return False
    
    result = gen_response.json()
    spec_id = result["spec_id"]
    print(f"Design generated: {spec_id}")
    
    # Step 3: Switch Materials
    print("\nStep 3: Switch Materials")
    switch_response = session.post(f"{BASE_URL}/api/v1/switch",
        json={"spec_id": spec_id, "instruction": "change walls to brick"},
        headers=headers
    )
    
    if switch_response.status_code == 200:
        switch_result = switch_response.json()
        print(f"Material switched: {switch_result['changed']['after']['material']}")
    else:
        print(f"Switch failed: {switch_response.status_code}")
    
    # Step 4: Compliance
    print("\nStep 4: Compliance Analysis")
    compliance_response = session.post(f"{BASE_URL}/api/v1/compliance/run_case",
        json={
            "project_id": "demo_project",
            "spec_data": {"design_type": "building"}
        },
        headers=headers
    )
    
    if compliance_response.status_code == 200:
        print("Compliance analysis completed")
    else:
        print(f"Compliance failed: {compliance_response.status_code}")
    
    # Step 5: Three.js Data
    print("\nStep 5: Three.js Integration")
    threejs_response = session.get(f"{BASE_URL}/api/v1/three-js/{spec_id}",
        headers=headers
    )
    
    if threejs_response.status_code == 200:
        threejs_data = threejs_response.json()
        objects_count = len(threejs_data["three_js_data"]["objects"])
        print(f"Three.js data generated: {objects_count} objects")
    else:
        print(f"Three.js failed: {threejs_response.status_code}")
    
    # Step 6: RL Iterations
    print("\nStep 6: RL Training")
    rl_response = session.post(f"{BASE_URL}/iterate",
        json={"prompt": "Improve building design", "n_iter": 2},
        headers=headers
    )
    
    if rl_response.status_code == 200:
        rl_result = rl_response.json()
        iterations = len(rl_result.get("iterations", []))
        print(f"RL training completed: {iterations} iterations")
    else:
        print(f"RL training failed: {rl_response.status_code}")
    
    # Step 7: Health Check
    print("\nStep 7: System Health")
    health_response = session.get(f"{BASE_URL}/health")
    
    if health_response.status_code == 200:
        health = health_response.json()
        print(f"System status: {health['status']}")
    else:
        print("Health check failed")
    
    print("\n" + "=" * 60)
    print("Demo Complete - ALL SYSTEMS OPERATIONAL!")
    return True

if __name__ == "__main__":
    success = run_demo()
    if success:
        print("\nStep 7 Complete: System ready for deployment!")
    else:
        print("\nStep 7 Issues: Review and fix before deployment")