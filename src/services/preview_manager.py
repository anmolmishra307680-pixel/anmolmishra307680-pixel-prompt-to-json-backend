"""Enhanced preview management with BHIV bucket storage and Three.js compatibility"""

import os
import time
from typing import Dict, Any
from pathlib import Path
import json
from src.storage.bucket_storage import bucket_storage
from src.services.preview_generator import preview_generator

class PreviewManager:
    """Enhanced preview manager with bucket storage integration"""
    
    def __init__(self):
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
    
    async def generate_preview(self, spec_data: Dict[str, Any]) -> str:
        """Generate preview with bucket storage and signed URL"""
        spec_id = spec_data.get('spec_id', f"preview_{int(time.time())}")
        
        # Check cache first
        if spec_id in self.preview_cache:
            cached = self.preview_cache[spec_id]
            if cached['expires'] > time.time():
                return cached['signed_url']
        
        # Generate preview using enhanced preview generator
        signed_url = await preview_generator.generate_preview(spec_data)
        
        # Cache the result
        self.preview_cache[spec_id] = {
            'signed_url': signed_url,
            'expires': time.time() + 86400,  # 24 hours
            'created_at': time.time()
        }
        self._save_cache()
        
        return signed_url
    
    def verify_preview_url(self, spec_id: str, expires: int, signature: str) -> bool:
        """Verify signed preview URL using bucket storage"""
        return bucket_storage.verify_signed_url(spec_id, expires, signature)
    
    async def refresh_preview(self, spec_id: str, spec_data: Dict[str, Any]) -> str:
        """Force refresh preview"""
        # Remove from cache
        if spec_id in self.preview_cache:
            del self.preview_cache[spec_id]
        
        # Generate new preview
        return await self.generate_preview(spec_data)
    
    def cleanup_stale_previews(self) -> int:
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
    
    def get_threejs_data(self, spec_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get Three.js formatted data for viewer"""
        return preview_generator.format_for_threejs(spec_data)
    
    def generate_viewer_html(self, spec_data: Dict[str, Any]) -> str:
        """Generate HTML for Three.js viewer"""
        return preview_generator.generate_viewer_html(spec_data)

# Global instance
preview_manager = PreviewManager()