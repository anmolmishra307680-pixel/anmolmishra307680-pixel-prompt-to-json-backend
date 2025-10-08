"""Geometry storage service for BHIV bucket integration"""

import os
from pathlib import Path
from typing import Optional
import uuid

class GeometryStorage:
    """Service for storing geometry files (.stl, .zip) to BHIV bucket"""
    
    def __init__(self):
        self.storage_dir = Path("geometry")
        self.storage_dir.mkdir(exist_ok=True)
        self.bucket_url = os.getenv("BHIV_BUCKET_URL", "https://bhiv-bucket.s3.amazonaws.com")
    
    def store_geometry(self, case_id: str, project_id: str, geometry_data: bytes, file_format: str = "stl") -> str:
        """Store geometry file and return URL"""
        try:
            # Generate filename
            filename = f"{case_id}.{file_format}"
            local_path = self.storage_dir / filename
            
            # Save file locally (mock BHIV bucket)
            with open(local_path, 'wb') as f:
                f.write(geometry_data)
            
            # Return mock bucket URL
            bucket_url = f"{self.bucket_url}/geometry/{project_id}/{filename}"
            
            print(f"[GEOMETRY] Stored {filename} for case {case_id}")
            return bucket_url
            
        except Exception as e:
            print(f"[ERROR] Geometry storage failed: {e}")
            return f"/geometry/{case_id}.{file_format}"  # Fallback local URL
    
    def get_geometry_url(self, case_id: str, file_format: str = "stl") -> Optional[str]:
        """Get geometry URL for case_id"""
        filename = f"{case_id}.{file_format}"
        local_path = self.storage_dir / filename
        
        if local_path.exists():
            return f"/geometry/{filename}"
        return None
    
    def delete_geometry(self, case_id: str, file_format: str = "stl") -> bool:
        """Delete geometry file"""
        try:
            filename = f"{case_id}.{file_format}"
            local_path = self.storage_dir / filename
            
            if local_path.exists():
                local_path.unlink()
                print(f"[GEOMETRY] Deleted {filename}")
                return True
            return False
            
        except Exception as e:
            print(f"[ERROR] Geometry deletion failed: {e}")
            return False

# Global instance
geometry_storage = GeometryStorage()