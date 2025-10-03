#!/usr/bin/env python3
"""Test token blacklist functionality"""

import sys
import os
sys.path.append('src')

from auth.jwt_auth import jwt_auth

# Test token creation and blacklist
user_data = {"username": "admin"}
tokens = jwt_auth.create_tokens(user_data)

print("=== Token Blacklist Test ===")
print(f"Access Token: {tokens.access_token[:50]}...")
print(f"Refresh Token: {tokens.refresh_token[:50]}...")

# Verify access token works
payload = jwt_auth.verify_token(tokens.access_token, "access")
print(f"[OK] Access token valid: {payload['sub'] if payload else 'INVALID'}")

# Blacklist the access token
success = jwt_auth.blacklist_token(tokens.access_token)
print(f"[OK] Token blacklisted: {success}")

# Try to verify blacklisted token
payload_after = jwt_auth.verify_token(tokens.access_token, "access")
print(f"[TEST] Blacklisted token valid: {payload_after['sub'] if payload_after else 'INVALID (GOOD)'}")

# Test refresh token blacklist
print("\n=== Refresh Token Test ===")
new_tokens = jwt_auth.refresh_access_token(tokens.refresh_token)
if new_tokens:
    print(f"[OK] New tokens created")
    
    # Try old refresh token again
    old_refresh_result = jwt_auth.refresh_access_token(tokens.refresh_token)
    print(f"[TEST] Old refresh token works: {'YES (BAD)' if old_refresh_result else 'NO (GOOD)'}")
else:
    print("[ERROR] Refresh failed")

print(f"\nBlacklist size: {len(jwt_auth.blacklisted_tokens)}")
print("Blacklisted tokens:", list(jwt_auth.blacklisted_tokens))