#!/usr/bin/env python3
"""
Debug BHIV bucket configuration
"""

import os

print("BHIV Bucket Configuration Debug")
print("=" * 40)

# Check all BHIV-related environment variables
bhiv_vars = [
    "BHIV_BUCKET_ENABLED",
    "BHIV_BUCKET_NAME", 
    "BHIV_ACCESS_KEY",
    "BHIV_SECRET_KEY",
    "BHIV_ENDPOINT",
    "BHIV_REGION"
]

for var in bhiv_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive keys
        if "KEY" in var:
            display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***MASKED***"
        else:
            display_value = value
        print(f"{var}: {display_value}")
    else:
        print(f"{var}: NOT SET")

print("\nBucket Logic Check:")
bucket_enabled = os.getenv("BHIV_BUCKET_ENABLED", "false").lower() == "true"
access_key = os.getenv("BHIV_ACCESS_KEY")
secret_key = os.getenv("BHIV_SECRET_KEY")

print(f"BHIV_BUCKET_ENABLED: {bucket_enabled}")
print(f"Has ACCESS_KEY: {bool(access_key)}")
print(f"Has SECRET_KEY: {bool(secret_key)}")

use_local = not (bucket_enabled and access_key and secret_key)
print(f"Will use local storage: {use_local}")

if use_local:
    if not bucket_enabled:
        print("Reason: BHIV Bucket is disabled")
    elif not access_key:
        print("Reason: BHIV_ACCESS_KEY not set")
    elif not secret_key:
        print("Reason: BHIV_SECRET_KEY not set")
    else:
        print("Reason: Unknown")
else:
    print("BHIV Bucket should be used!")