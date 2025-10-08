"""Unit tests for material switching functionality"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.schemas.spec_schema import Spec, ObjectSpec, SceneSpec
from src.routers.switch import find_object, SwitchRequest, TargetObject, MaterialUpdate

# Test data
sample_spec = Spec(
    spec_id="test_spec_123",
    objects=[
        ObjectSpec(
            id="floor_001",
            type="floor",
            material="wood",
            editable=True,
            properties={"finish": "matte", "color": "brown"}
        ),
        ObjectSpec(
            id="cushion_001", 
            type="cushion",
            material="fabric",
            editable=True,
            properties={"color": "blue", "texture": "soft"}
        )
    ],
    scene=SceneSpec(environment="indoor", lighting="natural", scale=1.0)
)

class TestFindObject:
    """Test object finding functionality"""
    
    def test_find_existing_object(self):
        """Test finding an object that exists"""
        obj = find_object(sample_spec, "floor_001")
        assert obj.id == "floor_001"
        assert obj.material == "wood"
    
    def test_find_nonexistent_object(self):
        """Test finding an object that doesn't exist"""
        with pytest.raises(Exception) as exc_info:
            find_object(sample_spec, "nonexistent_001")
        assert "not found" in str(exc_info.value)

class TestSwitchEndpoint:
    """Test switch endpoint functionality"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def mock_db(self, monkeypatch):
        """Mock database operations"""
        mock_db = AsyncMock()
        mock_db.get_spec.return_value = sample_spec.dict()
        mock_db.save_iteration.return_value = "iter_123"
        mock_db.update_spec.return_value = True
        
        def mock_get_database():
            return mock_db
        
        monkeypatch.setattr("src.routers.switch.get_database", mock_get_database)
        return mock_db
    
    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers"""
        return {
            "X-API-Key": "test-api-key",
            "Authorization": "Bearer test-token"
        }
    
    def test_change_floor_to_marble(self, client, mock_db, auth_headers, monkeypatch):
        """Test changing floor material to marble"""
        # Mock auth functions
        monkeypatch.setattr("src.routers.switch.verify_api_key", lambda: "test-key")
        monkeypatch.setattr("src.routers.switch.verify_jwt_token", lambda: "test-token")
        
        request_data = {
            "spec_id": "test_spec_123",
            "target": {"object_id": "floor_001"},
            "update": {"material": "marble"},
            "note": "Changed floor to marble for elegance"
        }
        
        response = client.post("/api/v1/switch", json=request_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert data["spec_id"] == "test_spec_123"
        assert "updated_spec_json" in data
        assert "preview_url" in data
        assert data["changed"]["object_id"] == "floor_001"
        assert data["changed"]["before"] == "wood"
        assert data["changed"]["after"] == "marble"
        
        # Verify database calls
        mock_db.get_spec.assert_called_once_with("test_spec_123")
        mock_db.save_iteration.assert_called_once()
        mock_db.update_spec.assert_called_once()
    
    def test_make_cushions_orange(self, client, mock_db, auth_headers, monkeypatch):
        """Test making cushions orange with property update"""
        # Mock auth functions
        monkeypatch.setattr("src.routers.switch.verify_api_key", lambda: "test-key")
        monkeypatch.setattr("src.routers.switch.verify_jwt_token", lambda: "test-token")
        
        request_data = {
            "spec_id": "test_spec_123",
            "target": {"object_id": "cushion_001"},
            "update": {
                "material": "fabric",
                "properties": {"color": "orange"}
            },
            "note": "Made cushions orange for warmth"
        }
        
        response = client.post("/api/v1/switch", json=request_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response
        assert data["spec_id"] == "test_spec_123"
        assert data["changed"]["object_id"] == "cushion_001"
        assert data["changed"]["before"] == "fabric"
        assert data["changed"]["after"] == "fabric"
        
        # Verify updated spec contains orange color
        updated_spec = data["updated_spec_json"]
        cushion_obj = next(obj for obj in updated_spec["objects"] if obj["id"] == "cushion_001")
        assert cushion_obj["properties"]["color"] == "orange"
        
        # Verify database interaction
        mock_db.save_iteration.assert_called_once()
    
    def test_switch_nonexistent_object(self, client, mock_db, auth_headers, monkeypatch):
        """Test switching material on nonexistent object"""
        # Mock auth functions
        monkeypatch.setattr("src.routers.switch.verify_api_key", lambda: "test-key")
        monkeypatch.setattr("src.routers.switch.verify_jwt_token", lambda: "test-token")
        
        request_data = {
            "spec_id": "test_spec_123",
            "target": {"object_id": "nonexistent_001"},
            "update": {"material": "steel"}
        }
        
        response = client.post("/api/v1/switch", json=request_data, headers=auth_headers)
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_switch_nonexistent_spec(self, client, auth_headers, monkeypatch):
        """Test switching material on nonexistent spec"""
        # Mock auth functions
        monkeypatch.setattr("src.routers.switch.verify_api_key", lambda: "test-key")
        monkeypatch.setattr("src.routers.switch.verify_jwt_token", lambda: "test-token")
        
        # Mock database to return None
        mock_db = AsyncMock()
        mock_db.get_spec.return_value = None
        
        def mock_get_database():
            return mock_db
        
        monkeypatch.setattr("src.routers.switch.get_database", mock_get_database)
        
        request_data = {
            "spec_id": "nonexistent_spec",
            "target": {"object_id": "floor_001"},
            "update": {"material": "marble"}
        }
        
        response = client.post("/api/v1/switch", json=request_data, headers=auth_headers)
        
        assert response.status_code == 404
        assert "Spec not found" in response.json()["detail"]