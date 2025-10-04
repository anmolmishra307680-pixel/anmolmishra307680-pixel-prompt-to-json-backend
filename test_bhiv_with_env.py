#!/usr/bin/env python3
"""
Test BHIV bucket with proper environment loading
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_file = Path("config/.env")
if env_file.exists():
    load_dotenv(env_file)
    print(f"Loaded environment from: {env_file}")
else:
    print("No .env file found")

print("\nBHIV Bucket Configuration After Loading .env")
print("=" * 50)

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

print("\nTesting BHIV Bucket Storage:")
try:
    from src.storage.bucket_storage import BHIVBucketStorage
    
    # Create new instance with loaded environment
    bucket = BHIVBucketStorage()
    
    print(f"Bucket Name: {bucket.bucket_name}")
    print(f"Endpoint: {bucket.endpoint}")
    print(f"Using Local Storage: {bucket.use_local}")
    
    if not bucket.use_local:
        print("✅ BHIV Bucket is properly configured!")
        
        # Test signed URL generation
        test_url = bucket.generate_signed_url("test-preview.jpg", 3600)
        print(f"Test Signed URL: {test_url[:80]}...")
        
    else:
        print("❌ BHIV Bucket is using local storage fallback")
        
        # Check why
        bucket_enabled = os.getenv("BHIV_BUCKET_ENABLED", "false").lower() == "true"
        access_key = os.getenv("BHIV_ACCESS_KEY")
        secret_key = os.getenv("BHIV_SECRET_KEY")
        
        print(f"Enabled: {bucket_enabled}")
        print(f"Has Access Key: {bool(access_key)}")
        print(f"Has Secret Key: {bool(secret_key)}")
        
except Exception as e:
    print(f"Error testing BHIV bucket: {e}")

print("\n" + "=" * 50)