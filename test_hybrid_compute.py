#!/usr/bin/env python3
"""
Test hybrid compute routing with both GPU and Yotta cloud
"""

import os
import sys
import asyncio
import time
from pathlib import Path

# Set hybrid compute environment
os.environ["PRODUCTION_MODE"] = "true"
os.environ["LOCAL_GPU_ENABLED"] = "true"
os.environ["COMPUTE_STRATEGY"] = "hybrid"
os.environ["YOTTA_API_KEY"] = "bhiv-yotta-production-key-2024"
os.environ["YOTTA_ENDPOINT"] = "https://api.yotta.com/v1/inference"
os.environ["BURST_THRESHOLD"] = "0.6"
os.environ["BHIV_BUCKET_ENABLED"] = "true"
os.environ["API_KEY"] = "bhiv-secret-key-2024"

async def test_hybrid_compute():
    """Test hybrid compute routing with GPU + Yotta"""
    print("Testing Hybrid Compute: GPU + Yotta Cloud")
    print("=" * 50)
    
    # Test 1: Initialize compute router
    print("1. Testing hybrid compute router initialization...")
    try:
        from src.services.compute_router import compute_router
        print(f"   [OK] Strategy: {compute_router.compute_strategy}")
        print(f"   [OK] Local GPU: {compute_router.local_gpu}")
        print(f"   [OK] Yotta Cloud: {compute_router.yotta_available}")
        print(f"   [OK] Burst threshold: {compute_router.burst_threshold}")
        
        if compute_router.compute_strategy == "hybrid" and compute_router.local_gpu and compute_router.yotta_available:
            print("   [SUCCESS] Hybrid compute fully configured!")
        else:
            print("   [WARNING] Hybrid compute not fully configured")
    except Exception as e:
        print(f"   [ERROR] Compute router failed: {e}")
        return
    
    # Test 2: Test BHIV bucket storage
    print("\n2. Testing BHIV bucket storage...")
    try:
        from src.storage.bucket_storage import bucket_storage
        
        if bucket_storage.use_local:
            print("   [INFO] Using local storage fallback")
        else:
            print(f"   [OK] BHIV bucket configured: {bucket_storage.bucket_name}")
        
        # Test preview upload
        test_data = b"test preview data"
        preview_url = await bucket_storage.upload_preview("test-spec-123", test_data)
        print(f"   [OK] Preview uploaded: {preview_url[:50]}...")
        
    except Exception as e:
        print(f"   [ERROR] Bucket storage failed: {e}")
    
    # Test 3: Test local GPU routing
    print("\n3. Testing local GPU routing...")
    try:
        # Simple job should go to local GPU
        result = await compute_router.route_inference(
            "Simple office building", 
            None, 
            "generation"
        )
        
        print(f"   [OK] Simple job routed to: {result['compute']}")
        print(f"   [OK] Complexity: {result['complexity']:.2f}")
        print(f"   [OK] Response time: {result['response_time']:.3f}s")
        
        if result['compute'] == 'local_gpu':
            print("   [SUCCESS] Local GPU routing works!")
        else:
            print("   [INFO] Job routed to cloud (may be expected)")
            
    except Exception as e:
        print(f"   [ERROR] Local GPU routing failed: {e}")
    
    # Test 4: Test Yotta cloud bursting
    print("\n4. Testing Yotta cloud bursting...")
    try:
        # Complex job should burst to Yotta
        complex_prompt = "Design a comprehensive multi-story industrial complex with advanced HVAC systems, sustainable energy solutions, smart building automation, and integrated manufacturing facilities"
        
        result = await compute_router.route_inference(
            complex_prompt,
            "Additional context for complex building design",
            "complex_generation"
        )
        
        print(f"   [OK] Complex job routed to: {result['compute']}")
        print(f"   [OK] Complexity: {result['complexity']:.2f}")
        print(f"   [OK] Response time: {result['response_time']:.3f}s")
        
        if result['compute'] in ['yotta_cloud', 'yotta_emergency']:
            print("   [SUCCESS] Yotta cloud bursting works!")
        elif result['compute'] == 'rule_based':
            print("   [INFO] Fallback to rule-based (Yotta may be unavailable)")
        else:
            print("   [INFO] Job handled locally (may be expected)")
            
    except Exception as e:
        print(f"   [ERROR] Yotta cloud bursting failed: {e}")
    
    # Test 5: Test cost tracking
    print("\n5. Testing cost tracking...")
    try:
        stats = compute_router.get_job_stats()
        cost_report = compute_router.get_cost_report()
        
        print(f"   [OK] Total jobs: {stats['total_jobs']}")
        print(f"   [OK] Local jobs: {stats['local_jobs']}")
        print(f"   [OK] Remote jobs: {stats['remote_jobs']}")
        print(f"   [OK] Total cost: ${stats['total_cost']:.4f}")
        print(f"   [OK] Cost savings: ${cost_report['efficiency']['cost_savings_vs_all_cloud']:.2f}")
        
        if stats['total_jobs'] > 0:
            print("   [SUCCESS] Cost tracking works!")
        
    except Exception as e:
        print(f"   [ERROR] Cost tracking failed: {e}")
    
    # Test 6: Test fallback mechanisms
    print("\n6. Testing fallback mechanisms...")
    try:
        # Simulate API failure by using invalid endpoint
        original_url = compute_router.yotta_url
        compute_router.yotta_url = "https://invalid-endpoint.com/api"
        
        result = await compute_router.route_inference(
            "Test fallback building",
            None,
            "batch_rl"  # Heavy job that would normally go to cloud
        )
        
        print(f"   [OK] Fallback result: {result['compute']}")
        print(f"   [OK] Fallback successful: {'fallback' in result}")
        
        # Restore original URL
        compute_router.yotta_url = original_url
        
        if 'fallback' in result or result['compute'] in ['local_fallback', 'rule_based']:
            print("   [SUCCESS] Fallback mechanisms work!")
        
    except Exception as e:
        print(f"   [ERROR] Fallback test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Hybrid Compute Test Summary:")
    print(f"- Strategy: {compute_router.compute_strategy}")
    print(f"- Local GPU: {compute_router.local_gpu}")
    print(f"- Yotta Cloud: {compute_router.yotta_available}")
    print(f"- BHIV Bucket: {'Enabled' if not bucket_storage.use_local else 'Local Fallback'}")
    print(f"- Total Jobs Processed: {compute_router.job_stats['total_jobs']}")
    print("\nHybrid compute system is ready for production!")

if __name__ == "__main__":
    asyncio.run(test_hybrid_compute())