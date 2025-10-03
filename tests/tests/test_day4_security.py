#!/usr/bin/env python3
"""Test script for Day 4 Security, Monitoring, Compute Routing"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_jwt_auth():
    """Test JWT authentication system"""
    print("Testing JWT Authentication...")
    try:
        from src.auth.jwt_auth import jwt_auth
        
        # Test token creation
        user_data = {"username": "testuser"}
        tokens = jwt_auth.create_tokens(user_data)
        
        assert tokens.access_token is not None, "Access token not created"
        assert tokens.refresh_token is not None, "Refresh token not created"
        assert tokens.token_type == "bearer", "Wrong token type"
        
        print("[OK] JWT Authentication working")
    except Exception as e:
        print(f"[FAIL] JWT Authentication failed: {e}")
        assert False, f"JWT Authentication failed: {e}"

def test_compute_router():
    """Test compute routing system"""
    print("Testing Compute Router...")
    try:
        from src.services.compute_router import compute_router
        
        # Test router initialization
        assert compute_router is not None, "Router not initialized"
        
        print("[OK] Compute Router working")
    except Exception as e:
        print(f"[FAIL] Compute Router failed: {e}")
        assert False, f"Compute Router failed: {e}"

def test_monitoring():
    """Test monitoring system"""
    print("Testing Monitoring...")
    try:
        from src.utils.system_monitoring import system_monitor
        
        # Test counters
        initial_requests = system_monitor.request_count
        system_monitor.increment_requests()
        assert system_monitor.request_count == initial_requests + 1, "Request counter failed"
        
        print("[OK] Monitoring working")
    except Exception as e:
        print(f"[FAIL] Monitoring failed: {e}")
        assert False, f"Monitoring failed: {e}"