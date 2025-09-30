"""Test configuration and fixtures"""
import os
import sys
from pathlib import Path
import pytest

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set test environment variables
os.environ["API_KEY"] = "bhiv-secret-key-2024"
os.environ["DEMO_USERNAME"] = "admin"
os.environ["DEMO_PASSWORD"] = "bhiv2024"
os.environ["JWT_SECRET"] = "bhiv-jwt-secret-2024"
os.environ["SECRET_KEY"] = "bhiv-jwt-secret-2024"
os.environ["TESTING"] = "true"

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    # Ensure test environment is properly configured
    yield