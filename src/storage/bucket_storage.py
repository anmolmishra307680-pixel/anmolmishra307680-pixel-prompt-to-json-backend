#!/usr/bin/env python3
"""BHIV Bucket storage integration with signed URL generation"""

import os
import json
import hashlib
import hmac
import base64
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from pathlib import Path
import httpx

class BHIVBucketStorage:
    """BHIV Bucket storage with signed URL generation"""
    
    def __init__(self):
        self.bucket_name = os.getenv("BHIV_BUCKET_NAME", "bhiv-previews")
        self.access_key = os.getenv("BHIV_ACCESS_KEY")
        self.secret_key = os.getenv("BHIV_SECRET_KEY")
        self.endpoint = os.getenv("BHIV_ENDPOINT", "https://storage.bhiv.ai")
        self.region = os.getenv("BHIV_REGION", "us-east-1")
        
        # Fallback to local storage if bucket not configured
        self.use_local = not (self.access_key and self.secret_key)
        if self.use_local:
            print("[INFO] BHIV Bucket not configured, using local storage fallback")
            self.local_storage = Path("preview_storage")
            self.local_storage.mkdir(exist_ok=True)
    
    def generate_signed_url(self, object_key: str, expires_in: int = 3600) -> str:
        """Generate signed URL for object access"""
        if self.use_local:
            return self._generate_local_signed_url(object_key, expires_in)
        
        # Generate AWS S3-style signed URL
        expires = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        expires_timestamp = int(expires.timestamp())
        
        # Create string to sign
        string_to_sign = f"GET\n\n\n{expires_timestamp}\n/{self.bucket_name}/{object_key}"
        
        # Generate signature
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
        ).decode('utf-8')
        
        # Build signed URL
        signed_url = (
            f"{self.endpoint}/{self.bucket_name}/{object_key}"
            f"?AWSAccessKeyId={self.access_key}"
            f"&Expires={expires_timestamp}"
            f"&Signature={signature.replace('+', '%2B').replace('/', '%2F').replace('=', '%3D')}"
        )
        
        return signed_url
    
    def _generate_local_signed_url(self, object_key: str, expires_in: int) -> str:
        """Generate signed URL for local storage"""
        expires = int((datetime.now(timezone.utc) + timedelta(seconds=expires_in)).timestamp())
        
        # Create signature for local URLs
        payload = f"{object_key}:{expires}"
        signature = hashlib.sha256(
            f"{payload}:{os.getenv('API_KEY', 'fallback-key')}".encode()
        ).hexdigest()[:16]
        
        return f"/api/v1/preview/local/{object_key}?expires={expires}&signature={signature}"
    
    async def upload_preview(self, spec_id: str, preview_data: bytes, content_type: str = "image/jpeg") -> str:
        """Upload preview to bucket storage"""
        object_key = f"previews/{spec_id}.jpg"
        
        if self.use_local:
            return await self._upload_local(object_key, preview_data)
        
        try:
            # Upload to BHIV bucket
            upload_url = f"{self.endpoint}/{self.bucket_name}/{object_key}"
            
            headers = {
                "Content-Type": content_type,
                "Authorization": self._generate_auth_header("PUT", object_key)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.put(upload_url, content=preview_data, headers=headers)
                response.raise_for_status()
            
            # Generate signed URL for access
            signed_url = self.generate_signed_url(object_key, expires_in=86400)  # 24 hours
            return signed_url
            
        except Exception as e:
            print(f"[WARN] Bucket upload failed: {e}, using local fallback")
            return await self._upload_local(object_key, preview_data)
    
    async def _upload_local(self, object_key: str, preview_data: bytes) -> str:
        """Upload to local storage"""
        file_path = self.local_storage / object_key.replace("/", "_")
        file_path.parent.mkdir(exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(preview_data)
        
        return self._generate_local_signed_url(object_key.replace("/", "_"), 86400)
    
    def _generate_auth_header(self, method: str, object_key: str) -> str:
        """Generate authorization header for bucket requests"""
        timestamp = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        string_to_sign = f"{method}\n\nimage/jpeg\n{timestamp}\n/{self.bucket_name}/{object_key}"
        
        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
        ).decode('utf-8')
        
        return f"AWS {self.access_key}:{signature}"
    
    def verify_signed_url(self, object_key: str, expires: int, signature: str) -> bool:
        """Verify signed URL signature"""
        if self.use_local:
            return self._verify_local_signature(object_key, expires, signature)
        
        # Verify bucket signed URL
        if datetime.now(timezone.utc).timestamp() > expires:
            return False
        
        # Recreate signature
        string_to_sign = f"GET\n\n\n{expires}\n/{self.bucket_name}/{object_key}"
        expected_signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
        ).decode('utf-8')
        
        return signature == expected_signature
    
    def _verify_local_signature(self, object_key: str, expires: int, signature: str) -> bool:
        """Verify local signed URL signature"""
        if datetime.now(timezone.utc).timestamp() > expires:
            return False
        
        payload = f"{object_key}:{expires}"
        expected_signature = hashlib.sha256(
            f"{payload}:{os.getenv('API_KEY', 'fallback-key')}".encode()
        ).hexdigest()[:16]
        
        return signature == expected_signature

# Global instance
bucket_storage = BHIVBucketStorage()