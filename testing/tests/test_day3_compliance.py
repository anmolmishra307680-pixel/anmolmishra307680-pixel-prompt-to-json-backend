#!/usr/bin/env python3
"""Test script for Day 3 Orchestration & Compliance Pipes"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_compliance_proxy():
    """Test compliance proxy functionality"""
    print("Testing Compliance Proxy...")
    try:
        from src.compliance.proxy import ComplianceProxy
        
        proxy = ComplianceProxy()
        
        # Test proxy initialization
        assert proxy.base_url is not None, "Base URL not set"
        assert proxy.timeout == 30.0, "Timeout not set correctly"
        
        print("[OK] Compliance Proxy initialized")
        print(f"   Base URL: {proxy.base_url}")
        print(f"   Timeout: {proxy.timeout}s")
        
        return True
    except Exception as e:
        print(f"[FAIL] Compliance Proxy failed: {e}")
        return False

def test_geometry_storage():
    """Test geometry storage functionality"""
    print("Testing Geometry Storage...")
    try:
        from src.geometry_storage import GeometryStorage
        
        storage = GeometryStorage()
        
        # Test storing geometry
        case_id = "test-case-123"
        project_id = "test-project-456"
        mock_data = b"mock STL data"
        
        url = storage.store_geometry(case_id, project_id, mock_data, "stl")
        
        assert url == f"/geometry/{case_id}.stl", f"Wrong URL: {url}"
        
        # Test retrieval
        retrieved_url = storage.get_geometry_url(case_id)
        assert retrieved_url == url, f"URL mismatch: {retrieved_url} != {url}"
        
        # Test project mapping
        mapped_project = storage.get_project_id(case_id)
        assert mapped_project == project_id, f"Project ID mismatch: {mapped_project}"
        
        print("[OK] Geometry Storage working")
        print(f"   Stored: {case_id} -> {url}")
        print(f"   Mapped: {case_id} -> {project_id}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Geometry Storage failed: {e}")
        return False

def test_database_compliance():
    """Test database compliance methods"""
    print("Testing Database Compliance...")
    try:
        from src.db.database import Database
        
        db = Database()
        
        # Test compliance case storage
        case_id = "test-case-db"
        project_id = "test-project-db"
        case_data = {"test": "data"}
        result = {"status": "passed"}
        
        saved_id = db.save_compliance_case(case_id, project_id, case_data, result)
        assert saved_id == case_id, f"Case ID mismatch: {saved_id}"
        
        # Test compliance feedback storage
        feedback_data = {"rating": 5}
        feedback_result = {"received": True}
        
        feedback_id = db.save_compliance_feedback(case_id, feedback_data, feedback_result)
        assert feedback_id is not None, "Feedback ID not returned"
        
        # Test pipeline result storage
        pipeline_id = "test-pipeline-123"
        pipeline_result = {"completed": True}
        
        saved_pipeline = db.save_pipeline_result(pipeline_id, pipeline_result)
        assert saved_pipeline == pipeline_id, f"Pipeline ID mismatch: {saved_pipeline}"
        
        print("[OK] Database Compliance working")
        print(f"   Case saved: {saved_id}")
        print(f"   Feedback saved: {feedback_id}")
        print(f"   Pipeline saved: {saved_pipeline}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Database Compliance failed: {e}")
        return False

def test_mock_pipeline():
    """Test mock pipeline without external services"""
    print("Testing Mock Pipeline...")
    try:
        from src.lm_adapter.lm_interface import LocalLMAdapter
        from src.geometry_storage import geometry_storage
        from src.db.database import db
        
        # Step 1: Generate spec
        adapter = LocalLMAdapter()
        spec_data = adapter.run("Test building for compliance")
        
        # Step 2: Mock compliance result
        case_id = "mock-pipeline-test"
        project_id = "mock-project-test"
        compliance_result = {
            "status": "passed",
            "score": 85,
            "violations": []
        }
        
        # Step 3: Store geometry
        geometry_url = geometry_storage.store_geometry(
            case_id, project_id, b"mock_geometry", "stl"
        )
        
        # Step 4: Save pipeline result
        pipeline_result = {
            "pipeline_id": case_id,
            "spec_data": spec_data,
            "compliance_result": compliance_result,
            "geometry_url": geometry_url,
            "status": "completed"
        }
        
        saved_pipeline = db.save_pipeline_result(case_id, pipeline_result)
        
        # Validate
        assert spec_data is not None, "Spec not generated"
        assert geometry_url is not None, "Geometry not stored"
        assert saved_pipeline == case_id, "Pipeline not saved"
        
        print("[OK] Mock Pipeline working")
        print(f"   Spec type: {spec_data.get('design_type')}")
        print(f"   Compliance score: {compliance_result['score']}")
        print(f"   Geometry URL: {geometry_url}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Mock Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Day 3: Orchestration & Compliance Pipes - Test Suite")
    print("=" * 60)
    
    tests = [
        test_compliance_proxy,
        test_geometry_storage,
        test_database_compliance,
        test_mock_pipeline
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Day 3 implementation is ready.")
        return True
    else:
        print("Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)