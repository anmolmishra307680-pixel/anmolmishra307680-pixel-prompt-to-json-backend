"""Preview service for signed GLB URLs"""

import os
import hashlib
import time
from typing import Dict, Any

class PreviewService:
    def __init__(self):
        self.bucket_url = os.getenv("BHIV_BUCKET_URL", "https://bhiv-bucket.s3.amazonaws.com")
        self.secret_key = os.getenv("PREVIEW_SECRET", "bhiv-preview-secret")
    
    def generate_signed_glb_url(self, spec_id: str, expires_in: int = 3600) -> str:
        """Generate signed GLB URL from BHIV bucket"""
        expires = int(time.time()) + expires_in
        
        # Create signature
        message = f"{spec_id}:{expires}"
        signature = hashlib.sha256(f"{message}:{self.secret_key}".encode()).hexdigest()[:16]
        
        return f"{self.bucket_url}/previews/{spec_id}.glb?expires={expires}&signature={signature}"
    
    def trigger_preview(self, spec_data: Dict[str, Any]) -> str:
        """Generate preview and return signed URL"""
        spec_id = spec_data.get("spec_id", "default")
        
        # Mock GLB generation (replace with actual 3D rendering)
        print(f"[PREVIEW] Generating GLB for spec {spec_id}")
        
        return self.generate_signed_glb_url(spec_id)

preview_service = PreviewService()