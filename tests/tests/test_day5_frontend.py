#!/usr/bin/env python3
"""Test script for Day 5 Frontend + Preview Integration"""

import sys
import os
import asyncio
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_preview_manager():
    """Test preview management with signed URLs"""
    print("Testing Preview Manager...")
    try:
        from src.preview_manager import PreviewManager
        
        manager = PreviewManager()
        
        # Test signature generation
        spec_id = "test-spec-123"
        expires = int(time.time() + 3600)
        signature = manager._generate_signature(spec_id, expires)
        
        assert signature is not None, "Signature not generated"
        assert len(signature) == 64, f"Wrong signature length: {len(signature)}"
        
        # Test signature validation
        is_valid = manager._is_signature_valid(spec_id, expires, signature)
        assert is_valid, "Signature validation failed"
        
        # Test invalid signature
        invalid_signature = "invalid_signature"
        is_invalid = manager._is_signature_valid(spec_id, expires, invalid_signature)
        assert not is_invalid, "Invalid signature accepted"
        
        # Test expired signature
        expired_time = int(time.time() - 3600)
        is_expired = manager.verify_preview_url(spec_id, expired_time, signature)
        assert not is_expired, "Expired signature accepted"
        
        print("[OK] Preview Manager working")
        print(f"   Signature length: {len(signature)} chars")
        print(f"   Valid signature: {is_valid}")
        print(f"   Expired check: {not is_expired}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Preview Manager failed: {e}")
        return False

async def test_preview_generation():
    """Test preview generation with signed URLs"""
    print("Testing Preview Generation...")
    try:
        from src.preview_manager import preview_manager
        
        # Test spec data
        spec_data = {
            'spec_id': 'test-preview-123',
            'objects': [
                {'id': 'obj1', 'type': 'floor', 'material': 'wood'},
                {'id': 'obj2', 'type': 'wall', 'material': 'concrete'}
            ]
        }
        
        # Generate preview
        preview_url = await preview_manager.generate_preview(spec_data)
        
        assert preview_url is not None, "Preview URL not generated"
        assert 'signature=' in preview_url, "URL not signed"
        assert 'expires=' in preview_url, "URL missing expiry"
        
        # Test cache hit
        cached_url = await preview_manager.generate_preview(spec_data)
        assert cached_url == preview_url, "Cache not working"
        
        # Test refresh
        refreshed_url = await preview_manager.refresh_preview('test-preview-123', spec_data)
        assert refreshed_url != preview_url, "Refresh not working"
        
        print("[OK] Preview Generation working")
        print(f"   Preview URL: {preview_url[:50]}...")
        print(f"   Cached: {cached_url == preview_url}")
        print(f"   Refreshed: {refreshed_url != preview_url}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Preview Generation failed: {e}")
        return False

def test_frontend_integration():
    """Test frontend integration utilities"""
    print("Testing Frontend Integration...")
    try:
        from src.frontend_integration import FrontendIntegration
        
        integration = FrontendIntegration()
        
        # Test UI session creation
        session_id = "test-session-123"
        user_data = {"user": "test_user", "browser": "chrome"}
        
        session = integration.create_ui_session(session_id, user_data)
        
        assert session['session_id'] == session_id, "Session ID mismatch"
        assert session['user_data'] == user_data, "User data mismatch"
        
        # Test flow logging
        integration.log_ui_flow(session_id, "generate", {"prompt": "test building"})
        integration.log_ui_flow(session_id, "switch", {"instruction": "change floor to marble"})
        
        # Test summary
        summary = integration.get_ui_test_summary()
        
        assert summary['total_flows'] >= 2, "Flows not logged"
        assert summary['active_sessions'] >= 1, "Session not tracked"
        assert 'generate' in summary['flow_types'], "Generate flow not tracked"
        assert 'switch' in summary['flow_types'], "Switch flow not tracked"
        
        print("[OK] Frontend Integration working")
        print(f"   Session created: {session_id}")
        print(f"   Flows logged: {summary['total_flows']}")
        print(f"   Flow types: {list(summary['flow_types'].keys())}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Frontend Integration failed: {e}")
        return False

def test_three_js_conversion():
    """Test Three.js data conversion"""
    print("Testing Three.js Conversion...")
    try:
        from src.frontend_integration import frontend_integration
        
        # Test spec data
        spec_data = {
            'spec_id': 'three-js-test',
            'objects': [
                {
                    'id': 'floor-1',
                    'type': 'floor',
                    'material': 'wood',
                    'position': {'x': 0, 'y': 0, 'z': 0},
                    'dimensions': {'width': 10, 'height': 0.1, 'depth': 10},
                    'editable': True
                },
                {
                    'id': 'wall-1',
                    'type': 'wall',
                    'material': 'concrete',
                    'position': {'x': 5, 'y': 1.5, 'z': 0},
                    'dimensions': {'width': 0.2, 'height': 3, 'depth': 10},
                    'editable': True
                }
            ]
        }
        
        # Convert to Three.js format
        three_js_data = frontend_integration.prepare_three_js_data(spec_data)
        
        assert 'scene' in three_js_data, "Scene data missing"
        assert 'metadata' in three_js_data, "Metadata missing"
        assert len(three_js_data['scene']['objects']) == 2, "Objects not converted"
        
        # Check object conversion
        floor_obj = three_js_data['scene']['objects'][0]
        assert floor_obj['id'] == 'floor-1', "Object ID not preserved"
        assert floor_obj['geometry']['type'] == 'PlaneGeometry', "Wrong geometry for floor"
        assert floor_obj['material']['color'] == '#8B4513', "Wrong color for wood"
        
        # Check metadata
        metadata = three_js_data['metadata']
        assert metadata['spec_id'] == 'three-js-test', "Spec ID not preserved"
        assert metadata['object_count'] == 2, "Object count wrong"
        assert len(metadata['editable_objects']) == 2, "Editable objects not tracked"
        
        print("[OK] Three.js Conversion working")
        print(f"   Objects converted: {len(three_js_data['scene']['objects'])}")
        print(f"   Editable objects: {len(metadata['editable_objects'])}")
        print(f"   Floor geometry: {floor_obj['geometry']['type']}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Three.js Conversion failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("Day 5: Frontend + Preview Integration - Test Suite")
    print("=" * 60)
    
    sync_tests = [
        test_preview_manager,
        test_frontend_integration,
        test_three_js_conversion
    ]
    
    async_tests = [
        test_preview_generation
    ]
    
    passed = 0
    total = len(sync_tests) + len(async_tests)
    
    # Run sync tests
    for test in sync_tests:
        if test():
            passed += 1
        print()
    
    # Run async tests
    for test in async_tests:
        if await test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Day 5 implementation is ready.")
        return True
    else:
        print("Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)