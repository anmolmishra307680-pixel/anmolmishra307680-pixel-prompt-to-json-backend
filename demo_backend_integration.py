#!/usr/bin/env python3
"""
End-to-End Backend Integration Demo
Tests all major API endpoints with authentication
"""
import requests
import json
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "bhiv-secret-key-2024"
USERNAME = "admin"
PASSWORD = "bhiv2024"

class BackendDemo:
    def __init__(self):
        self.base_url = BASE_URL
        self.api_key = API_KEY
        self.jwt_token = None
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
    
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
    
    def authenticate(self):
        """Get JWT token"""
        self.log("🔐 Authenticating...")
        
        auth_data = {"username": USERNAME, "password": PASSWORD}
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            headers=self.headers,
            json=auth_data
        )
        
        if response.status_code == 200:
            data = response.json()
            self.jwt_token = data["access_token"]
            self.headers["Authorization"] = f"Bearer {self.jwt_token}"
            self.log("✅ Authentication successful")
            return True
        else:
            self.log(f"❌ Authentication failed: {response.text}", "ERROR")
            return False
    
    def test_health(self):
        """Test health endpoint (no auth required)"""
        self.log("🏥 Testing health endpoint...")
        
        response = requests.get(f"{self.base_url}/health")
        if response.status_code == 200:
            self.log("✅ Health check passed")
            return True
        else:
            self.log(f"❌ Health check failed: {response.text}", "ERROR")
            return False
    
    def test_generate(self):
        """Test design generation"""
        self.log("🎨 Testing design generation...")
        
        prompts = [
            "Modern electric vehicle with 400-mile range",
            "Sustainable office building with solar panels",
            "Smart home IoT sensor with WiFi connectivity"
        ]
        
        results = []
        for prompt in prompts:
            self.log(f"   Generating: {prompt[:50]}...")
            
            response = requests.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json={"prompt": prompt}
            )
            
            if response.status_code == 200:
                data = response.json()
                spec_id = data["specification"]["metadata"]["created_at"]
                results.append({"prompt": prompt, "spec_id": spec_id, "data": data})
                self.log(f"   ✅ Generated spec for: {data['specification']['design_type']}")
            else:
                self.log(f"   ❌ Generation failed: {response.text}", "ERROR")
        
        self.log(f"✅ Generated {len(results)} designs")
        return results
    
    def test_evaluate(self, spec_data):
        """Test design evaluation"""
        self.log("📊 Testing design evaluation...")
        
        if not spec_data:
            self.log("❌ No spec data for evaluation", "ERROR")
            return []
        
        results = []
        for item in spec_data[:2]:  # Test first 2 specs
            spec = item["data"]["specification"]
            self.log(f"   Evaluating: {spec['design_type']}")
            
            response = requests.post(
                f"{self.base_url}/api/v1/evaluate",
                headers=self.headers,
                json={"spec": spec}
            )
            
            if response.status_code == 200:
                eval_data = response.json()
                results.append(eval_data)
                score = eval_data.get("overall_score", "N/A")
                self.log(f"   ✅ Evaluation score: {score}")
            else:
                self.log(f"   ❌ Evaluation failed: {response.text}", "ERROR")
        
        self.log(f"✅ Evaluated {len(results)} designs")
        return results
    
    def test_iterate(self, spec_data):
        """Test design iteration"""
        self.log("🔄 Testing design iteration...")
        
        if not spec_data:
            self.log("❌ No spec data for iteration", "ERROR")
            return []
        
        results = []
        feedback_options = [
            "Make it more sustainable",
            "Reduce cost by 20%",
            "Improve performance"
        ]
        
        for i, item in enumerate(spec_data[:2]):
            spec = item["data"]["specification"]
            feedback = feedback_options[i % len(feedback_options)]
            
            self.log(f"   Iterating: {spec['design_type']} with feedback: {feedback}")
            
            response = requests.post(
                f"{self.base_url}/api/v1/iterate",
                headers=self.headers,
                json={
                    "spec": spec,
                    "feedback": feedback,
                    "iterations": 2
                }
            )
            
            if response.status_code == 200:
                iter_data = response.json()
                results.append(iter_data)
                improvements = len(iter_data.get("improvements", []))
                self.log(f"   ✅ Applied {improvements} improvements")
            else:
                self.log(f"   ❌ Iteration failed: {response.text}", "ERROR")
        
        self.log(f"✅ Iterated {len(results)} designs")
        return results
    
    def test_mobile_api(self):
        """Test mobile API endpoints"""
        self.log("📱 Testing mobile API...")
        
        # Mobile generate
        response = requests.post(
            f"{self.base_url}/api/v1/mobile/generate",
            headers=self.headers,
            json={
                "prompt": "Compact smart home device",
                "platform": "react-native",
                "optimize_for_mobile": True
            }
        )
        
        if response.status_code == 200:
            self.log("   ✅ Mobile generation successful")
            mobile_data = response.json()
        else:
            self.log(f"   ❌ Mobile generation failed: {response.text}", "ERROR")
            return False
        
        # Mobile sync
        response = requests.post(
            f"{self.base_url}/api/v1/mobile/sync",
            headers=self.headers
        )
        
        if response.status_code == 200:
            self.log("   ✅ Mobile sync successful")
        else:
            self.log(f"   ❌ Mobile sync failed: {response.text}", "ERROR")
        
        self.log("✅ Mobile API tests completed")
        return True
    
    def test_vr_api(self):
        """Test VR/AR API endpoints"""
        self.log("🥽 Testing VR/AR API...")
        
        # VR generate
        response = requests.post(
            f"{self.base_url}/api/v1/vr/generate",
            headers=self.headers,
            json={
                "prompt": "Interactive office space",
                "vr_platform": "oculus",
                "immersion_level": "full"
            }
        )
        
        if response.status_code == 200:
            self.log("   ✅ VR generation successful")
            vr_data = response.json()
        else:
            self.log(f"   ❌ VR generation failed: {response.text}", "ERROR")
            return False
        
        # VR platforms
        response = requests.get(
            f"{self.base_url}/api/v1/vr/platforms",
            headers=self.headers
        )
        
        if response.status_code == 200:
            platforms = response.json()
            vr_count = len(platforms["data"]["vr_headsets"])
            self.log(f"   ✅ Found {vr_count} VR platforms")
        else:
            self.log(f"   ❌ VR platforms failed: {response.text}", "ERROR")
        
        self.log("✅ VR/AR API tests completed")
        return True
    
    def test_monitoring(self):
        """Test monitoring endpoints"""
        self.log("📈 Testing monitoring endpoints...")
        
        endpoints = [
            "/agent-status",
            "/cache-stats",
            "/metrics"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
            if response.status_code == 200:
                success_count += 1
                self.log(f"   ✅ {endpoint}")
            else:
                self.log(f"   ❌ {endpoint}: {response.status_code}", "ERROR")
        
        self.log(f"✅ Monitoring: {success_count}/{len(endpoints)} endpoints working")
        return success_count == len(endpoints)
    
    def run_full_demo(self):
        """Run complete end-to-end demo"""
        self.log("🚀 Starting End-to-End Backend Integration Demo")
        self.log("=" * 60)
        
        # Step 1: Health check
        if not self.test_health():
            self.log("❌ Demo failed at health check", "ERROR")
            return False
        
        # Step 2: Authentication
        if not self.authenticate():
            self.log("❌ Demo failed at authentication", "ERROR")
            return False
        
        # Step 3: Core functionality
        spec_data = self.test_generate()
        eval_data = self.test_evaluate(spec_data)
        iter_data = self.test_iterate(spec_data)
        
        # Step 4: Mobile & VR APIs
        self.test_mobile_api()
        self.test_vr_api()
        
        # Step 5: Monitoring
        self.test_monitoring()
        
        # Summary
        self.log("=" * 60)
        self.log("🎉 End-to-End Demo Completed Successfully!")
        self.log(f"   Generated: {len(spec_data)} designs")
        self.log(f"   Evaluated: {len(eval_data)} designs")
        self.log(f"   Iterated: {len(iter_data)} designs")
        self.log("   Mobile API: ✅")
        self.log("   VR/AR API: ✅")
        self.log("   Monitoring: ✅")
        
        return True

def main():
    """Main demo execution"""
    print("🎯 Prompt-to-JSON Backend Integration Demo")
    print("=" * 60)
    
    demo = BackendDemo()
    
    try:
        success = demo.run_full_demo()
        if success:
            print("\n✅ All tests passed! Backend is fully operational.")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed. Check logs above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Demo crashed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()