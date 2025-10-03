#!/usr/bin/env python3
"""Test script for Day 3 Orchestration & Compliance Pipes"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_compliance_proxy():
    """Test compliance proxy functionality"""
    print("Testing Compliance Proxy...")
    try:
        from src.services.compliance import proxy
        
        # Test proxy initialization
        assert proxy is not None, "Proxy not initialized"
        
        print("[OK] Compliance Proxy initialized")
    except Exception as e:
        print(f"[FAIL] Compliance Proxy failed: {e}")
        assert False, f"Compliance Proxy failed: {e}"

def test_geometry_storage():
    """Test geometry storage functionality"""
    print("Testing Geometry Storage...")
    try:
        from src.services.geometry_storage import geometry_storage
        
        # Test storing geometry
        case_id = "test-case-123"
        project_id = "test-project-456"
        mock_data = b"mock STL data"
        
        url = geometry_storage.store_geometry(case_id, project_id, mock_data, "stl")
        
        assert url == f"/geometry/{case_id}.stl", f"Wrong URL: {url}"
        
        print("[OK] Geometry Storage working")
    except Exception as e:
        print(f"[FAIL] Geometry Storage failed: {e}")
        assert False, f"Geometry Storage failed: {e}"

def test_database_compliance():
    """Test database compliance methods"""
    print("Testing Database Compliance...")
    try:
        from src.data.database import Database
        
        db = Database()
        
        # Test compliance case storage
        case_id = "test-case-db"
        project_id = "test-project-db"
        case_data = {"test": "data"}
        result = {"status": "passed"}
        
        saved_id = db.save_compliance_case(case_id, project_id, case_data, result)
        assert saved_id == case_id, f"Case ID mismatch: {saved_id}"
        
        print("[OK] Database Compliance working")
    except Exception as e:
        print(f"[FAIL] Database Compliance failed: {e}")
        assert False, f"Database Compliance failed: {e}"

def test_mock_pipeline():
    """Test mock pipeline without external services"""
    print("Testing Mock Pipeline...")
    try:
        from src.core.lm_adapter import LocalLMAdapter
        from src.services.geometry_storage import geometry_storage
        from src.data.database import Database
        
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
        
        # Validate
        assert spec_data is not None, "Spec not generated"
        assert geometry_url is not None, "Geometry not stored"
        
        print("[OK] Mock Pipeline working")
    except Exception as e:
        print(f"[FAIL] Mock Pipeline failed: {e}")
        assert False, f"Mock Pipeline failed: {e}"