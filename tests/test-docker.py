#!/usr/bin/env python3
"""Test Docker container with proper authentication"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_KEY = "test-api-key"
USERNAME = "testuser"
PASSWORD = "testpass"

def test_docker_container():
    print("🐳 Testing Docker container...")
    
    # Wait for container to start
    print("⏳ Waiting for container startup...")
    time.sleep(3)
    
    try:
        # Step 1: Get JWT token
        print("1️⃣ Getting JWT token...")
        token_response = requests.post(
            f"{BASE_URL}/token",
            json={"username": USERNAME, "password": PASSWORD},
            timeout=10
        )
        
        if token_response.status_code != 200:
            print(f"❌ Token request failed: {token_response.status_code}")
            print(f"Response: {token_response.text}")
            return False
        
        token_data = token_response.json()
        token = token_data["access_token"]
        print(f"✅ Token obtained: {token[:20]}...")
        
        # Step 2: Test protected endpoint
        print("2️⃣ Testing health endpoint...")
        headers = {
            "X-API-Key": API_KEY,
            "Authorization": f"Bearer {token}"
        }
        
        health_response = requests.get(f"{BASE_URL}/health", headers=headers, timeout=10)
        
        if health_response.status_code != 200:
            print(f"❌ Health check failed: {health_response.status_code}")
            print(f"Response: {health_response.text}")
            return False
        
        health_data = health_response.json()
        print(f"✅ Health check passed: {health_data['status']}")
        
        # Step 3: Test generate endpoint
        print("3️⃣ Testing generate endpoint...")
        generate_response = requests.post(
            f"{BASE_URL}/generate",
            json={"prompt": "Test building"},
            headers=headers,
            timeout=30
        )
        
        if generate_response.status_code != 200:
            print(f"❌ Generate failed: {generate_response.status_code}")
            print(f"Response: {generate_response.text}")
            return False
        
        generate_data = generate_response.json()
        print(f"✅ Generate successful: {generate_data['success']}")
        
        # Step 4: Test metrics (public endpoint)
        print("4️⃣ Testing metrics endpoint...")
        metrics_response = requests.get(f"{BASE_URL}/metrics", timeout=10)
        
        if metrics_response.status_code != 200:
            print(f"❌ Metrics failed: {metrics_response.status_code}")
            return False
        
        print("✅ Metrics endpoint accessible")
        
        print("\n🎉 All Docker tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to container. Is it running?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timeout. Container may be starting up.")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_docker_container()
    exit(0 if success else 1)