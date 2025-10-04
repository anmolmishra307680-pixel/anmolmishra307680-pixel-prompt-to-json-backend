"""API Contract V2 Implementation - Helper Functions"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Storage directories
SPEC_STORAGE_DIR = Path("spec_storage")
ITERATION_LOGS_DIR = Path("iteration_logs")

# Ensure directories exist
SPEC_STORAGE_DIR.mkdir(exist_ok=True)
ITERATION_LOGS_DIR.mkdir(exist_ok=True)

async def store_spec(spec_id: str, spec_data: dict) -> bool:
    """Store specification data"""
    try:
        # Try database first
        from src.services.spec_storage import spec_storage
        spec_storage.store_spec(spec_id, spec_data)
        return True
    except Exception:
        # Fallback to file storage
        storage_file = SPEC_STORAGE_DIR / f"{spec_id}.json"
        with open(storage_file, 'w') as f:
            json.dump(spec_data, f, indent=2)
        return True

async def load_spec(spec_id: str) -> Optional[dict]:
    """Load specification data"""
    try:
        # Try database first
        from src.services.spec_storage import spec_storage
        return spec_storage.get_spec(spec_id)
    except Exception:
        # Fallback to file storage
        storage_file = SPEC_STORAGE_DIR / f"{spec_id}.json"
        if storage_file.exists():
            with open(storage_file, 'r') as f:
                return json.load(f)
        return None

async def save_spec(spec_id: str, spec_data: dict) -> bool:
    """Save updated specification"""
    return await store_spec(spec_id, spec_data)

async def save_iteration(spec_id: str, object_id: str, before: dict, after: dict, instruction: str) -> str:
    """Save iteration details"""
    iteration_id = str(uuid.uuid4())
    iteration_data = {
        'iteration_id': iteration_id,
        'spec_id': spec_id,
        'object_id': object_id,
        'instruction': instruction,
        'before': before,
        'after': after,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # Try database first
        from src.data.database import db
        db.save_iteration_log(spec_id, iteration_data)
    except Exception as e:
        print(f"[WARN] Failed to save iteration to DB: {e}")
        # Fallback to file
        log_file = ITERATION_LOGS_DIR / f"{iteration_id}.json"
        with open(log_file, 'w') as f:
            json.dump(iteration_data, f, indent=2)
    
    return iteration_id

async def generate_preview_url(spec_id: str) -> str:
    """Generate preview URL for spec"""
    try:
        from src.services.preview_manager import preview_manager
        return await preview_manager.generate_preview({'spec_id': spec_id})
    except Exception:
        return f"/preview/{spec_id}.jpg"

class ObjectTargeter:
    """Parse target objects and material changes from instructions"""
    
    def parse_target(self, instruction: str, spec_data: dict) -> Optional[str]:
        """Parse target object ID from instruction"""
        instruction_lower = instruction.lower()
        
        # Look for object types in instruction
        for obj in spec_data.get('objects', []):
            obj_type = obj.get('type', '').lower()
            if obj_type in instruction_lower:
                return obj['id']
        
        # Fallback: return first editable object
        for obj in spec_data.get('objects', []):
            if obj.get('editable', True):
                return obj['id']
        
        return None
    
    def parse_material(self, instruction: str) -> dict:
        """Parse material changes from instruction"""
        instruction_lower = instruction.lower()
        changes = {}
        
        # Common materials
        materials = ['wood', 'concrete', 'steel', 'glass', 'brick', 'marble', 'granite', 'tile']
        
        for material in materials:
            if material in instruction_lower:
                changes['material'] = material
                break
        
        # If no specific material found, extract from "to X" pattern
        if 'material' not in changes:
            import re
            match = re.search(r'to (\w+)', instruction_lower)
            if match:
                changes['material'] = match.group(1)
        
        return changes