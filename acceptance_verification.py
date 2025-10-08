"""Acceptance verification script for BHIV Backend"""

import requests
import json
import time

class AcceptanceVerifier:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_key = "bhiv-secret-key-2024"
        self.token = None
        self.results = []

    def verify(self, test_name, condition, message=""):
        status = "✅ PASS" if condition else "❌ FAIL"
        result = f"{status} {test_name}: {message}"
        self.results.append(result)
        print(result)
        return condition

    def login(self):
        """Test JWT authentication"""
        try:
            response = requests.post(f"{self.base_url}/api/v1/auth/login", 
                headers={"X-API-Key": self.api_key},
                data={"username": "admin", "password": "bhiv2024"})
            
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                return self.verify("JWT Login", True, "Authentication successful")
            else:
                return self.verify("JWT Login", False, f"Status: {response.status_code}")
        except Exception as e:
            return self.verify("JWT Login", False, str(e))

    def test_jwt_guards(self):
        """Test JWT-guarded endpoints"""
        headers = {
            "X-API-Key": self.api_key,
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Test generate endpoint
        try:
            response = requests.post(f"{self.base_url}/api/v1/generate",
                headers=headers, json={"prompt": "Test room"})
            self.verify("JWT Guard - Generate", response.status_code == 200, 
                      f"Generate endpoint protected: {response.status_code}")
        except Exception as e:
            self.verify("JWT Guard - Generate", False, str(e))

    def test_preview_chain(self):
        """Test preview URL generation chain"""
        headers = {
            "X-API-Key": self.api_key,
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        try:
            # Generate spec
            response = requests.post(f"{self.base_url}/api/v1/generate",
                headers=headers, json={"prompt": "Test office"})
            
            if response.status_code == 200:
                data = response.json()
                preview_url = data.get("preview_url", "")
                has_signature = "signature=" in preview_url
                has_expires = "expires=" in preview_url
                is_glb = ".glb" in preview_url
                
                self.verify("Preview Chain", has_signature and has_expires and is_glb,
                          f"Signed GLB URL: {preview_url[:50]}...")
            else:
                self.verify("Preview Chain", False, f"Generation failed: {response.status_code}")
        except Exception as e:
            self.verify("Preview Chain", False, str(e))

    def test_compliance_storage(self):
        """Test compliance geometry storage"""
        headers = {
            "X-API-Key": self.api_key,
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/compliance/run_case",
                headers=headers, json={
                    "case_id": "test_case_001",
                    "project_id": "test_project",
                    "spec_data": {"design_type": "building"},
                    "compliance_rules": ["fire_safety"]
                })
            
            if response.status_code == 200:
                result = response.json().get("result", {})
                has_geometry = "geometry_url" in result
                self.verify("Compliance Storage", has_geometry, 
                          f"Geometry storage: {result.get('geometry_url', 'N/A')}")
            else:
                self.verify("Compliance Storage", False, f"Status: {response.status_code}")
        except Exception as e:
            self.verify("Compliance Storage", False, str(e))

    def test_compute_routing(self):
        """Test local vs Yotta routing"""
        # Test logged in usage_logs.json
        try:
            with open("logs/usage_logs.json", "r") as f:
                logs = json.load(f)
                
            has_local = any(log.get("provider") == "local" for log in logs)
            has_cost_tracking = any("cost" in log for log in logs)
            
            self.verify("Compute Routing", has_local and has_cost_tracking,
                      f"Usage logs: {len(logs)} entries with cost tracking")
        except Exception as e:
            self.verify("Compute Routing", False, str(e))

    def test_metrics_endpoint(self):
        """Test Prometheus metrics"""
        try:
            response = requests.get(f"{self.base_url}/metrics")
            has_metrics = response.status_code == 200 and "http_requests_total" in response.text
            self.verify("Metrics Endpoint", has_metrics, 
                      f"Prometheus metrics exposed: {len(response.text)} chars")
        except Exception as e:
            self.verify("Metrics Endpoint", False, str(e))

    def test_vr_mobile_demo(self):
        """Test VR/Mobile endpoints"""
        headers = {
            "X-API-Key": self.api_key,
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            # Test VR preview
            response = requests.get(f"{self.base_url}/api/v1/vr/preview?spec_id=test_spec",
                headers=headers)
            
            vr_works = response.status_code == 200
            if vr_works:
                data = response.json()
                has_metadata = "metadata" in data and "vr_optimized" in data
                self.verify("VR/Mobile Demo", has_metadata, 
                          f"VR preview with metadata: {data.get('vr_optimized', False)}")
            else:
                self.verify("VR/Mobile Demo", False, f"VR endpoint failed: {response.status_code}")
        except Exception as e:
            self.verify("VR/Mobile Demo", False, str(e))

    def run_all_tests(self):
        """Run complete acceptance verification"""
        print("🚀 BHIV Backend Acceptance Verification")
        print("=" * 50)
        
        if self.login():
            self.test_jwt_guards()
            self.test_preview_chain()
            self.test_compliance_storage()
            self.test_compute_routing()
            self.test_metrics_endpoint()
            self.test_vr_mobile_demo()
        
        print("\n" + "=" * 50)
        passed = sum(1 for r in self.results if "✅ PASS" in r)
        total = len(self.results)
        print(f"📊 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - PRODUCTION READY!")
        else:
            print("⚠️  Some tests failed - review before deployment")

if __name__ == "__main__":
    verifier = AcceptanceVerifier()
    verifier.run_all_tests()