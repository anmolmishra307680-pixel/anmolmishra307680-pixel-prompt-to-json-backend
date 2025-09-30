#!/usr/bin/env python3
"""Test script for Day 2 Material Switcher & Object Editing"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_object_parser():
    """Test ObjectTargeter functionality"""
    print("Testing ObjectTargeter...")
    try:
        from src.nlp_parser.object_parser import ObjectTargeter
        
        targeter = ObjectTargeter()
        
        # Test spec with objects
        test_spec = {
            'objects': [
                {'id': 'obj1', 'type': 'floor', 'material': 'wood'},
                {'id': 'obj2', 'type': 'cushion', 'material': 'fabric'},
                {'id': 'obj3', 'type': 'wall', 'material': 'concrete'}
            ]
        }
        
        # Test "change floor to marble"
        target_id = targeter.parse_target("change floor to marble", test_spec)
        material_changes = targeter.parse_material("change floor to marble")
        
        assert target_id == 'obj1', f"Expected obj1, got {target_id}"
        assert material_changes['material'] == 'marble', f"Expected marble, got {material_changes}"
        
        # Test "make cushions orange"
        target_id2 = targeter.parse_target("make cushions orange", test_spec)
        material_changes2 = targeter.parse_material("make cushions orange")
        
        assert target_id2 == 'obj2', f"Expected obj2, got {target_id2}"
        assert material_changes2['material'] == 'fabric', f"Expected fabric, got {material_changes2}"
        assert material_changes2['properties']['color'] == 'orange', f"Expected orange color"
        
        print("[OK] ObjectTargeter working")
        return True
    except Exception as e:
        print(f"[FAIL] ObjectTargeter failed: {e}")
        return False

def test_spec_storage():
    """Test spec storage functionality"""
    print("Testing Spec Storage...")
    try:
        from src.spec_storage import spec_storage
        
        # Test storing and retrieving spec
        test_spec = {
            'spec_id': 'test-123',
            'objects': [{'id': 'obj1', 'type': 'test', 'material': 'steel'}]
        }
        
        spec_storage.store_spec('test-123', test_spec)
        retrieved = spec_storage.get_spec('test-123')
        
        assert retrieved is not None, "Spec not retrieved"
        assert retrieved['spec_id'] == 'test-123', "Wrong spec ID"
        
        print("[OK] Spec Storage working")
        return True
    except Exception as e:
        print(f"[FAIL] Spec Storage failed: {e}")
        return False

def test_switch_logic():
    """Test the switch logic"""
    print("Testing Switch Logic...")
    try:
        from src.nlp_parser.object_parser import ObjectTargeter
        
        # Create test data
        spec_data = {
            'objects': [
                {
                    'id': 'floor-obj',
                    'type': 'floor',
                    'material': 'wood',
                    'properties': {}
                },
                {
                    'id': 'cushion-obj', 
                    'type': 'cushion',
                    'material': 'fabric',
                    'properties': {'color': 'blue'}
                }
            ]
        }
        
        targeter = ObjectTargeter()
        
        # Test "change floor to marble"
        target_id1 = targeter.parse_target("change floor to marble", spec_data)
        changes1 = targeter.parse_material("change floor to marble")
        
        assert target_id1 == 'floor-obj', f"Wrong floor target: {target_id1}"
        assert changes1['material'] == 'marble', f"Wrong material: {changes1}"
        
        # Test "make cushions orange"
        target_id2 = targeter.parse_target("make cushions orange", spec_data)
        changes2 = targeter.parse_material("make cushions orange")
        
        assert target_id2 == 'cushion-obj', f"Wrong cushion target: {target_id2}"
        assert changes2['properties']['color'] == 'orange', f"Wrong color: {changes2}"
        
        print("[OK] Switch Logic working")
        return True
    except Exception as e:
        print(f"[FAIL] Switch Logic failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Day 2: Material Switcher & Object Editing - Test Suite")
    print("=" * 60)
    
    tests = [
        test_object_parser,
        test_spec_storage,
        test_switch_logic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Day 2 implementation is ready.")
        return True
    else:
        print("Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)