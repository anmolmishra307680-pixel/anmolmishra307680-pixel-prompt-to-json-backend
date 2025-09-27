"""Simple endpoint monitoring script for production"""

import requests
import json
from datetime import datetime

BASE_URL = "https://prompt-to-json-backend.onrender.com"
API_KEY = "bhiv-secret-key-2024"
USERNAME = "admin"
PASSWORD = "bhiv2024"

def test_core_endpoints():
    """Test core working endpoints"""
    print("PRODUCTION ENDPOINT MONITORING")
    print("=" * 40)
    print(f"Target: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {"passed": 0, "failed": 0, "total": 0}
    
    # Test 1: Health Check (Public)
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=10)
        status = "[OK]" if resp.status_code == 200 else "[FAIL]"
        print(f"{status} Health Check: {resp.status_code}")
        if resp.status_code == 200:
            results["passed"] += 1
            health_data = resp.json()
            print(f"   Database: {health_data.get('database', 'unknown')}")
        else:
            results["failed"] += 1
        results["total"] += 1
    except Exception as e:
        print(f"[FAIL] Health Check error: {str(e)[:50]}")
        results["failed"] += 1
        results["total"] += 1
    
    # Test 2: JWT Token Generation
    try:
        token_resp = requests.post(
            f"{BASE_URL}/token",
            json={"username": USERNAME, "password": PASSWORD},
            headers={"X-API-Key": API_KEY},
            timeout=10
        )
        status = "[OK]" if token_resp.status_code == 200 else "[FAIL]"
        print(f"{status} JWT Token: {token_resp.status_code}")
        if token_resp.status_code == 200:
            results["passed"] += 1
            token = token_resp.json().get("access_token")
        else:
            results["failed"] += 1
            return results
        results["total"] += 1
    except Exception as e:
        print(f"[FAIL] JWT Token error: {str(e)[:50]}")
        results["failed"] += 1
        results["total"] += 1
        return results
    
    # Test 3: Basic API Info (Protected)
    try:
        auth_headers = {
            "Authorization": f"Bearer {token}",
            "X-API-Key": API_KEY
        }
        resp = requests.get(f"{BASE_URL}/", headers=auth_headers, timeout=10)
        status = "[OK]" if resp.status_code == 200 else "[FAIL]"
        print(f"{status} API Info: {resp.status_code}")
        if resp.status_code == 200:
            results["passed"] += 1
        else:
            results["failed"] += 1
        results["total"] += 1
    except Exception as e:
        print(f"[FAIL] API Info error: {str(e)[:50]}")
        results["failed"] += 1
        results["total"] += 1
    
    # Test 4: Agent Status
    try:
        resp = requests.get(f"{BASE_URL}/agent-status", headers=auth_headers, timeout=15)
        status = "[OK]" if resp.status_code == 200 else "[FAIL]"
        print(f"{status} Agent Status: {resp.status_code}")
        if resp.status_code == 200:
            results["passed"] += 1
        else:
            results["failed"] += 1
        results["total"] += 1
    except Exception as e:
        print(f"[FAIL] Agent Status error: {str(e)[:50]}")
        results["failed"] += 1
        results["total"] += 1
    
    # Test 5: Cache Stats
    try:
        resp = requests.get(f"{BASE_URL}/cache-stats", headers=auth_headers, timeout=10)
        status = "[OK]" if resp.status_code == 200 else "[FAIL]"
        print(f"{status} Cache Stats: {resp.status_code}")
        if resp.status_code == 200:
            results["passed"] += 1
        else:
            results["failed"] += 1
        results["total"] += 1
    except Exception as e:
        print(f"[FAIL] Cache Stats error: {str(e)[:50]}")
        results["failed"] += 1
        results["total"] += 1
    
    # Summary
    print("\n" + "=" * 40)
    print(f"RESULTS: {results['passed']}/{results['total']} endpoints working")
    success_rate = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("Status: HEALTHY")
    elif success_rate >= 60:
        print("Status: DEGRADED")
    else:
        print("Status: CRITICAL")
    
    return results

if __name__ == "__main__":
    test_core_endpoints()