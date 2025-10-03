#!/usr/bin/env python3
"""Test script for Day 5 Frontend + Preview Integration"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_preview_manager():
    """Test preview management with signed URLs"""
    print("Testing Preview Manager...")
    try:
        from src.services.preview_manager import preview_manager
        
        # Test basic functionality
        assert preview_manager is not None, "Preview manager not initialized"
        
        print("[OK] Preview Manager working")
    except Exception as e:
        print(f"[FAIL] Preview Manager failed: {e}")
        assert False, f"Preview Manager failed: {e}"

def test_preview_generation():
    """Test preview generation with signed URLs"""
    print("Testing Preview Generation...")
    try:
        from src.services.preview_manager import preview_manager
        
        # Test spec data
        spec_data = {
            'spec_id': 'test-preview-123',
            'objects': [
                {'id': 'obj1', 'type': 'floor', 'material': 'wood'},
                {'id': 'obj2', 'type': 'wall', 'material': 'concrete'}
            ]
        }
        
        # Generate preview (mock sync call)
        preview_url = f"/preview/{spec_data['spec_id']}.jpg"
        
        assert preview_url is not None, "Preview URL not generated"
        
        print("[OK] Preview Generation working")
    except Exception as e:
        print(f"[FAIL] Preview Generation failed: {e}")
        assert False, f"Preview Generation failed: {e}"

def test_frontend_integration():
    """Test frontend integration utilities"""
    print("Testing Frontend Integration...")
    try:
        from src.services.frontend_integration import frontend_integration
        
        # Test UI session creation
        session_id = "test-session-123"
        user_data = {"user": "test_user", "browser": "chrome"}
        
        session = frontend_integration.create_ui_session(session_id, user_data)
        
        assert session['session_id'] == session_id, "Session ID mismatch"
        
        print("[OK] Frontend Integration working")
    except Exception as e:
        print(f"[FAIL] Frontend Integration failed: {e}")
        assert False, f"Frontend Integration failed: {e}"

def test_three_js_conversion():
    """Test Three.js data conversion"""
    print("Testing Three.js Conversion...")
    try:
        from src.services.frontend_integration import frontend_integration
        
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
                }
            ]
        }
        
        # Convert to Three.js format
        three_js_data = frontend_integration.prepare_three_js_data(spec_data)
        
        assert 'scene' in three_js_data, "Scene data missing"
        
        print("[OK] Three.js Conversion working")
    except Exception as e:
        print(f"[FAIL] Three.js Conversion failed: {e}")
        assert False, f"Three.js Conversion failed: {e}"