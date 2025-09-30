"""Mobile API wrapper optimized for React Native/Expo"""

from typing import Dict, Any, Optional
from pydantic import BaseModel

class MobileGenerateRequest(BaseModel):
    prompt: str
    device_info: Optional[Dict[str, str]] = None
    location: Optional[Dict[str, float]] = None
    
class MobileSwitchRequest(BaseModel):
    spec_id: str
    instruction: str
    device_info: Optional[Dict[str, str]] = None

class MobileResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    mobile_optimized: bool = True
    cache_ttl: int = 300  # 5 minutes

class MobileAPIWrapper:
    def __init__(self):
        self.mobile_cache = {}
    
    def optimize_for_mobile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize response for mobile consumption"""
        # Reduce payload size for mobile
        if 'spec_json' in data:
            spec = data['spec_json']
            # Keep only essential fields for mobile
            mobile_spec = {
                'spec_id': spec.get('spec_id'),
                'objects': [
                    {
                        'id': obj.get('id'),
                        'type': obj.get('type'),
                        'material': obj.get('material'),
                        'editable': obj.get('editable', True)
                    }
                    for obj in spec.get('objects', [])[:10]  # Limit to 10 objects
                ],
                'scene': {
                    'name': spec.get('scene', {}).get('name', 'Mobile Scene'),
                    'total_objects': len(spec.get('objects', []))
                }
            }
            data['spec_json'] = mobile_spec
        
        # Add mobile-specific metadata
        data['mobile_metadata'] = {
            'optimized': True,
            'reduced_payload': True,
            'cache_recommended': True
        }
        
        return data

# Global instance
mobile_api = MobileAPIWrapper()