#!/usr/bin/env python3
"""Test script for Day 1 LM Integration and Schema Extensions"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_lm_adapter():
    """Test LM Adapter functionality"""
    print("Testing LM Adapter...")
    try:
        from src.lm_adapter.lm_interface import LocalLMAdapter
        
        adapter = LocalLMAdapter()
        result = adapter.run("Modern electric vehicle with aerodynamic design")
        
        print(f"[OK] LM Adapter working")
        print(f"   Design Type: {result.get('design_type')}")
        print(f"   Features: {result.get('features')}")
        print(f"   Materials: {len(result.get('materials', []))} materials")
        
        return True
    except Exception as e:
        print(f"[FAIL] LM Adapter failed: {e}")
        return False

def test_v2_schema():
    """Test v2 Schema functionality"""
    print("\nTesting v2 Schema...")
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
        
        print(f"[OK] v2 Schema working")
        print(f"   Spec ID: {spec.spec_id}")
        print(f"   Object ID: {spec.objects[0].id}")
        print(f"   Editable: {spec.objects[0].editable}")
        
        return True
    except Exception as e:
        print(f"[FAIL] v2 Schema failed: {e}")
        return False

def test_preview_generator():
    """Test preview generator"""
    print("\nTesting Preview Generator...")
    try:
        from src.preview_generator import generate_preview, create_placeholder_preview
        
        test_spec = {
            'spec_id': 'test-123',
            'metadata': {
                'original_spec': {
                    'design_type': 'vehicle'
                }
            }
        }
        
        preview_url = generate_preview(test_spec)
        placeholder = create_placeholder_preview('building', [
            {'type': 'wall', 'material': 'concrete'},
            {'type': 'door', 'material': 'wood'}
        ])
        
        print(f"[OK] Preview Generator working")
        print(f"   Preview URL: {preview_url}")
        print(f"   Placeholder length: {len(placeholder)} chars")
        
        return True
    except Exception as e:
        print(f"[FAIL] Preview Generator failed: {e}")
        return False

def test_integration():
    """Test full integration"""
    print("\nTesting Full Integration...")
    try:
        from src.lm_adapter.lm_interface import LocalLMAdapter
        from src.schemas.v2_schema import GenerateRequestV2, DesignObject, SceneInfo, Dimensions3D, Position3D, EnhancedDesignSpec
        
        # Simulate the full flow
        adapter = LocalLMAdapter()
        request = GenerateRequestV2(
            prompt="Smart home IoT sensor",
            context={"environment": "indoor"},
            style="minimalist"
        )
        
        # Run LM inference
        spec_data = adapter.run(request.prompt, request.context)
        
        # Create enhanced objects
        objects = []
        for i, component in enumerate(spec_data.get('components', ['sensor'])):
            obj = DesignObject(
                type=component,
                material=spec_data.get('materials', [{'type': 'plastic'}])[0]['type'],
                dimensions=Dimensions3D(width=5.0, height=2.0, depth=3.0),
                position=Position3D(x=i*2.0, y=0.0, z=0.0)
            )
            objects.append(obj)
        
        scene = SceneInfo(
            name="IoT Sensor Design",
            description=request.prompt,
            total_objects=len(objects),
            bounding_box=Dimensions3D(width=10.0, height=5.0, depth=10.0)
        )
        
        enhanced_spec = EnhancedDesignSpec(
            objects=objects,
            scene=scene,
            metadata={
                "original_spec": spec_data,
                "generation_method": "lm_adapter"
            }
        )
        
        print(f"[OK] Full Integration working")
        print(f"   Generated {len(enhanced_spec.objects)} objects")
        print(f"   Scene: {enhanced_spec.scene.name}")
        print(f"   Metadata keys: {list(enhanced_spec.metadata.keys())}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Full Integration failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Day 1: LM Integration and Schema Extensions - Test Suite")
    print("=" * 60)
    
    tests = [
        test_lm_adapter,
        test_v2_schema,
        test_preview_generator,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Day 1 implementation is ready.")
        return True
    else:
        print("Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)