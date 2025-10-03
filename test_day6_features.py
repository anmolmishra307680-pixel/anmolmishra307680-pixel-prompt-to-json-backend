#!/usr/bin/env python3
"""
Day 6 Features Test - Mobile/VR + Final Demo
Tests React Native integration, VR/AR functionality, and handover artifacts
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

class Day6Tester:
    def __init__(self):
        self.base_url = BASE_URL
        self.api_key = API_KEY
        self.jwt_token = None
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
    
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Remove Unicode characters for Windows compatibility
        clean_message = message.encode('ascii', 'ignore').decode('ascii')
        print(f"[{timestamp}] {status}: {clean_message}")
    
    def authenticate(self):
        """Get JWT token"""
        self.log("🔐 Authenticating for Day 6 tests...")
        
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
    
    def test_react_native_integration(self):
        """Test React Native bridge functionality"""
        self.log("📱 Testing React Native integration...")
        
        # Test mobile generate
        mobile_request = {
            "prompt": "Smart doorbell with camera and motion detection",
            "platform": "react-native",
            "device_info": {
                "os": "iOS",
                "version": "16.0",
                "device": "iPhone 14"
            },
            "optimize_for_mobile": True
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/mobile/generate",
            headers=self.headers,
            json=mobile_request
        )
        
        if response.status_code == 200:
            data = response.json()
            self.log("   ✅ Mobile generate successful")
            self.log(f"   📱 Mobile optimized: {data.get('mobile_optimized', False)}")
            
            # Test mobile preview
            preview_request = {
                "spec_id": "test_mobile_spec",
                "format": "base64",
                "size": "mobile"
            }
            
            preview_response = requests.post(
                f"{self.base_url}/api/v1/mobile/preview",
                headers=self.headers,
                json=preview_request
            )
            
            if preview_response.status_code == 200:
                preview_data = preview_response.json()
                has_base64 = "preview_base64" in preview_data.get("data", {})
                self.log(f"   ✅ Mobile preview: Base64 format: {has_base64}")
            else:
                self.log(f"   ⚠️ Mobile preview failed: {preview_response.status_code}")
            
            return True
        else:
            self.log(f"   ❌ Mobile generate failed: {response.status_code}", "ERROR")
            return False
    
    def test_vr_ar_functionality(self):
        """Test VR/AR bridge functionality"""
        self.log("🥽 Testing VR/AR functionality...")
        
        # Test VR generate
        vr_request = {
            "prompt": "Interactive office meeting room",
            "vr_platform": "oculus",
            "immersion_level": "full",
            "spatial_constraints": {
                "play_area_width": 4.0,
                "play_area_depth": 4.0,
                "ceiling_height": 3.0
            }
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/vr/generate",
            headers=self.headers,
            json=vr_request
        )
        
        if response.status_code == 200:
            data = response.json()
            self.log("   ✅ VR generation successful")
            
            vr_spec = data.get("data", {}).get("vr_spec", {})
            has_scene_objects = len(vr_spec.get("scene_objects", [])) > 0
            self.log(f"   🎮 Scene objects: {has_scene_objects}")
            
            # Test VR scene setup
            scene_request = {
                "spec_id": "test_vr_spec",
                "scene_type": "room_scale",
                "lighting": "natural",
                "environment": "studio"
            }
            
            scene_response = requests.post(
                f"{self.base_url}/api/v1/vr/scene",
                headers=self.headers,
                json=scene_request
            )
            
            if scene_response.status_code == 200:
                scene_data = scene_response.json()
                self.log("   ✅ VR scene setup successful")
            else:
                self.log(f"   ⚠️ VR scene setup failed: {scene_response.status_code}")
            
            return True
        else:
            self.log(f"   ❌ VR generation failed: {response.status_code}", "ERROR")
            return False
    
    def test_vr_platforms_support(self):
        """Test VR platforms and export functionality"""
        self.log("🎯 Testing VR platforms support...")
        
        # Test platforms endpoint
        response = requests.get(
            f"{self.base_url}/api/v1/vr/platforms",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            platforms = data.get("data", {})
            
            vr_headsets = len(platforms.get("vr_headsets", []))
            ar_devices = len(platforms.get("ar_devices", []))
            web_platforms = len(platforms.get("web_platforms", []))
            
            self.log(f"   ✅ VR headsets supported: {vr_headsets}")
            self.log(f"   ✅ AR devices supported: {ar_devices}")
            self.log(f"   ✅ Web platforms supported: {web_platforms}")
            
            # Test VR export
            export_response = requests.post(
                f"{self.base_url}/api/v1/vr/export?spec_id=test_spec&format=unity",
                headers=self.headers
            )
            
            if export_response.status_code == 200:
                export_data = export_response.json()
                self.log("   ✅ VR export (Unity) successful")
                
                # Test WebXR export
                webxr_response = requests.post(
                    f"{self.base_url}/api/v1/vr/export?spec_id=test_spec&format=webxr",
                    headers=self.headers
                )
                
                if webxr_response.status_code == 200:
                    self.log("   ✅ WebXR export successful")
                else:
                    self.log(f"   ⚠️ WebXR export failed: {webxr_response.status_code}")
            else:
                self.log(f"   ⚠️ VR export failed: {export_response.status_code}")
            
            return True
        else:
            self.log(f"   ❌ VR platforms failed: {response.status_code}", "ERROR")
            return False
    
    def test_full_demo_flow(self):
        """Test full demo across web + mobile + VR"""
        self.log("🎆 Testing full demo flow...")
        
        # Step 1: Web generation
        web_request = {"prompt": "Modern smart home with IoT integration"}
        web_response = requests.post(
            f"{self.base_url}/generate",
            headers=self.headers,
            json=web_request
        )
        
        web_success = web_response.status_code == 200
        self.log(f"   🌐 Web generation: {'✅' if web_success else '❌'}")
        
        # Step 2: Mobile generation
        mobile_request = {
            "prompt": "Compact smart home hub",
            "platform": "react-native",
            "optimize_for_mobile": True
        }
        mobile_response = requests.post(
            f"{self.base_url}/api/v1/mobile/generate",
            headers=self.headers,
            json=mobile_request
        )
        
        mobile_success = mobile_response.status_code == 200
        self.log(f"   📱 Mobile generation: {'✅' if mobile_success else '❌'}")
        
        # Step 3: VR generation
        vr_request = {
            "prompt": "Virtual smart home walkthrough",
            "vr_platform": "oculus",
            "immersion_level": "full"
        }
        vr_response = requests.post(
            f"{self.base_url}/api/v1/vr/generate",
            headers=self.headers,
            json=vr_request
        )
        
        vr_success = vr_response.status_code == 200
        self.log(f"   🥽 VR generation: {'✅' if vr_success else '❌'}")
        
        # Step 4: End-to-end demo
        demo_request = {"prompt": "Complete smart home ecosystem"}
        demo_response = requests.post(
            f"{self.base_url}/api/v1/demo/end-to-end",
            headers=self.headers,
            json=demo_request
        )
        
        demo_success = demo_response.status_code == 200
        self.log(f"   🎯 End-to-end demo: {'✅' if demo_success else '❌'}")
        
        if demo_success:
            demo_data = demo_response.json()
            demo_flow = demo_data.get("demo_flow", {})
            self.log(f"   📊 Demo steps completed: {len(demo_flow)}")
        
        all_success = web_success and mobile_success and vr_success and demo_success
        return all_success
    
    def test_handover_artifacts(self):
        """Test critical handover artifacts"""
        self.log("📋 Testing handover artifacts...")
        
        from pathlib import Path
        
        artifacts = {
            "API Contract v2": "docs/api_contract_v2_complete.md",
            "Demo Script": "demo_backend_integration.py",
            "Alembic Migration": "alembic/versions/0003_add_mobile_vr_tables.py",
            "Seed Data": "migrations/seed.py",
            "Auth Runbook": "config/handover/auth_runbook.md",
            "Compute Routing": "config/handover/compute_routing.md",
            "Security Checklist": "config/handover/security_checklist.md",
            "HIDG Logs": "reports/lead_log.txt"
        }
        
        missing_artifacts = []
        for name, path in artifacts.items():
            file_path = Path(path)
            if file_path.exists():
                self.log(f"   ✅ {name}: Found")
            else:
                self.log(f"   ❌ {name}: Missing ({path})")
                missing_artifacts.append(name)
        
        if not missing_artifacts:
            self.log("   🎉 All handover artifacts present!")
            return True
        else:
            self.log(f"   ⚠️ Missing artifacts: {len(missing_artifacts)}")
            return False
    
    def run_day6_tests(self):
        """Run all Day 6 tests"""
        self.log("🚀 Starting Day 6 Feature Tests")
        self.log("=" * 60)
        
        # Authentication
        if not self.authenticate():
            return False
        
        # Test results
        results = {
            "react_native": self.test_react_native_integration(),
            "vr_ar_functionality": self.test_vr_ar_functionality(),
            "vr_platforms": self.test_vr_platforms_support(),
            "full_demo": self.test_full_demo_flow(),
            "handover_artifacts": self.test_handover_artifacts()
        }
        
        # Summary
        self.log("=" * 60)
        self.log("📊 Day 6 Test Results:")
        
        passed = 0
        total = len(results)
        
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            self.log(f"   {test_name}: {status}")
            if success:
                passed += 1
        
        self.log(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 Day 6 - Mobile/VR + Final Demo: COMPLETE!")
            return True
        else:
            self.log("⚠️ Some Day 6 features need attention")
            return False

def main():
    """Main test execution"""
    print("Day 6 Features Test - Mobile/VR + Final Demo")
    print("=" * 60)
    
    tester = Day6Tester()
    
    try:
        success = tester.run_day6_tests()
        if success:
            print("\nAll Day 6 tests passed! Mobile/VR integration complete.")
            sys.exit(0)
        else:
            print("\nSome Day 6 tests failed. Check logs above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTests crashed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()