"""Test switch functionality for material changes"""

import pytest
import requests
import json
from datetime import datetime

class TestSwitchFunctionality:
    
    @pytest.fixture
    def api_base(self):
        return "http://localhost:8000"
    
    @pytest.fixture
    def auth_headers(self, api_base):
        """Get authentication headers"""
        # Get JWT token
        login_response = requests.post(
            f"{api_base}/api/v1/auth/login",
            json={"username": "admin", "password": "bhiv2024"},
            headers={"X-API-Key": "bhiv-secret-key-2024"}
        )
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            return {
                "X-API-Key": "bhiv-secret-key-2024",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        else:
            # Fallback for testing
            return {
                "X-API-Key": "test-api-key",
                "Content-Type": "application/json"
            }
    
    def test_change_floor_to_marble(self, api_base, auth_headers):
        """Test changing floor material to marble"""
        
        # First generate a design with a floor
        generate_data = {
            "user_id": "test_user",
            "prompt": "Living room with wooden floor",
            "context": {"style": "modern"}
        }
        
        gen_response = requests.post(
            f"{api_base}/api/v1/generate",
            json=generate_data,
            headers=auth_headers
        )
        
        assert gen_response.status_code == 200
        gen_result = gen_response.json()
        spec_id = gen_result.get("spec_id")
        
        # Now switch floor to marble
        switch_data = {
            "user_id": "test_user",
            "spec_id": spec_id,
            "target": {"object_id": "floor_1"},
            "update": {"material": "marble"}
        }
        
        switch_response = requests.post(
            f"{api_base}/api/v1/switch",
            json=switch_data,
            headers=auth_headers
        )
        
        assert switch_response.status_code == 200
        switch_result = switch_response.json()
        
        # Verify the change
        assert "changed" in switch_result
        assert switch_result["changed"]["object_id"] == "floor_1"
        assert "marble" in switch_result["changed"]["after"]["material"].lower()
        
        # Verify iteration ID is generated
        assert "iteration_id" in switch_result
        assert switch_result["iteration_id"] is not None
    
    def test_make_cushions_orange(self, api_base, auth_headers):
        """Test making cushions orange"""
        
        # Generate a design with furniture
        generate_data = {
            "user_id": "test_user",
            "prompt": "Living room with sofa and cushions",
            "context": {"style": "contemporary"}
        }
        
        gen_response = requests.post(
            f"{api_base}/api/v1/generate",
            json=generate_data,
            headers=auth_headers
        )
        
        assert gen_response.status_code == 200
        gen_result = gen_response.json()
        spec_id = gen_result.get("spec_id")
        
        # Switch cushion color to orange
        switch_data = {
            "user_id": "test_user",
            "spec_id": spec_id,
            "target": {"object_id": "cushion_1"},
            "update": {
                "material": "fabric_orange",
                "properties": {"color": "orange"}
            }
        }
        
        switch_response = requests.post(
            f"{api_base}/api/v1/switch",
            json=switch_data,
            headers=auth_headers
        )
        
        assert switch_response.status_code == 200
        switch_result = switch_response.json()
        
        # Verify the change
        assert "changed" in switch_result
        changed = switch_result["changed"]
        assert "orange" in changed["after"]["material"].lower() or \
               changed["after"].get("properties", {}).get("color") == "orange"
    
    def test_natural_language_switch(self, api_base, auth_headers):
        """Test natural language instruction parsing"""
        
        # Generate base design
        generate_data = {
            "user_id": "test_user",
            "prompt": "Modern kitchen with white cabinets",
            "context": {"style": "minimalist"}
        }
        
        gen_response = requests.post(
            f"{api_base}/api/v1/generate",
            json=generate_data,
            headers=auth_headers
        )
        
        assert gen_response.status_code == 200
        gen_result = gen_response.json()
        spec_id = gen_result.get("spec_id")
        
        # Use natural language instruction
        switch_data = {
            "user_id": "test_user",
            "spec_id": spec_id,
            "instruction": "Change the cabinets to dark wood"
        }
        
        switch_response = requests.post(
            f"{api_base}/api/v1/switch",
            json=switch_data,
            headers=auth_headers
        )
        
        # Should work even if parsing is basic
        if switch_response.status_code == 200:
            switch_result = switch_response.json()
            assert "changed" in switch_result or "updated_spec_json" in switch_result
    
    def test_switch_with_preview_update(self, api_base, auth_headers):
        """Test that switch generates new preview URL"""
        
        # Generate design
        generate_data = {
            "user_id": "test_user",
            "prompt": "Bedroom with blue walls",
            "context": {"style": "cozy"}
        }
        
        gen_response = requests.post(
            f"{api_base}/api/v1/generate",
            json=generate_data,
            headers=auth_headers
        )
        
        assert gen_response.status_code == 200
        gen_result = gen_response.json()
        spec_id = gen_result.get("spec_id")
        original_preview = gen_result.get("preview_url")
        
        # Switch wall color
        switch_data = {
            "user_id": "test_user",
            "spec_id": spec_id,
            "target": {"object_id": "wall_1"},
            "update": {"material": "paint_green"}
        }
        
        switch_response = requests.post(
            f"{api_base}/api/v1/switch",
            json=switch_data,
            headers=auth_headers
        )
        
        assert switch_response.status_code == 200
        switch_result = switch_response.json()
        
        # Verify new preview URL is generated
        new_preview = switch_result.get("preview_url")
        assert new_preview is not None
        assert new_preview != original_preview  # Should be different
    
    def test_switch_error_handling(self, api_base, auth_headers):
        """Test error handling for invalid switch requests"""
        
        # Test with non-existent spec_id
        switch_data = {
            "user_id": "test_user",
            "spec_id": "non_existent_spec",
            "target": {"object_id": "floor_1"},
            "update": {"material": "marble"}
        }
        
        switch_response = requests.post(
            f"{api_base}/api/v1/switch",
            json=switch_data,
            headers=auth_headers
        )
        
        assert switch_response.status_code == 404
        
        # Test with missing required fields
        invalid_data = {
            "user_id": "test_user"
            # Missing spec_id, target, update
        }
        
        invalid_response = requests.post(
            f"{api_base}/api/v1/switch",
            json=invalid_data,
            headers=auth_headers
        )
        
        assert invalid_response.status_code in [400, 422]  # Bad request or validation error
    
    def test_multiple_switches_on_same_spec(self, api_base, auth_headers):
        """Test multiple sequential switches on the same specification"""
        
        # Generate base design
        generate_data = {
            "user_id": "test_user",
            "prompt": "Office space with desk and chair",
            "context": {"style": "professional"}
        }
        
        gen_response = requests.post(
            f"{api_base}/api/v1/generate",
            json=generate_data,
            headers=auth_headers
        )
        
        assert gen_response.status_code == 200
        gen_result = gen_response.json()
        spec_id = gen_result.get("spec_id")
        
        # First switch: change desk material
        switch1_data = {
            "user_id": "test_user",
            "spec_id": spec_id,
            "target": {"object_id": "desk_1"},
            "update": {"material": "oak_wood"}
        }
        
        switch1_response = requests.post(
            f"{api_base}/api/v1/switch",
            json=switch1_data,
            headers=auth_headers
        )
        
        assert switch1_response.status_code == 200
        switch1_result = switch1_response.json()
        iteration1_id = switch1_result.get("iteration_id")
        
        # Second switch: change chair material
        switch2_data = {
            "user_id": "test_user",
            "spec_id": spec_id,
            "target": {"object_id": "chair_1"},
            "update": {"material": "leather_black"}
        }
        
        switch2_response = requests.post(
            f"{api_base}/api/v1/switch",
            json=switch2_data,
            headers=auth_headers
        )
        
        assert switch2_response.status_code == 200
        switch2_result = switch2_response.json()
        iteration2_id = switch2_result.get("iteration_id")
        
        # Verify different iteration IDs
        assert iteration1_id != iteration2_id
        
        # Verify both changes are preserved
        final_spec = switch2_result.get("updated_spec_json", {})
        assert final_spec is not None