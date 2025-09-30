from typing import Dict, Any, Optional, List

class ObjectTargeter:
    def __init__(self):
        self.object_keywords = {
            'floor': ['floor', 'flooring', 'ground'],
            'wall': ['wall', 'walls'],
            'door': ['door', 'doors'],
            'window': ['window', 'windows'],
            'cushion': ['cushion', 'cushions', 'pillow', 'pillows'],
            'table': ['table', 'desk'],
            'chair': ['chair', 'seat'],
            'roof': ['roof', 'ceiling'],
            'main_structure': ['structure', 'frame', 'body']
        }
        
        self.material_keywords = {
            'marble': 'marble',
            'wood': 'wood',
            'steel': 'steel',
            'concrete': 'concrete',
            'glass': 'glass',
            'plastic': 'plastic',
            'fabric': 'fabric',
            'leather': 'leather',
            'metal': 'metal',
            'stone': 'stone'
        }
        
        self.color_keywords = {
            'orange': 'orange',
            'red': 'red',
            'blue': 'blue',
            'green': 'green',
            'yellow': 'yellow',
            'black': 'black',
            'white': 'white',
            'brown': 'brown',
            'gray': 'gray',
            'grey': 'gray'
        }

    def parse_target(self, text: str, spec: Dict[str, Any]) -> Optional[str]:
        """Return correct object_id given 'change floor to marble'"""
        text_lower = text.lower()
        
        # Get objects from spec
        objects = spec.get('objects', [])
        if not objects:
            return None
        
        # Find matching object by type
        for obj in objects:
            obj_type = obj.get('type', '').lower()
            
            # Check direct match
            if obj_type in text_lower:
                return obj.get('id')
            
            # Check keyword matches
            for target_type, keywords in self.object_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    if target_type in obj_type or obj_type in target_type:
                        return obj.get('id')
        
        # Fallback: return first editable object
        for obj in objects:
            if obj.get('editable', True):
                return obj.get('id')
        
        return objects[0].get('id') if objects else None

    def parse_material(self, text: str) -> Dict[str, Any]:
        """Return new material from text"""
        text_lower = text.lower()
        result = {}
        
        # Extract material
        for material, value in self.material_keywords.items():
            if material in text_lower:
                result['material'] = value
                break
        
        # Extract color
        for color, value in self.color_keywords.items():
            if color in text_lower:
                if 'properties' not in result:
                    result['properties'] = {}
                result['properties']['color'] = value
                break
        
        # If no material found but color found, use fabric as default
        if 'properties' in result and 'material' not in result:
            result['material'] = 'fabric'
        
        return result