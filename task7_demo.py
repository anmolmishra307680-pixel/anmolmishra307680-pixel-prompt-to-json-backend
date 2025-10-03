#!/usr/bin/env python3
"""Task 7 Integration Demo"""

import requests
import json
import time

def main():
    base_url = "http://localhost:8000"
    headers = {
        "X-API-Key": "bhiv-secret-key-2024",
        "Content-Type": "application/json"
    }
    
    print("Task 7 Integration Demo")
    print("=" * 30)
    
    # Step 1: Get JWT token
    print("1. Getting JWT token...")
    token_response = requests.post(f"{base_url}/token", 
        headers=headers,
        json={"username": "admin", "password": "bhiv2024"})
    
    if token_response.status_code == 200:
        token = token_response.json()["access_token"]
        headers["Authorization"] = f"Bearer {token}"
        print("✅ Authentication successful")
    else:
        print("❌ Authentication failed")
        return
    
    # Step 2: Enhanced generate
    print("\n2. Testing enhanced generate...")
    gen_response = requests.post(f"{base_url}/api/v1/generate",
        headers=headers,
        json={
            "prompt": "Modern office building with glass facade",
            "style": "contemporary"
        })
    
    if gen_response.status_code == 200:
        gen_data = gen_response.json()
        spec_id = gen_data["spec_id"]
        print(f"✅ Generated spec: {spec_id}")
    else:
        print("❌ Generate failed")
        return
    
    # Step 3: Material switch
    print("\n3. Testing material switch...")
    switch_response = requests.post(f"{base_url}/api/v1/switch",
        headers=headers,
        json={
            "spec_id": spec_id,
            "instruction": "change floor to marble"
        })
    
    if switch_response.status_code == 200:
        switch_data = switch_response.json()
        print(f"✅ Switch successful: {switch_data['iteration_id']}")
    else:
        print("❌ Switch failed")
    
    # Step 4: Compliance check
    print("\n4. Testing compliance integration...")
    compliance_response = requests.post(f"{base_url}/api/v1/compliance/run_case",
        headers=headers,
        json={
            "spec_id": spec_id,
            "compliance_rules": ["fire_safety", "accessibility"]
        })
    
    if compliance_response.status_code == 200:
        compliance_data = compliance_response.json()
        print(f"✅ Compliance case: {compliance_data['case_id']}")
    else:
        print("❌ Compliance failed")
    
    print("\n🎉 Task 7 Integration Demo Complete!")

if __name__ == "__main__":
    main()