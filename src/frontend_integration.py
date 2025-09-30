"""Frontend integration utilities for UI testing flows"""

from typing import Dict, Any, List
from datetime import datetime
import json

class FrontendIntegration:
    def __init__(self):
        self.test_flows = []
        self.ui_sessions = {}
    
    def create_ui_session(self, session_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create UI testing session"""
        session = {
            'session_id': session_id,
            'user_data': user_data,
            'created_at': datetime.now().isoformat(),
            'flows_completed': [],
            'current_spec': None,
            'three_js_ready': False
        }
        
        self.ui_sessions[session_id] = session
        return session
    
    def log_ui_flow(self, session_id: str, flow_type: str, data: Dict[str, Any]):
        """Log UI testing flow"""
        flow_entry = {
            'session_id': session_id,
            'flow_type': flow_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_flows.append(flow_entry)
        
        if session_id in self.ui_sessions:
            self.ui_sessions[session_id]['flows_completed'].append(flow_type)
    
    def get_ui_test_summary(self) -> Dict[str, Any]:
        """Get UI testing summary"""
        flow_types = {}
        for flow in self.test_flows:
            flow_type = flow['flow_type']
            flow_types[flow_type] = flow_types.get(flow_type, 0) + 1
        
        return {
            'total_flows': len(self.test_flows),
            'active_sessions': len(self.ui_sessions),
            'flow_types': flow_types,
            'last_activity': self.test_flows[-1]['timestamp'] if self.test_flows else None
        }
    
    def prepare_three_js_data(self, spec_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for Three.js loader"""
        objects = spec_data.get('objects', [])
        
        three_js_data = {
            'scene': {
                'objects': [],
                'camera': {
                    'position': [0, 10, 20],
                    'target': [0, 0, 0]
                },
                'lighting': {
                    'ambient': 0.4,
                    'directional': {
                        'intensity': 0.8,
                        'position': [10, 10, 5]
                    }
                }
            },
            'metadata': {
                'spec_id': spec_data.get('spec_id'),
                'object_count': len(objects),
                'editable_objects': [obj['id'] for obj in objects if obj.get('editable', True)]
            }
        }
        
        # Convert objects to Three.js format
        for obj in objects:
            three_obj = {
                'id': obj['id'],
                'type': obj['type'],
                'geometry': self._get_geometry_for_type(obj['type']),
                'material': {
                    'type': 'MeshLambertMaterial',
                    'color': self._get_color_for_material(obj.get('material', 'standard')),
                    'properties': obj.get('properties', {})
                },
                'position': [
                    obj.get('position', {}).get('x', 0),
                    obj.get('position', {}).get('y', 0),
                    obj.get('position', {}).get('z', 0)
                ],
                'scale': [
                    obj.get('dimensions', {}).get('width', 1),
                    obj.get('dimensions', {}).get('height', 1),
                    obj.get('dimensions', {}).get('depth', 1)
                ],
                'editable': obj.get('editable', True)
            }
            three_js_data['scene']['objects'].append(three_obj)
        
        return three_js_data
    
    def _get_geometry_for_type(self, obj_type: str) -> Dict[str, Any]:
        """Get Three.js geometry for object type"""
        geometry_map = {
            'floor': {'type': 'PlaneGeometry', 'args': [10, 10]},
            'wall': {'type': 'BoxGeometry', 'args': [0.2, 3, 10]},
            'door': {'type': 'BoxGeometry', 'args': [1, 2, 0.1]},
            'window': {'type': 'BoxGeometry', 'args': [2, 1, 0.1]},
            'cushion': {'type': 'BoxGeometry', 'args': [1, 0.2, 1]},
            'table': {'type': 'BoxGeometry', 'args': [2, 0.1, 1]},
            'chair': {'type': 'BoxGeometry', 'args': [0.5, 1, 0.5]}
        }
        
        return geometry_map.get(obj_type, {'type': 'BoxGeometry', 'args': [1, 1, 1]})
    
    def _get_color_for_material(self, material: str) -> str:
        """Get color hex for material"""
        color_map = {
            'wood': '#8B4513',
            'marble': '#F8F8FF',
            'steel': '#C0C0C0',
            'concrete': '#808080',
            'glass': '#87CEEB',
            'fabric': '#DDA0DD',
            'plastic': '#FFB6C1'
        }
        
        return color_map.get(material, '#CCCCCC')

# Global instance
frontend_integration = FrontendIntegration()