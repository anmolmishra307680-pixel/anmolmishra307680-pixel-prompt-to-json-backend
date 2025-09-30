"""Geometry file storage using Nipun's bucket"""

import os
import uuid
from pathlib import Path
from typing import Optional, Dict, Any
import json

class GeometryStorage:
    def __init__(self):
        self.bucket_url = os.getenv("NIPUN_BUCKET_URL", "https://storage.example.com")
        self.local_storage = Path("geometry")
        self.local_storage.mkdir(exist_ok=True)
        self.case_mapping = {}
        self._load_mappings()
    
    def _load_mappings(self):
        """Load case_id to project_id mappings"""
        mapping_file = self.local_storage / "case_mappings.json"
        if mapping_file.exists():
            try:
                with open(mapping_file, 'r') as f:
                    self.case_mapping = json.load(f)
            except Exception:
                self.case_mapping = {}
    
    def _save_mappings(self):
        """Save case_id to project_id mappings"""
        mapping_file = self.local_storage / "case_mappings.json"
        try:
            with open(mapping_file, 'w') as f:
                json.dump(self.case_mapping, f, indent=2)
        except Exception:
            pass
    
    def store_geometry(self, case_id: str, project_id: str, file_data: bytes, file_type: str = "stl") -> str:
        """Store geometry file and return URL"""
        # Map case_id to project_id
        self.case_mapping[case_id] = project_id
        self._save_mappings()
        
        # Store file locally (would upload to Nipun's bucket in production)
        filename = f"{case_id}.{file_type}"
        file_path = self.local_storage / filename
        
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        # Return URL (would be bucket URL in production)
        return f"/geometry/{filename}"
    
    def get_geometry_url(self, case_id: str) -> Optional[str]:
        """Get geometry file URL for case_id"""
        for ext in ['stl', 'zip']:
            filename = f"{case_id}.{ext}"
            if (self.local_storage / filename).exists():
                return f"/geometry/{filename}"
        return None
    
    def get_project_id(self, case_id: str) -> Optional[str]:
        """Get project_id for case_id"""
        return self.case_mapping.get(case_id)

# Global instance
geometry_storage = GeometryStorage()