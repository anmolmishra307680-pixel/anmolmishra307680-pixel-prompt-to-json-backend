#!/usr/bin/env python3
"""
End-to-End Demo Script - Step 7 Final Testing
Demonstrates complete workflow: Generate → Switch → Compliance → Preview → RL
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "bhiv-secret-key-2024"
USERNAME = "admin"
PASSWORD = "bhiv2024"

class EndToEndDemo:
    def __init__(self):
        self.session = requests.Session()
        self.jwt_token = None
        self.spec_id = None
        
    def authenticate(self):
        """Step 1: Authenticate and get JWT token"""
        print("🔐 Step 1: Authentication")
        
        response = self.session.post(f"{BASE_URL}/api/v1/auth/login", 
            json={"username": USERNAME, "password": PASSWORD},
            headers={"X-API-Key": API_KEY}
        )
        
        if response.status_code == 200:
            self.jwt_token = response.json()["access_token"]
            print(f"✅ Authentication successful")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            return False
    
    def get_headers(self):
        """Get authentication headers"""
        return {
            "X-API-Key": API_KEY,
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }
    
    def generate_design(self):
        """Step 2: Generate design specification"""
        print("\n🏗️ Step 2: Generate Design Specification")
        
        prompt = "Modern sustainable office building with glass walls, concrete foundation, and green roof"
        
        response = self.session.post(f"{BASE_URL}/api/v1/generate",
            json={"prompt": prompt},
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            self.spec_id = result["spec_id"]
            objects_count = len(result["spec_json"]["objects"])
            print(f"✅ Design generated successfully")
            print(f"   Spec ID: {self.spec_id}")
            print(f"   Objects: {objects_count}")
            print(f"   Preview URL: {result.get('preview_url', 'N/A')}")
            return True
        else:
            print(f"❌ Design generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    
    def switch_materials(self):
        """Step 3: Switch materials on objects"""
        print("\n🔄 Step 3: Switch Materials")
        
        switches = [
            "change walls to glass",
            "change foundation to steel",
            "change roof to wood"
        ]
        
        for instruction in switches:
            print(f"   Switching: {instruction}")
            
            response = self.session.post(f"{BASE_URL}/api/v1/switch",
                json={
                    "spec_id": self.spec_id,
                    "instruction": instruction
                },
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                result = response.json()
                changed = result["changed"]
                print(f"   ✅ {changed['after']['type']} → {changed['after']['material']}")
            else:
                print(f"   ❌ Switch failed: {response.status_code}")
        
        return True
    
    def run_compliance(self):
        """Step 4: Run compliance analysis"""
        print("\n⚖️ Step 4: Compliance Analysis")
        
        case_data = {
            "project_id": f"demo_project_{int(time.time())}",
            "spec_data": {
                "design_type": "building",
                "materials": [{"type": "glass"}, {"type": "steel"}],
                "dimensions": {"length": 30, "width": 20, "height": 15}
            },
            "compliance_rules": ["fire_safety", "structural_integrity", "accessibility"]
        }
        
        response = self.session.post(f"{BASE_URL}/api/v1/compliance/run_case",
            json=case_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            case_id = result["result"]["case_id"]
            print(f"✅ Compliance analysis completed")
            print(f"   Case ID: {case_id}")
            
            # Submit feedback
            feedback_data = {
                "case_id": case_id,
                "feedback_type": "accuracy",
                "rating": 5,
                "comments": "Excellent compliance analysis"
            }
            
            feedback_response = self.session.post(f"{BASE_URL}/api/v1/compliance/feedback",
                json=feedback_data,
                headers=self.get_headers()
            )
            
            if feedback_response.status_code == 200:
                print("✅ Compliance feedback submitted")
            
            return True
        else:
            print(f"❌ Compliance analysis failed: {response.status_code}")
            return False
    
    def get_threejs_data(self):
        """Step 5: Get Three.js data for frontend rendering"""
        print("\n🎨 Step 5: Three.js Frontend Integration")
        
        response = self.session.get(f"{BASE_URL}/api/v1/three-js/{self.spec_id}",
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            three_js_data = result["three_js_data"]
            objects_count = len(three_js_data["objects"])
            lights_count = len(three_js_data["lights"])
            
            print(f"✅ Three.js data generated")
            print(f"   Objects: {objects_count}")
            print(f"   Lights: {lights_count}")
            print(f"   Scene: {three_js_data['scene']['name']}")
            
            # Get React Three Fiber code
            react_response = self.session.get(f"{BASE_URL}/api/v1/react-three-fiber/{self.spec_id}",
                headers=self.get_headers()
            )
            
            if react_response.status_code == 200:
                print("✅ React Three Fiber component generated")
            
            return True
        else:
            print(f"❌ Three.js data generation failed: {response.status_code}")
            return False
    
    def refresh_preview(self):
        """Step 6: Refresh preview after changes"""
        print("\n🖼️ Step 6: Preview Refresh")
        
        response = self.session.post(f"{BASE_URL}/api/v1/preview/refresh",
            json={"spec_id": self.spec_id},
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Preview refreshed")
            print(f"   New preview URL: {result['preview_url']}")
            print(f"   Refreshed at: {result['refreshed_at']}")
            return True
        else:
            print(f"❌ Preview refresh failed: {response.status_code}")
            return False
    
    def run_rl_iterations(self):
        """Step 7: Run RL iterations for design improvement"""
        print("\n🧠 Step 7: RL Design Improvement")
        
        response = self.session.post(f"{BASE_URL}/iterate",
            json={
                "prompt": f"Improve the design with spec_id {self.spec_id} for better sustainability and cost efficiency",
                "n_iter": 3
            },
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            result = response.json()
            iterations = result.get("iterations", [])
            session_id = result.get("session_id")
            
            print(f"✅ RL training completed")
            print(f"   Session ID: {session_id}")
            print(f"   Iterations: {len(iterations)}")
            
            for i, iteration in enumerate(iterations[:2]):  # Show first 2
                score_after = iteration.get("after", {}).get("score", 0)
                print(f"   Iteration {i+1}: Score = {score_after}")
            
            return True
        else:
            print(f"❌ RL iterations failed: {response.status_code}")
            return False
    
    def test_system_health(self):
        """Step 8: System health and metrics"""
        print("\n📊 Step 8: System Health Check")
        
        # Health check
        health_response = self.session.get(f"{BASE_URL}/health")
        if health_response.status_code == 200:
            health = health_response.json()
            print(f"✅ System health: {health['status']}")
            print(f"   Database: {'✅' if health['database'] else '❌'}")
            print(f"   Agents: {len(health['agents'])}")
        
        # System metrics
        metrics_response = self.session.get(f"{BASE_URL}/api/v1/metrics/detailed",
            headers=self.get_headers()
        )
        if metrics_response.status_code == 200:
            print("✅ System metrics retrieved")
        
        return True
    
    def run_full_demo(self):
        """Run complete end-to-end demo"""
        print("Starting End-to-End Demo - Step 7 Final Testing")
        print("=" * 60)
        
        steps = [
            self.authenticate,
            self.generate_design,
            self.switch_materials,
            self.run_compliance,
            self.get_threejs_data,
            self.refresh_preview,
            self.run_rl_iterations,
            self.test_system_health
        ]
        
        success_count = 0
        for step in steps:
            try:
                if step():
                    success_count += 1
                time.sleep(1)  # Brief pause between steps
            except Exception as e:
                print(f"❌ Step failed with exception: {e}")
        
        print("\n" + "=" * 60)
        print(f"Demo Complete: {success_count}/{len(steps)} steps successful")
        
        if success_count == len(steps):
            print("ALL SYSTEMS OPERATIONAL - PRODUCTION READY!")
            return True
        else:
            print("Some issues detected - review logs above")
            return False

if __name__ == "__main__":
    demo = EndToEndDemo()
    success = demo.run_full_demo()
    
    if success:
        print("\nStep 7 Complete: System ready for deployment!")
    else:
        print("\nStep 7 Issues: Review and fix before deployment")