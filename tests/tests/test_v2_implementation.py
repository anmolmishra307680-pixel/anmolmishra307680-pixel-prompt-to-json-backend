#!/usr/bin/env python3
"""Test script for Day 1 LM Integration and Schema Extensions"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_lm_adapter():
    """Test LM Adapter functionality"""
    print("Testing LM Adapter...")
    try:
        from src.core.lm_adapter import LocalLMAdapter
        
        adapter = LocalLMAdapter()
        result = adapter.run("Modern electric vehicle with aerodynamic design")
        
        assert result is not None, "No result returned"
        
        print("[OK] LM Adapter working")
    except Exception as e:
        print(f"[FAIL] LM Adapter failed: {e}")
        assert False, f"LM Adapter failed: {e}"

def test_v2_schema():
    """Test v2 Schema functionality"""
    print("Testing v2 Schema...")
    try:
        from src.schemas.v2_schema import (
            DesignObject, SceneInfo, EnhancedDesignSpec, 
            GenerateRequestV2, GenerateResponseV2,
            Dimensions3D, Position3D
        )
        
        # Create test objects
        obj = DesignObject(
            type="test_component",
            material="steel",
            dimensions=Dimensions3D(width=10.0, height=5.0, depth=8.0),
            position=Position3D(x=0.0, y=0.0, z=0.0)
        )
        
        scene = SceneInfo(
            name="Test Scene",
            description="Test description",
            total_objects=1,
            bounding_box=Dimensions3D(width=20.0, height=10.0, depth=20.0)
        )
        
        spec = EnhancedDesignSpec(
            objects=[obj],
            scene=scene
        )
        
        assert spec.spec_id is not None, "Spec ID not generated"
        
        print("[OK] v2 Schema working")
    except Exception as e:
        print(f"[FAIL] v2 Schema failed: {e}")
        assert False, f"v2 Schema failed: {e}"

def test_preview_generator():
    """Test preview generator"""
    print("Testing Preview Generator...")
    try:
        from src.services.preview_generator import generate_preview
        
        test_spec = {
            'spec_id': 'test-123',
            'metadata': {
                'original_spec': {
                    'design_type': 'vehicle'
                }
            }
        }
        
        preview_url = generate_preview(test_spec)
        
        assert preview_url is not None, "Preview URL not generated"
        
        print("[OK] Preview Generator working")
    except Exception as e:
        print(f"[FAIL] Preview Generator failed: {e}")
        assert False, f"Preview Generator failed: {e}"

def test_integration():
    """Test full integration"""
    print("Testing Full Integration...")
    try:
        from src.core.lm_adapter import LocalLMAdapter
        from src.schemas.v2_schema import GenerateRequestV2, DesignObject, SceneInfo, Dimensions3D, Position3D, EnhancedDesignSpec
        
        # Simulate the full flow
        adapter = LocalLMAdapter()
        request = GenerateRequestV2(
            prompt="Smart home IoT sensor",
            context={"environment": "indoor"},
            style="minimalist"
        )
        
        # Run LM inference
        spec_data = adapter.run(request.prompt)
        
        assert spec_data is not None, "Spec data not generated"
        
        print("[OK] Full Integration working")
    except Exception as e:
        print(f"[FAIL] Full Integration failed: {e}")
        assert False, f"Full Integration failed: {e}"