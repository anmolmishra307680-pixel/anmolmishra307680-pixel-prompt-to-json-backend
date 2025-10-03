#!/usr/bin/env python3
"""Comprehensive test cases for material switching - Day 2 requirements"""

import pytest
import json
import uuid
from src.core.nlp_parser import ObjectTargeter, IterationTracker

class TestMaterialSwitching:
    """Test cases for 'change floor to marble', 'make cushions orange', etc."""
    
    def setup_method(self):
        """Setup test data"""
        self.targeter = ObjectTargeter()
        self.tracker = IterationTracker()
        
        # Sample spec with objects
        self.sample_spec = {
            "spec_id": "test_spec_001",
            "objects": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "floor",
                    "material": "wood",
                    "editable": True,
                    "properties": {"color": "brown", "finish": "matte"}
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "cushion",
                    "material": "fabric",
                    "editable": True,
                    "properties": {"color": "blue", "texture": "soft"}
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "wall",
                    "material": "concrete",
                    "editable": True,
                    "properties": {"color": "white"}
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "window",
                    "material": "glass",
                    "editable": True,
                    "properties": {"transparency": "clear"}
                }
            ]
        }
    
    def test_change_floor_to_marble(self):
        """Test: 'change floor to marble'"""
        instruction = "change floor to marble"
        
        # Parse target object
        target_id = self.targeter.parse_target(instruction, self.sample_spec)
        assert target_id is not None, "Should identify floor object"
        
        # Find floor object
        floor_obj = next(obj for obj in self.sample_spec['objects'] if obj['id'] == target_id)
        assert floor_obj['type'] == 'floor', "Should target floor object"
        
        # Parse material changes
        changes = self.targeter.parse_material(instruction)
        assert changes['material'] == 'marble', "Should parse marble material"
        
        # Apply changes
        before = floor_obj.copy()
        floor_obj.update(changes)
        after = floor_obj.copy()
        
        # Track iteration
        iteration_id = self.tracker.save_iteration(
            self.sample_spec['spec_id'], instruction, target_id, before, after
        )
        
        assert iteration_id is not None, "Should save iteration"
        assert floor_obj['material'] == 'marble', "Floor should be marble"
    
    def test_make_cushions_orange(self):
        """Test: 'make cushions orange'"""
        instruction = "make cushions orange"
        
        # Parse target object
        target_id = self.targeter.parse_target(instruction, self.sample_spec)
        assert target_id is not None, "Should identify cushion object"
        
        # Find cushion object
        cushion_obj = next(obj for obj in self.sample_spec['objects'] if obj['id'] == target_id)
        assert cushion_obj['type'] == 'cushion', "Should target cushion object"
        
        # Parse material changes
        changes = self.targeter.parse_material(instruction)
        assert 'properties' in changes, "Should have property changes"
        assert changes['properties']['color'] == 'orange', "Should parse orange color"
        
        # Apply changes
        before = cushion_obj.copy()
        if 'properties' not in cushion_obj:
            cushion_obj['properties'] = {}
        cushion_obj['properties'].update(changes['properties'])
        after = cushion_obj.copy()
        
        # Track iteration
        iteration_id = self.tracker.save_iteration(
            self.sample_spec['spec_id'], instruction, target_id, before, after
        )
        
        assert iteration_id is not None, "Should save iteration"
        assert cushion_obj['properties']['color'] == 'orange', "Cushions should be orange"
    
    def test_change_wall_to_glass(self):
        """Test: 'change wall to glass'"""
        instruction = "change wall to glass"
        
        target_id = self.targeter.parse_target(instruction, self.sample_spec)
        wall_obj = next(obj for obj in self.sample_spec['objects'] if obj['id'] == target_id)
        changes = self.targeter.parse_material(instruction)
        
        before = wall_obj.copy()
        wall_obj['material'] = changes['material']
        after = wall_obj.copy()
        
        iteration_id = self.tracker.save_iteration(
            self.sample_spec['spec_id'], instruction, target_id, before, after
        )
        
        assert wall_obj['material'] == 'glass', "Wall should be glass"
        assert iteration_id is not None, "Should track iteration"
    
    def test_make_window_blue_glossy(self):
        """Test: 'make window blue and glossy'"""
        instruction = "make window blue and glossy"
        
        target_id = self.targeter.parse_target(instruction, self.sample_spec)
        window_obj = next(obj for obj in self.sample_spec['objects'] if obj['id'] == target_id)
        changes = self.targeter.parse_material(instruction)
        
        before = window_obj.copy()
        if 'properties' not in window_obj:
            window_obj['properties'] = {}
        window_obj['properties'].update(changes['properties'])
        after = window_obj.copy()
        
        assert changes['properties']['color'] == 'blue', "Should parse blue color"
        assert changes['properties']['finish'] == 'glossy', "Should parse glossy finish"
        
        iteration_id = self.tracker.save_iteration(
            self.sample_spec['spec_id'], instruction, target_id, before, after
        )
        
        assert window_obj['properties']['color'] == 'blue', "Window should be blue"
        assert window_obj['properties']['finish'] == 'glossy', "Window should be glossy"
    
    def test_fuzzy_object_matching(self):
        """Test fuzzy matching for partial object names"""
        # Test partial matches
        assert self.targeter.parse_target("change flooring to marble", self.sample_spec) is not None
        assert self.targeter.parse_target("make pillow red", self.sample_spec) is not None
        assert self.targeter.parse_target("update walls", self.sample_spec) is not None
    
    def test_material_synonyms(self):
        """Test material synonym recognition"""
        # Test wood synonyms
        changes = self.targeter.parse_material("change to oak")
        assert changes['material'] == 'wood', "Should recognize oak as wood"
        
        # Test stone synonyms
        changes = self.targeter.parse_material("make it granite")
        assert changes['material'] == 'granite', "Should recognize granite"
        
        # Test metal synonyms
        changes = self.targeter.parse_material("switch to steel")
        assert changes['material'] == 'metal', "Should recognize steel as metal"
    
    def test_color_synonyms(self):
        """Test color synonym recognition"""
        changes = self.targeter.parse_material("make it crimson")
        assert changes['properties']['color'] == 'red', "Should recognize crimson as red"
        
        changes = self.targeter.parse_material("paint it navy")
        assert changes['properties']['color'] == 'blue', "Should recognize navy as blue"
    
    def test_iteration_diff_tracking(self):
        """Test detailed diff tracking in iterations"""
        instruction = "change floor to marble"
        target_id = self.targeter.parse_target(instruction, self.sample_spec)
        floor_obj = next(obj for obj in self.sample_spec['objects'] if obj['id'] == target_id)
        
        before = floor_obj.copy()
        floor_obj['material'] = 'marble'
        after = floor_obj.copy()
        
        iteration_id = self.tracker.save_iteration(
            self.sample_spec['spec_id'], instruction, target_id, before, after
        )
        
        # Check iteration was saved
        iterations = self.tracker.get_iterations(self.sample_spec['spec_id'])
        assert len(iterations) > 0, "Should have saved iterations"
        
        iteration = iterations[-1]
        assert iteration['instruction'] == instruction, "Should save instruction"
        assert iteration['object_id'] == target_id, "Should save object ID"
        assert 'diff' in iteration, "Should have diff"
        assert 'material' in iteration['diff']['changed_fields'], "Should track material change"
    
    def test_multiple_property_changes(self):
        """Test multiple property changes in one instruction"""
        instruction = "make cushion red leather with glossy finish"
        
        changes = self.targeter.parse_material(instruction)
        
        assert changes['material'] == 'leather', "Should parse leather material"
        assert changes['properties']['color'] == 'red', "Should parse red color"
        assert changes['properties']['finish'] == 'glossy', "Should parse glossy finish"
    
    def test_no_match_scenarios(self):
        """Test scenarios where no object or material is found"""
        # No matching object
        result = self.targeter.parse_target("change xyz to marble", self.sample_spec)
        assert result is None, "Should return None for non-existent object"
        
        # No matching material
        changes = self.targeter.parse_material("change to unknown_material")
        assert 'material' not in changes, "Should not parse unknown material"
    
    def test_case_insensitive_parsing(self):
        """Test case insensitive parsing"""
        # Mixed case instructions
        assert self.targeter.parse_target("Change FLOOR to Marble", self.sample_spec) is not None
        
        changes = self.targeter.parse_material("Make it ORANGE and GLOSSY")
        assert changes['properties']['color'] == 'orange', "Should handle uppercase"
        assert changes['properties']['finish'] == 'glossy', "Should handle mixed case"

def run_material_switching_tests():
    """Run all material switching tests"""
    test_instance = TestMaterialSwitching()
    
    test_methods = [
        'test_change_floor_to_marble',
        'test_make_cushions_orange', 
        'test_change_wall_to_glass',
        'test_make_window_blue_glossy',
        'test_fuzzy_object_matching',
        'test_material_synonyms',
        'test_color_synonyms',
        'test_iteration_diff_tracking',
        'test_multiple_property_changes',
        'test_no_match_scenarios',
        'test_case_insensitive_parsing'
    ]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            test_instance.setup_method()
            method = getattr(test_instance, method_name)
            method()
            print(f"[PASS] {method_name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {method_name}: {e}")
            failed += 1
    
    print(f"\n[RESULTS] Test Results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = run_material_switching_tests()
    exit(0 if success else 1)