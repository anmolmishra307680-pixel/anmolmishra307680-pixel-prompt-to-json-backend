"""Preview management with signed URLs and bucket storage"""

import os
import time
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path
import json
import httpx

class PreviewManager:
    def __init__(self):
        self.bucket_url = os.getenv("BHIV_BUCKET_URL", "https://storage.bhiv.com")
        self.signing_key = os.getenv("PREVIEW_SIGNING_KEY", "dev-signing-key")
        self.preview_expiry = 3600  # 1 hour
        self.preview_cache = {}
        self._load_cache()
    
    def _load_cache(self):
        """Load preview cache from file"""
        cache_file = Path("logs/preview_cache.json")
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    self.preview_cache = json.load(f)
            except Exception:
                self.preview_cache = {}
    
    def _save_cache(self):
        """Save preview cache to file"""
        Path("logs").mkdir(exist_ok=True)
        try:
            with open("logs/preview_cache.json", 'w') as f:
                json.dump(self.preview_cache, f, indent=2)
        except Exception:
            pass
    
    def _generate_signature(self, spec_id: str, expires: int) -> str:
        """Generate HMAC signature for URL"""
        message = f"{spec_id}:{expires}"
        signature = hmac.new(
            self.signing_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _is_signature_valid(self, spec_id: str, expires: int, signature: str) -> bool:
        """Validate HMAC signature"""
        expected = self._generate_signature(spec_id, expires)
        return hmac.compare_digest(expected, signature)
    
    async def generate_preview(self, spec_data: Dict[str, Any]) -> str:
        """Generate signed preview URL"""
        spec_id = spec_data.get('spec_id', 'unknown')
        
        # Check cache first
        if spec_id in self.preview_cache:
            cached = self.preview_cache[spec_id]
            if cached['expires'] > time.time():
                return cached['signed_url']
        
        # Generate new preview
        expires = int(time.time() + self.preview_expiry)
        signature = self._generate_signature(spec_id, expires)
        
        # Create signed URL
        signed_url = f"{self.bucket_url}/preview/{spec_id}.png?expires={expires}&signature={signature}"
        
        # Upload to bucket (mock implementation)
        await self._upload_preview(spec_id, spec_data)
        
        # Cache the result
        self.preview_cache[spec_id] = {
            'signed_url': signed_url,
            'expires': expires,
            'created_at': time.time()
        }
        self._save_cache()
        
        return signed_url
    
    async def _upload_preview(self, spec_id: str, spec_data: Dict[str, Any]):
        """Upload preview to BHIV bucket"""
        try:
            # Mock preview generation - would use actual 3D rendering
            preview_data = self._generate_mock_preview(spec_data)
            
            # Upload to bucket (mock implementation)
            upload_url = f"{self.bucket_url}/upload/preview/{spec_id}.png"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.put(
                    upload_url,
                    content=preview_data,
                    headers={"Content-Type": "image/png"}
                )
                response.raise_for_status()
                
        except Exception as e:
            print(f"Preview upload failed: {e}")
            # Continue with signed URL even if upload fails
    
    def _generate_mock_preview(self, spec_data: Dict[str, Any]) -> bytes:
        """Generate mock preview data"""
        # Mock PNG data - would be actual 3D render
        return b"mock_png_data_for_preview"
    
    def verify_preview_url(self, spec_id: str, expires: int, signature: str) -> bool:
        """Verify signed preview URL"""
        if expires < time.time():
            return False
        return self._is_signature_valid(spec_id, expires, signature)
    
    async def refresh_preview(self, spec_id: str, spec_data: Dict[str, Any]) -> str:
        """Force refresh preview"""
        # Remove from cache
        if spec_id in self.preview_cache:
            del self.preview_cache[spec_id]
        
        # Generate new preview
        return await self.generate_preview(spec_data)
    
    def cleanup_stale_previews(self):
        """Remove expired previews from cache"""
        current_time = time.time()
        stale_keys = [
            key for key, value in self.preview_cache.items()
            if value['expires'] < current_time
        ]
        
        for key in stale_keys:
            del self.preview_cache[key]
        
        if stale_keys:
            self._save_cache()
        
        return len(stale_keys)

# Global instance
preview_manager = PreviewManager()