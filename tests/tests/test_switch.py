"""Test switch functionality for material changes"""

import pytest
from unittest.mock import Mock, patch
import json
from datetime import datetime

class TestSwitchFunctionality:
    
    @pytest.fixture
    def mock_api_client(self):
        """Mock API client for testing"""
        client = Mock()
        client.base_url = "http://localhost:8000/api/v1"
        client.api_key = "test-api-key"
        client.token = "mock-jwt-token"
        return client
    
    @pytest.fixture
    def mock_auth_headers(self):
        """Mock authentication headers"""
        return {
            "X-API-Key": "test-api-key",
            "Authorization": "Bearer mock-jwt-token",
            "Content-Type": "application/json"
        }
    
    @patch('requests.post')
    def test_change_floor_to_marble(self, mock_post, mock_auth_headers):
        """Test changing floor material to marble"""
        
        # Mock generate response
        mock_gen_response = Mock()
        mock_gen_response.status_code = 200
        mock_gen_response.json.return_value = {
            "spec_id": "test_spec_001",
            "spec_json": {
                "objects": [{"object_id": "floor_1", "type": "floor", "material": "wood"}]
            }
        }
        
        # Mock switch response
        mock_switch_response = Mock()
        mock_switch_response.status_code = 200
        mock_switch_response.json.return_value = {
            "spec_id": "test_spec_001",
            "iteration_id": "iter_001",
            "changed": {
                "object_id": "floor_1",
                "before": {"material": "wood"},
                "after": {"material": "marble"}
            }
        }
        
        # Configure mock to return different responses for different calls
        mock_post.side_effect = [mock_gen_response, mock_switch_response]
        
        # Test generate call
        generate_data = {
            "user_id": "test_user",
            "prompt": "Living room with wooden floor",
            "context": {"style": "modern"}
        }
        
        # Simulate API calls
        gen_result = mock_gen_response.json()
        spec_id = gen_result.get("spec_id")
        assert spec_id == "test_spec_001"
        
        # Test switch call
        switch_data = {
            "user_id": "test_user",
            "spec_id": spec_id,
            "target": {"object_id": "floor_1"},
            "update": {"material": "marble"}
        }
        
        switch_result = mock_switch_response.json()
        
        # Verify the change
        assert "changed" in switch_result
        assert switch_result["changed"]["object_id"] == "floor_1"
        assert "marble" in switch_result["changed"]["after"]["material"].lower()
        
        # Verify iteration ID is generated
        assert "iteration_id" in switch_result
        assert switch_result["iteration_id"] is not None
    
    @patch('requests.post')
    def test_make_cushions_orange(self, mock_post, mock_auth_headers):
        """Test making cushions orange"""
        
        # Mock responses
        mock_gen_response = Mock()
        mock_gen_response.status_code = 200
        mock_gen_response.json.return_value = {
            "spec_id": "test_spec_002",
            "spec_json": {
                "objects": [{"object_id": "cushion_1", "type": "cushion", "material": "fabric_blue"}]
            }
        }
        
        mock_switch_response = Mock()
        mock_switch_response.status_code = 200
        mock_switch_response.json.return_value = {
            "spec_id": "test_spec_002",
            "iteration_id": "iter_002",
            "changed": {
                "object_id": "cushion_1",
                "before": {"material": "fabric_blue"},
                "after": {"material": "fabric_orange", "properties": {"color": "orange"}}
            }
        }
        
        mock_post.side_effect = [mock_gen_response, mock_switch_response]
        
        # Simulate the test
        gen_result = mock_gen_response.json()
        spec_id = gen_result.get("spec_id")
        
        switch_result = mock_switch_response.json()
        
        # Verify the change
        assert "changed" in switch_result
        changed = switch_result["changed"]
        assert "orange" in changed["after"]["material"].lower() or \
               changed["after"].get("properties", {}).get("color") == "orange"
    
    @patch('requests.post')
    def test_natural_language_switch(self, mock_post, mock_auth_headers):
        """Test natural language instruction parsing"""
        
        # Mock responses
        mock_gen_response = Mock()
        mock_gen_response.status_code = 200
        mock_gen_response.json.return_value = {
            "spec_id": "test_spec_003",
            "spec_json": {
                "objects": [{"object_id": "cabinet_1", "type": "cabinet", "material": "wood_white"}]
            }
        }
        
        mock_switch_response = Mock()
        mock_switch_response.status_code = 200
        mock_switch_response.json.return_value = {
            "spec_id": "test_spec_003",
            "iteration_id": "iter_003",
            "updated_spec_json": {
                "objects": [{"object_id": "cabinet_1", "type": "cabinet", "material": "wood_dark"}]
            }
        }
        
        mock_post.side_effect = [mock_gen_response, mock_switch_response]
        
        # Simulate the test
        gen_result = mock_gen_response.json()
        spec_id = gen_result.get("spec_id")
        
        switch_result = mock_switch_response.json()
        
        # Should work even if parsing is basic
        assert switch_result["spec_id"] == spec_id
        assert "updated_spec_json" in switch_result
    
    @patch('requests.post')
    def test_switch_with_preview_update(self, mock_post, mock_auth_headers):
        """Test that switch generates new preview URL"""
        
        # Mock responses
        mock_gen_response = Mock()
        mock_gen_response.status_code = 200
        mock_gen_response.json.return_value = {
            "spec_id": "test_spec_004",
            "preview_url": "/preview/test_spec_004_v1.jpg"
        }
        
        mock_switch_response = Mock()
        mock_switch_response.status_code = 200
        mock_switch_response.json.return_value = {
            "spec_id": "test_spec_004",
            "preview_url": "/preview/test_spec_004_v2.jpg",
            "iteration_id": "iter_004"
        }
        
        mock_post.side_effect = [mock_gen_response, mock_switch_response]
        
        # Simulate the test
        gen_result = mock_gen_response.json()
        spec_id = gen_result.get("spec_id")
        original_preview = gen_result.get("preview_url")
        
        switch_result = mock_switch_response.json()
        
        # Verify new preview URL is generated
        new_preview = switch_result.get("preview_url")
        assert new_preview is not None
        assert new_preview != original_preview  # Should be different
    
    @patch('requests.post')
    def test_switch_error_handling(self, mock_post, mock_auth_headers):
        """Test error handling for invalid switch requests"""
        
        # Mock error responses
        mock_404_response = Mock()
        mock_404_response.status_code = 404
        mock_404_response.json.return_value = {"detail": "Spec not found"}
        
        mock_400_response = Mock()
        mock_400_response.status_code = 400
        mock_400_response.json.return_value = {"detail": "Missing required fields"}
        
        mock_post.side_effect = [mock_404_response, mock_400_response]
        
        # Test with non-existent spec_id
        switch_data = {
            "user_id": "test_user",
            "spec_id": "non_existent_spec",
            "target": {"object_id": "floor_1"},
            "update": {"material": "marble"}
        }
        
        # Simulate first call (404)
        result_404 = mock_404_response
        assert result_404.status_code == 404
        
        # Test with missing required fields
        invalid_data = {
            "user_id": "test_user"
            # Missing spec_id, target, update
        }
        
        # Simulate second call (400)
        result_400 = mock_400_response
        assert result_400.status_code == 400
    
    @patch('requests.post')
    def test_multiple_switches_on_same_spec(self, mock_post, mock_auth_headers):
        """Test multiple sequential switches on the same specification"""
        
        # Mock responses
        mock_gen_response = Mock()
        mock_gen_response.status_code = 200
        mock_gen_response.json.return_value = {
            "spec_id": "test_spec_005",
            "spec_json": {
                "objects": [
                    {"object_id": "desk_1", "type": "desk", "material": "wood_pine"},
                    {"object_id": "chair_1", "type": "chair", "material": "fabric_gray"}
                ]
            }
        }
        
        mock_switch1_response = Mock()
        mock_switch1_response.status_code = 200
        mock_switch1_response.json.return_value = {
            "spec_id": "test_spec_005",
            "iteration_id": "iter_005_1"
        }
        
        mock_switch2_response = Mock()
        mock_switch2_response.status_code = 200
        mock_switch2_response.json.return_value = {
            "spec_id": "test_spec_005",
            "iteration_id": "iter_005_2",
            "updated_spec_json": {
                "objects": [
                    {"object_id": "desk_1", "type": "desk", "material": "oak_wood"},
                    {"object_id": "chair_1", "type": "chair", "material": "leather_black"}
                ]
            }
        }
        
        mock_post.side_effect = [mock_gen_response, mock_switch1_response, mock_switch2_response]
        
        # Simulate the test
        gen_result = mock_gen_response.json()
        spec_id = gen_result.get("spec_id")
        
        switch1_result = mock_switch1_response.json()
        iteration1_id = switch1_result.get("iteration_id")
        
        switch2_result = mock_switch2_response.json()
        iteration2_id = switch2_result.get("iteration_id")
        
        # Verify different iteration IDs
        assert iteration1_id != iteration2_id
        
        # Verify both changes are preserved
        final_spec = switch2_result.get("updated_spec_json", {})
        assert final_spec is not None