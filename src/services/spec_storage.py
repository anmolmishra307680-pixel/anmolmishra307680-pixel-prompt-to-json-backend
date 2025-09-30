"""Simple in-memory spec storage for Day 2 implementation"""

from typing import Dict, Any, Optional
import json
from pathlib import Path

class SpecStorage:
    def __init__(self):
        self.specs = {}
        self.storage_file = Path("spec_storage.json")
        self._load_specs()
    
    def _load_specs(self):
        """Load specs from file"""
        if self.storage_file.exists():
            try:
                with open(self.storage_file, 'r') as f:
                    self.specs = json.load(f)
            except Exception:
                self.specs = {}
    
    def _save_specs(self):
        """Save specs to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.specs, f, indent=2)
        except Exception:
            pass
    
    def store_spec(self, spec_id: str, spec_data: Dict[str, Any]):
        """Store a spec"""
        self.specs[spec_id] = spec_data
        self._save_specs()
    
    def get_spec(self, spec_id: str) -> Optional[Dict[str, Any]]:
        """Get a spec by ID"""
        return self.specs.get(spec_id)
    
    def update_spec(self, spec_id: str, updated_spec: Dict[str, Any]):
        """Update an existing spec"""
        if spec_id in self.specs:
            self.specs[spec_id] = updated_spec
            self._save_specs()
            return True
        return False

# Global instance
spec_storage = SpecStorage()