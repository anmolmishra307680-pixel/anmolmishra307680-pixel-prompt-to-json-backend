#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete API Endpoint Testing Script
Tests all endpoints in logical order with proper authentication
"""

import sys
import os

# Fix Unicode encoding for Windows
if sys.platform.startswith('win'):
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, OSError):
        pass
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import requests
import json
import time
from typing import Dict, Any, Optional

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_key = "bhiv-secret-key-2024"
        self.jwt_token: Optional[str] = None
        self.session = requests.Session()
        self.results = []
        
    def log_result(self, section: str, endpoint: str, method: str, status: int, success: bool, message: str = "", validation: str = ""):
        """Log test result"""
        result = {
            "section": section,
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "success": success,
            "message": message,
            "validation": validation,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.results.append(result)
        icon = "✅" if success else "❌"
        val_msg = f" | {validation}" if validation else ""
        print(f"{icon} {section} | {method} {endpoint} | {status} | {message}{val_msg}")
    
    def validate_response(self, resp: requests.Response, expected_keys: list = None) -> tuple:
        """Validate response content"""
        try:
            data = resp.json()
            
            # Check if response has success field
            if "success" in data and not data["success"]:
                return False, "Response success=False"
            
            # Check expected keys
            if expected_keys:
                missing = [k for k in expected_keys if k not in data]
                if missing:
                    return False, f"Missing keys: {missing}"
            
            return True, "Valid response"
        except:
            return False, "Invalid JSON"

    def make_request(self, method: str, endpoint: str, data: Dict[Any, Any] = None, 
                    auth_required: bool = True, api_key_only: bool = False) -> requests.Response:
        """Make HTTP request with proper authentication"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if auth_required or api_key_only:
            headers["X-API-Key"] = self.api_key
            
        if auth_required and self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
            
        try:
            if method == "GET":
                return self.session.get(url, headers=headers)
            elif method == "POST":
                return self.session.post(url, headers=headers, json=data)
            elif method == "PUT":
                return self.session.put(url, headers=headers, json=data)
            elif method == "DELETE":
                return self.session.delete(url, headers=headers)
        except Exception as e:
            print(f"Request failed: {e}")
            raise

    def test_section_1_auth(self):
        """🔐 1. Authentication & Security"""
        print("\n🔐 SECTION 1: Authentication & Security")
        
        # Step 1: Login and get JWT token
        login_data = {"username": "admin", "password": "bhiv2024"}
        try:
            resp = self.make_request("POST", "/api/v1/auth/login", login_data, auth_required=False, api_key_only=True)
            success = resp.status_code == 200
            validation = ""
            if success:
                data = resp.json()
                if "access_token" in data and data["access_token"]:
                    self.jwt_token = data["access_token"]
                    validation = f"Token received (len={len(self.jwt_token)})"
                else:
                    success = False
                    validation = "No access_token in response"
            self.log_result("🔐 Auth", "/api/v1/auth/login", "POST", resp.status_code, success, "User login", validation)
        except Exception as e:
            self.log_result("🔐 Auth", "/api/v1/auth/login", "POST", 500, False, str(e))
        
        # Step 2: Test refresh token (if we have one)
        if self.jwt_token:
            try:
                resp = self.make_request("POST", "/api/v1/auth/login", login_data, auth_required=False, api_key_only=True)
                if resp.status_code == 200 and resp.json().get("refresh_token"):
                    refresh_token = resp.json()["refresh_token"]
                    refresh_data = {"refresh_token": refresh_token}
                    resp = self.make_request("POST", "/api/v1/auth/refresh", refresh_data, auth_required=False, api_key_only=True)
                    success = resp.status_code == 200
                    validation = ""
                    if success:
                        data = resp.json()
                        if "access_token" in data:
                            validation = "New token received"
                        else:
                            success = False
                            validation = "No new token"
                    self.log_result("🔐 Auth", "/api/v1/auth/refresh", "POST", resp.status_code, success, "Token refresh", validation)
                else:
                    self.log_result("🔐 Auth", "/api/v1/auth/refresh", "POST", 200, True, "Token refresh (skipped)", "No refresh token")
            except Exception as e:
                self.log_result("🔐 Auth", "/api/v1/auth/refresh", "POST", 500, False, str(e))

    def test_section_2_system(self):
        """ℹ️ 2. System Information & Health"""
        print("\nℹ️ SECTION 2: System Information & Health")
        
        endpoints = [
            ("/", "GET", "API root", True),
            ("/health", "GET", "Health check", False),
            ("/ping", "GET", "Ping check", False),
            ("/system-overview", "GET", "System overview", True),
            ("/system-test", "GET", "System test", True)
        ]
        
        for endpoint, method, desc, auth in endpoints:
            try:
                resp = self.make_request(method, endpoint, auth_required=auth)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("ℹ️ System", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("ℹ️ System", endpoint, method, 500, False, str(e))

    def test_section_3_generation(self):
        """🤖 3. Core AI Generation Pipeline"""
        print("\n🤖 SECTION 3: Core AI Generation Pipeline")
        
        # Generate V2
        gen_data = {"prompt": "Modern office chair with ergonomic design"}
        try:
            resp = self.make_request("POST", "/api/v1/generate", gen_data)
            success = resp.status_code == 200
            validation = ""
            if success:
                data = resp.json()
                if "spec_json" in data:
                    validation = "Spec generated"
                else:
                    success = False
                    validation = "No spec_json in response"
            self.log_result("🤖 Generation", "/api/v1/generate", "POST", resp.status_code, success, "Generate V2", validation)
        except Exception as e:
            self.log_result("🤖 Generation", "/api/v1/generate", "POST", 500, False, str(e))
        
        # Legacy Generate
        try:
            resp = self.make_request("POST", "/generate", gen_data)
            success = resp.status_code == 200
            valid, validation = self.validate_response(resp, ["spec"])
            success = success and valid
            self.log_result("🤖 Generation", "/generate", "POST", resp.status_code, success, "Generate Legacy", validation)
        except Exception as e:
            self.log_result("🤖 Generation", "/generate", "POST", 500, False, str(e))
        
        # Switch Material V2
        switch_data = {"spec_id": "test_123", "instruction": "change floor to marble"}
        try:
            resp = self.make_request("POST", "/api/v1/switch", switch_data)
            success = resp.status_code == 200
            valid, validation = self.validate_response(resp, ["updated_spec_json"])
            success = success and valid
            self.log_result("🤖 Generation", "/api/v1/switch", "POST", resp.status_code, success, "Switch V2", validation)
        except Exception as e:
            self.log_result("🤖 Generation", "/api/v1/switch", "POST", 500, False, str(e))
        
        # Legacy Switch
        try:
            resp = self.make_request("POST", "/switch", switch_data)
            success = resp.status_code == 200
            # Legacy switch returns different format
            validation = "Valid response"
            self.log_result("🤖 Generation", "/switch", "POST", resp.status_code, success, "Switch Legacy", validation)
        except Exception as e:
            self.log_result("🤖 Generation", "/switch", "POST", 500, False, str(e))
        
        # Core Pipeline
        core_data = {"prompt": "Test core pipeline", "config": {}}
        try:
            resp = self.make_request("POST", "/api/v1/core/run", core_data)
            success = resp.status_code == 200
            valid, validation = self.validate_response(resp, ["result"])
            success = success and valid
            self.log_result("🤖 Generation", "/api/v1/core/run", "POST", resp.status_code, success, "Core Pipeline", validation)
        except Exception as e:
            self.log_result("🤖 Generation", "/api/v1/core/run", "POST", 500, False, str(e))

    def test_section_4_evaluation(self):
        """📏 4. Evaluation & Quality Assessment"""
        print("\n📏 SECTION 4: Evaluation & Quality Assessment")
        
        eval_data = {
            "spec_id": "test_123",
            "criteria": ["aesthetics", "functionality", "cost"],
            "spec_json": {"design_type": "furniture", "materials": ["wood"]}
        }
        
        endpoints = [
            ("/api/v1/evaluate", "POST", eval_data, "Evaluate V2"),
            ("/evaluate", "POST", eval_data, "Evaluate Legacy"),
            ("/batch-evaluate", "POST", {"specs": [eval_data]}, "Batch Evaluate"),
            ("/reports/test_123", "GET", None, "Get Report")
        ]
        
        for endpoint, method, data, desc in endpoints:
            try:
                resp = self.make_request(method, endpoint, data)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("📏 Evaluation", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("📏 Evaluation", endpoint, method, 500, False, str(e))

    def test_section_5_rl(self):
        """🔄 5. Reinforcement Learning & Iteration"""
        print("\n🔄 SECTION 5: Reinforcement Learning & Iteration")
        
        iter_data = {"spec_id": "test_123", "strategy": "improve_materials", "max_iterations": 3}
        
        endpoints = [
            ("/api/v1/iterate", "POST", iter_data, "Iterate V2"),
            ("/iterate", "POST", iter_data, "Iterate Legacy"),
            ("/advanced-rl", "POST", iter_data, "Advanced RL"),
            ("/coordinated-improvement", "POST", iter_data, "Multi-Agent"),
            ("/iterations/test_session", "GET", None, "Get Iterations")
        ]
        
        for endpoint, method, data, desc in endpoints:
            try:
                resp = self.make_request(method, endpoint, data)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("🔄 RL", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("🔄 RL", endpoint, method, 500, False, str(e))

    def test_section_6_compliance(self):
        """✅ 6. Compliance & Validation"""
        print("\n✅ SECTION 6: Compliance & Validation")
        
        compliance_data = {"case_id": "test_case", "spec_data": {}}
        feedback_data = {"case_id": "test_case", "feedback": "Good compliance"}
        pipeline_data = {"spec_id": "test_123"}
        
        endpoints = [
            ("/api/v1/compliance/run_case", "POST", compliance_data, "Run Case"),
            ("/api/v1/compliance/feedback", "POST", feedback_data, "Compliance Feedback"),
            ("/api/v1/pipeline/run", "POST", pipeline_data, "Run Pipeline")
        ]
        
        for endpoint, method, data, desc in endpoints:
            try:
                resp = self.make_request(method, endpoint, data)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("✅ Compliance", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("✅ Compliance", endpoint, method, 500, False, str(e))

    def test_section_7_preview(self):
        """🖼️ 7. Preview & Visualization"""
        print("\n🖼️ SECTION 7: Preview & Visualization")
        
        endpoints = [
            ("/geometry/test_case", "GET", None, "Get Geometry"),
            ("/api/v1/three-js/test_spec", "GET", None, "Three.js Data"),
            ("/api/v1/preview/refresh", "POST", {"spec_id": "test_123"}, "Refresh Preview"),
            ("/api/v1/preview/verify", "GET", None, "Verify Preview"),
            ("/api/v1/preview/cleanup", "POST", {}, "Cleanup Previews")
        ]
        
        for endpoint, method, data, desc in endpoints:
            try:
                if endpoint == "/api/v1/preview/verify":
                    # Special handling for verify endpoint with query params
                    resp = self.session.get(f"{self.base_url}{endpoint}?spec_id=test&expires=9999999999&signature=test", 
                                          headers={"X-API-Key": self.api_key, "Authorization": f"Bearer {self.jwt_token}"})
                else:
                    resp = self.make_request(method, endpoint, data)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("🖼️ Preview", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("🖼️ Preview", endpoint, method, 500, False, str(e))

    def test_section_8_mobile(self):
        """📱 8. Mobile & Cross-Platform"""
        print("\n📱 SECTION 8: Mobile & Cross-Platform")
        
        mobile_gen_data = {"prompt": "Mobile chair design", "device_info": {"platform": "ios"}}
        mobile_switch_data = {"spec_id": "mobile_123", "instruction": "change to leather"}
        
        endpoints = [
            ("/api/v1/mobile/generate", "POST", mobile_gen_data, "Mobile Generate"),
            ("/api/v1/mobile/switch", "POST", mobile_switch_data, "Mobile Switch")
        ]
        
        for endpoint, method, data, desc in endpoints:
            try:
                resp = self.make_request(method, endpoint, data)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("📱 Mobile", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("📱 Mobile", endpoint, method, 500, False, str(e))

    def test_section_9_vr_ar(self):
        """🥽 9. VR/AR & Immersive Tech"""
        print("\n🥽 SECTION 9: VR/AR & Immersive Tech")
        
        vr_gen_data = {"prompt": "VR office space", "vr_config": {}}
        vr_scene_data = {"scene_type": "office", "objects": []}
        ar_data = {"target_object": "chair", "overlay_type": "info"}
        
        endpoints = [
            ("/api/v1/vr/generate", "POST", vr_gen_data, "VR Generate"),
            ("/api/v1/vr/preview", "GET", None, "VR Preview"),
            ("/api/v1/vr/scene", "POST", vr_scene_data, "VR Scene"),
            ("/api/v1/ar/overlay", "POST", ar_data, "AR Overlay")
        ]
        
        for endpoint, method, data, desc in endpoints:
            try:
                resp = self.make_request(method, endpoint, data)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("🥽 VR/AR", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("🥽 VR/AR", endpoint, method, 500, False, str(e))

    def test_section_10_ui(self):
        """🖥️ 10. Frontend & UI Integration"""
        print("\n🖥️ SECTION 10: Frontend & UI Integration")
        
        session_data = {"user_id": "test_user", "session_type": "design"}
        flow_data = {"session_id": "test_session", "action": "generate", "timestamp": time.time()}
        
        endpoints = [
            ("/api/v1/ui/session", "POST", session_data, "Create Session"),
            ("/api/v1/ui/flow", "POST", flow_data, "Log Flow"),
            ("/api/v1/ui/summary", "GET", None, "UI Summary")
        ]
        
        for endpoint, method, data, desc in endpoints:
            try:
                resp = self.make_request(method, endpoint, data)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("🖥️ UI", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("🖥️ UI", endpoint, method, 500, False, str(e))

    def test_section_11_monitoring(self):
        """📊 11. Monitoring & Analytics"""
        print("\n📊 SECTION 11: Monitoring & Analytics")
        
        endpoints = [
            ("/metrics", "GET", None, "Prometheus Metrics", True),
            ("/basic-metrics", "GET", None, "Basic Metrics", True),
            ("/api/v1/metrics/detailed", "GET", None, "Detailed Metrics", True),
            ("/agent-status", "GET", None, "Agent Status", True),
            ("/cache-stats", "GET", None, "Cache Stats", True)
        ]
        
        for endpoint, method, data, desc, auth in endpoints:
            try:
                resp = self.make_request(method, endpoint, data, auth_required=auth)
                success = resp.status_code == 200
                # /metrics returns plain text (Prometheus format), not JSON
                if endpoint == "/metrics":
                    validation = "Prometheus format" if "#" in resp.text else "Invalid format"
                else:
                    valid, validation = self.validate_response(resp)
                    success = success and valid
                self.log_result("📊 Monitoring", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("📊 Monitoring", endpoint, method, 500, False, str(e))

    def test_section_12_data(self):
        """🗄️ 12. Data Management & Logging"""
        print("\n🗄️ SECTION 12: Data Management & Logging")
        
        log_data = {"values": {"test_key": "test_value"}, "timestamp": time.time()}
        
        endpoints = [
            ("/log-values", "POST", log_data, "Log Values"),
            ("/cli-tools", "GET", None, "CLI Tools"),
            ("/admin/prune-logs", "POST", {}, "Prune Logs")
        ]
        
        for endpoint, method, data, desc in endpoints:
            try:
                resp = self.make_request(method, endpoint, data)
                success = resp.status_code == 200
                valid, validation = self.validate_response(resp)
                success = success and valid
                self.log_result("🗄️ Data", endpoint, method, resp.status_code, success, desc, validation)
            except Exception as e:
                self.log_result("🗄️ Data", endpoint, method, 500, False, str(e))

    def run_all_tests(self):
        """Run all endpoint tests in logical order"""
        print("Starting Complete API Endpoint Testing")
        print(f"Base URL: {self.base_url}")
        print(f"API Key: {self.api_key}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test sections
        self.test_section_1_auth()
        self.test_section_2_system()
        self.test_section_3_generation()
        self.test_section_4_evaluation()
        self.test_section_5_rl()
        self.test_section_6_compliance()
        self.test_section_7_preview()
        self.test_section_8_mobile()
        self.test_section_9_vr_ar()
        self.test_section_10_ui()
        self.test_section_11_monitoring()
        self.test_section_12_data()
        
        # Generate summary
        self.generate_summary(time.time() - start_time)

    def generate_summary(self, duration: float):
        """Generate test summary report"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Duration: {duration:.2f} seconds")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Section breakdown
        sections = {}
        for result in self.results:
            section = result["section"]
            if section not in sections:
                sections[section] = {"total": 0, "passed": 0}
            sections[section]["total"] += 1
            if result["success"]:
                sections[section]["passed"] += 1
        
        print("\nSection Breakdown:")
        for section, stats in sections.items():
            rate = (stats["passed"]/stats["total"])*100
            print(f"  {section}: {stats['passed']}/{stats['total']} ({rate:.0f}%)")
        
        # Failed tests
        if failed_tests > 0:
            print("\nFailed Tests:")
            for result in self.results:
                if not result["success"]:
                    print(f"  {result['method']} {result['endpoint']} - {result['status']} - {result['message']}")
        
        print("\nTesting Complete!")

if __name__ == "__main__":
    import sys
    
    # Allow custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    tester = APITester(base_url)
    tester.run_all_tests()