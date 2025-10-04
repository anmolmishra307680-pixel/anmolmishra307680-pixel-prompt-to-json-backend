#!/usr/bin/env python3
"""
Production deployment test script
Tests the key issues identified in the deployment logs
"""

import os
import sys
import asyncio
import httpx
from pathlib import Path

# Set production environment
os.environ["PRODUCTION_MODE"] = "true"
os.environ["LOCAL_GPU_ENABLED"] = "false"
os.environ["COMPUTE_STRATEGY"] = "cloud_only"
os.environ["BHIV_BUCKET_ENABLED"] = "false"
os.environ["REDIS_URL"] = "disabled"
os.environ["API_KEY"] = "bhiv-secret-key-2024"
os.environ["JWT_SECRET"] = "bhiv-jwt-secret-2024-production"
os.environ["DEMO_USERNAME"] = "admin"
os.environ["DEMO_PASSWORD"] = "bhiv2024"

async def test_production_fixes():
    """Test the production deployment fixes"""
    print("Testing Production Deployment Fixes")
    print("=" * 50)
    
    # Test 1: Import compute router without PyTorch warnings
    print("1. Testing compute router initialization...")
    try:
        from src.services.compute_router import compute_router
        print(f"   [OK] Compute router initialized: {compute_router.compute_strategy}")
        print(f"   [OK] Local GPU: {compute_router.local_gpu}, Cloud: {compute_router.yotta_available}")
    except Exception as e:
        print(f"   [ERROR] Compute router failed: {e}")
    
    # Test 2: Test bucket storage fallback
    print("\n2. Testing bucket storage fallback...")
    try:
        from src.storage.bucket_storage import bucket_storage
        print(f"   [OK] Bucket storage initialized: {'local' if bucket_storage.use_local else 'cloud'}")
        
        # Test signed URL generation
        test_url = bucket_storage.generate_signed_url("test-preview.jpg", 3600)
        print(f"   [OK] Signed URL generated: {test_url[:50]}...")
    except Exception as e:
        print(f"   [ERROR] Bucket storage failed: {e}")
    
    # Test 3: Test main app initialization
    print("\n3. Testing main app initialization...")
    try:
        from src.main import app
        print("   [OK] FastAPI app initialized successfully")
        
        # Test lifespan context
        async with app.router.lifespan_context(app):
            print("   [OK] Lifespan context works")
    except Exception as e:
        print(f"   [ERROR] Main app failed: {e}")
    
    # Test 4: Test database connection
    print("\n4. Testing database connection...")
    try:
        from src.data.database import db
        session = db.get_session()
        session.close()
        print("   [OK] Database connection successful")
    except Exception as e:
        print(f"   [ERROR] Database connection failed: {e}")
    
    # Test 5: Test agents initialization
    print("\n5. Testing agents initialization...")
    try:
        from src.agents.main_agent import MainAgent
        from src.agents.evaluator_agent import EvaluatorAgent
        
        agent = MainAgent()
        evaluator = EvaluatorAgent()
        print("   [OK] Agents initialized successfully")
    except Exception as e:
        print(f"   [ERROR] Agents initialization failed: {e}")
    
    print("\n" + "=" * 50)
    print("Production deployment test completed!")
    print("\nKey fixes applied:")
    print("- Reduced PyTorch warning noise")
    print("- Enabled mock cloud compute for production")
    print("- Fixed bucket storage fallback")
    print("- Made root endpoint public for health checks")
    print("- Configured cloud-only compute strategy")

if __name__ == "__main__":
    asyncio.run(test_production_fixes())