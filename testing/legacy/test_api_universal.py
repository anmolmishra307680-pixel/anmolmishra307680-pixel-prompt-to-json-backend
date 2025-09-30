#!/usr/bin/env python3
"""Test API with universal design prompts"""

import requests
import json

def test_api_with_universal_prompts():
    """Test the API with different design types"""
    
    # API configuration
    base_url = "http://localhost:8000"
    api_key = "bhiv-secret-key-2024"
    username = "admin"
    password = "bhiv2024"
    
    # Get JWT token
    print("Getting JWT token...")
    token_response = requests.post(
        f"{base_url}/token",
        headers={"X-API-Key": api_key},
        json={"username": username, "password": password}
    )
    
    if token_response.status_code != 200:
        print(f"Failed to get token: {token_response.status_code}")
        return
    
    token = token_response.json()["access_token"]
    headers = {
        "X-API-Key": api_key,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test prompts for different design types
    test_prompts = [
        "Design a 2-story office building with steel and glass",
        "Create a luxury car with GPS and leather seats", 
        "Design a laptop with touchscreen and aluminum body",
        "Create a smart fridge with wifi control",
        "Design an ergonomic office chair with adjustable height"
    ]
    
    print(f"\nTesting {len(test_prompts)} different design prompts...")
    print("=" * 60)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Testing: '{prompt}'")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{base_url}/generate",
                headers=headers,
                json={"prompt": prompt}
            )
            
            if response.status_code == 200:
                data = response.json()
                spec = data["spec"]
                print(f"SUCCESS - Generated specification:")
                print(f"  Design Type: {spec.get('design_type', 'N/A')}")
                print(f"  Category: {spec.get('category', 'N/A')}")
                print(f"  Materials: {[m.get('type') for m in spec.get('materials', [])]}")
                print(f"  Features: {spec.get('features', [])[:3]}...")
                print(f"  Dimensions: {spec.get('dimensions', {})}")
            else:
                print(f"FAILED - Status: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    test_api_with_universal_prompts()