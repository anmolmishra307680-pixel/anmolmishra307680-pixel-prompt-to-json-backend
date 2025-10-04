#!/usr/bin/env python3
"""
Test environment variable loading for production deployment
"""

import os

def test_env_loading():
    """Test environment variable loading logic"""
    print("Testing Environment Variable Loading")
    print("=" * 40)
    
    # Simulate production environment
    os.environ["PRODUCTION_MODE"] = "true"
    os.environ["LOCAL_GPU_ENABLED"] = "true"
    os.environ["COMPUTE_STRATEGY"] = "hybrid"
    os.environ["YOTTA_API_KEY"] = "bhiv-yotta-production-key-2024"
    os.environ["BHIV_BUCKET_ENABLED"] = "true"
    os.environ["BHIV_BUCKET_NAME"] = "bhiv-production-storage"
    os.environ["BHIV_ACCESS_KEY"] = "BHIV_PROD_ACCESS_KEY_2024"
    os.environ["BHIV_SECRET_KEY"] = "bhiv-secret-storage-key-2024-production"
    
    print("1. Set production environment variables")
    
    # Test the environment loading logic
    print("\n2. Testing environment loading...")
    try:
        from src.main import app
        print("   [OK] Main.py loaded successfully")
    except Exception as e:
        print(f"   [ERROR] Failed to load main.py: {e}")
        return
    
    # Check key environment variables
    print("\n3. Checking environment variables...")
    env_vars = [
        "PRODUCTION_MODE",
        "LOCAL_GPU_ENABLED", 
        "COMPUTE_STRATEGY",
        "YOTTA_API_KEY",
        "BHIV_BUCKET_ENABLED",
        "BHIV_BUCKET_NAME",
        "BHIV_ACCESS_KEY"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            display_value = f"{value[:8]}..." if "KEY" in var else value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: NOT SET")
    
    # Test compute router
    print("\n4. Testing compute router...")
    try:
        from src.services.compute_router import compute_router
        print(f"   Strategy: {compute_router.compute_strategy}")
        print(f"   Local GPU: {compute_router.local_gpu}")
        print(f"   Yotta: {compute_router.yotta_available}")
        
        if compute_router.compute_strategy == "hybrid":
            print("   ✅ Hybrid compute configured")
        else:
            print("   ❌ Hybrid compute not configured")
            
    except Exception as e:
        print(f"   ❌ Compute router error: {e}")
    
    # Test BHIV bucket
    print("\n5. Testing BHIV bucket...")
    try:
        from src.storage.bucket_storage import bucket_storage
        print(f"   Bucket: {bucket_storage.bucket_name}")
        print(f"   Using local: {bucket_storage.use_local}")
        
        if not bucket_storage.use_local:
            print("   ✅ BHIV bucket configured")
        else:
            print("   ❌ BHIV bucket using local fallback")
            
    except Exception as e:
        print(f"   ❌ BHIV bucket error: {e}")
    
    print("\n" + "=" * 40)
    print("Environment loading test completed!")

if __name__ == "__main__":
    test_env_loading()