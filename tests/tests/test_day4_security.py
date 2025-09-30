#!/usr/bin/env python3
"""Test script for Day 4 Security, Monitoring, Compute Routing"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_jwt_auth():
    """Test JWT authentication system"""
    print("Testing JWT Authentication...")
    try:
        from src.auth_v2.jwt_auth import JWTAuth, LoginRequest, TokenResponse
        
        auth = JWTAuth()
        
        # Test token creation
        user_data = {"username": "testuser"}
        tokens = auth.create_tokens(user_data)
        
        assert tokens.access_token is not None, "Access token not created"
        assert tokens.refresh_token is not None, "Refresh token not created"
        assert tokens.token_type == "bearer", "Wrong token type"
        
        # Test token verification
        access_payload = auth.verify_token(tokens.access_token, "access")
        assert access_payload is not None, "Access token verification failed"
        assert access_payload["sub"] == "testuser", "Wrong username in token"
        
        # Test refresh token
        new_tokens = auth.refresh_access_token(tokens.refresh_token)
        assert new_tokens is not None, "Refresh token failed"
        
        print("[OK] JWT Authentication working")
        print(f"   Access token created: {len(tokens.access_token)} chars")
        print(f"   Refresh token created: {len(tokens.refresh_token)} chars")
        print(f"   Token expires in: {tokens.expires_in} seconds")
        
        return True
    except Exception as e:
        print(f"[FAIL] JWT Authentication failed: {e}")
        return False

def test_compute_router():
    """Test compute routing system"""
    print("Testing Compute Router...")
    try:
        from src.compute_router import ComputeRouter
        
        router = ComputeRouter()
        
        # Test complexity calculation
        simple_prompt = "simple building"
        complex_prompt = "detailed comprehensive advanced building with complex requirements"
        
        simple_complexity = router._calculate_complexity(simple_prompt)
        complex_complexity = router._calculate_complexity(complex_prompt)
        
        assert simple_complexity < complex_complexity, "Complexity calculation failed"
        
        # Test job logging
        router._log_job("test", 50, "local_rtx3060", 0.05)
        stats = router.get_job_stats()
        
        assert stats["total_jobs"] >= 1, "Job logging failed"
        assert stats["total_cost"] > 0, "Cost calculation failed"
        
        print("[OK] Compute Router working")
        print(f"   Simple complexity: {simple_complexity}")
        print(f"   Complex complexity: {complex_complexity}")
        print(f"   Job stats: {stats}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Compute Router failed: {e}")
        return False

async def test_compute_routing():
    """Test actual compute routing"""
    print("Testing Compute Routing...")
    try:
        from src.compute_router import compute_router
        
        # Test simple prompt (should use local)
        simple_result = await compute_router.route_inference("simple test", None, "test")
        
        assert simple_result["compute_type"] == "local_rtx3060", "Simple routing failed"
        assert simple_result["result"] is not None, "No result returned"
        
        # Test complex prompt (would use Yotta but falls back to local)
        complex_prompt = "detailed comprehensive advanced building with complex architectural requirements"
        complex_result = await compute_router.route_inference(complex_prompt, None, "test")
        
        assert complex_result["result"] is not None, "Complex routing failed"
        assert complex_result["complexity"] > simple_result["complexity"], "Complexity not calculated"
        
        print("[OK] Compute Routing working")
        print(f"   Simple: {simple_result['compute_type']} (complexity: {simple_result['complexity']})")
        print(f"   Complex: {complex_result['compute_type']} (complexity: {complex_result['complexity']})")
        
        return True
    except Exception as e:
        print(f"[FAIL] Compute Routing failed: {e}")
        return False

def test_monitoring():
    """Test monitoring system"""
    print("Testing Monitoring...")
    try:
        from src.system_monitoring import system_monitor
        
        # Test counters
        initial_requests = system_monitor.request_count
        system_monitor.increment_requests()
        assert system_monitor.request_count == initial_requests + 1, "Request counter failed"
        
        initial_errors = system_monitor.error_count
        system_monitor.increment_errors()
        assert system_monitor.error_count == initial_errors + 1, "Error counter failed"
        
        # Test metrics
        health_metrics = system_monitor.get_health_metrics()
        assert "status" in health_metrics, "Health metrics missing status"
        assert "uptime_seconds" in health_metrics, "Health metrics missing uptime"
        
        # Test Prometheus format
        prometheus_metrics = system_monitor.get_prometheus_metrics()
        assert "http_requests_total" in prometheus_metrics, "Prometheus metrics missing"
        
        print("[OK] Monitoring working")
        print(f"   Requests: {system_monitor.request_count}")
        print(f"   Errors: {system_monitor.error_count}")
        print(f"   Status: {health_metrics['status']}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Monitoring failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("Day 4: Security, Monitoring, Compute Routing - Test Suite")
    print("=" * 60)
    
    sync_tests = [
        test_jwt_auth,
        test_compute_router,
        test_monitoring
    ]
    
    async_tests = [
        test_compute_routing
    ]
    
    passed = 0
    total = len(sync_tests) + len(async_tests)
    
    # Run sync tests
    for test in sync_tests:
        if test():
            passed += 1
        print()
    
    # Run async tests
    for test in async_tests:
        if await test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Day 4 implementation is ready.")
        return True
    else:
        print("Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)