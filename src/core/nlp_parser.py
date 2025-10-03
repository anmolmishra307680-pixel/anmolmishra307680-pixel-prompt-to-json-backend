import re
from typing import Dict, Any, List, Optional
import difflib

class ObjectTargeter:
    """Enhanced NLP parser for object identification and material switching"""
    
    def __init__(self):
        # Comprehensive object patterns with synonyms
        self.object_patterns = {
            'floor': ['floor', 'flooring', 'ground', 'base', 'surface'],
            'wall': ['wall', 'walls', 'partition', 'barrier'],
            'ceiling': ['ceiling', 'roof', 'top'],
            'window': ['window', 'windows', 'glass'],
            'door': ['door', 'doors', 'entrance', 'exit'],
            'cushion': ['cushion', 'cushions', 'pillow', 'pillows'],
            'chair': ['chair', 'chairs', 'seat', 'seats'],
            'table': ['table', 'tables', 'desk', 'desks'],
            'sofa': ['sofa', 'sofas', 'couch', 'couches'],
            'cabinet': ['cabinet', 'cabinets', 'cupboard', 'storage'],
            'counter': ['counter', 'counters', 'countertop'],
            'shelf': ['shelf', 'shelves', 'shelving'],
            'frame': ['frame', 'frames', 'structure'],
            'panel': ['panel', 'panels', 'board'],
            'handle': ['handle', 'handles', 'knob', 'knobs'],
            'surface': ['surface', 'surfaces', 'top', 'face']
        }
        
        # Enhanced material patterns
        self.material_patterns = {
            'marble': ['marble', 'marble stone', 'natural stone'],
            'wood': ['wood', 'wooden', 'timber', 'oak', 'pine', 'mahogany'],
            'glass': ['glass', 'crystal', 'transparent'],
            'metal': ['metal', 'steel', 'aluminum', 'iron', 'brass'],
            'plastic': ['plastic', 'polymer', 'acrylic'],
            'fabric': ['fabric', 'cloth', 'textile', 'upholstery'],
            'leather': ['leather', 'hide', 'suede'],
            'concrete': ['concrete', 'cement'],
            'ceramic': ['ceramic', 'tile', 'porcelain'],
            'granite': ['granite', 'stone'],
            'bamboo': ['bamboo'],
            'vinyl': ['vinyl', 'pvc'],
            'carpet': ['carpet', 'rug', 'carpeting']
        }
        
        # Comprehensive color patterns
        self.color_patterns = {
            'red': ['red', 'crimson', 'scarlet', 'burgundy'],
            'blue': ['blue', 'navy', 'azure', 'cobalt'],
            'green': ['green', 'emerald', 'forest', 'lime'],
            'yellow': ['yellow', 'gold', 'amber', 'lemon'],
            'orange': ['orange', 'tangerine', 'peach'],
            'purple': ['purple', 'violet', 'lavender', 'plum'],
            'pink': ['pink', 'rose', 'magenta'],
            'brown': ['brown', 'tan', 'beige', 'chocolate'],
            'black': ['black', 'charcoal', 'ebony'],
            'white': ['white', 'ivory', 'cream', 'pearl'],
            'gray': ['gray', 'grey', 'silver', 'slate'],
            'turquoise': ['turquoise', 'teal', 'cyan']
        }
        
        # Action patterns for parsing instructions
        self.action_patterns = {
            'change': ['change', 'switch', 'replace', 'update'],
            'make': ['make', 'set', 'turn', 'convert'],
            'paint': ['paint', 'color', 'dye'],
            'cover': ['cover', 'wrap', 'overlay']
        }
    
    def parse_target(self, instruction: str, spec_data: Dict[str, Any]) -> Optional[str]:
        """Enhanced object targeting with fuzzy matching"""
        instruction_lower = instruction.lower()
        objects = spec_data.get('objects', [])
        
        if not objects:
            return None
        
        # Direct pattern matching
        for obj_type, patterns in self.object_patterns.items():
            for pattern in patterns:
                if pattern in instruction_lower:
                    # Find matching object in spec
                    for obj in objects:
                        obj_type_lower = obj.get('type', '').lower()
                        if obj_type in obj_type_lower or any(p in obj_type_lower for p in patterns):
                            return obj['id']
        
        # Fuzzy matching for partial matches
        instruction_words = instruction_lower.split()
        best_match = None
        best_score = 0
        
        for obj in objects:
            obj_type = obj.get('type', '').lower()
            for word in instruction_words:
                # Calculate similarity score
                similarity = difflib.SequenceMatcher(None, word, obj_type).ratio()
                if similarity > 0.6 and similarity > best_score:
                    best_score = similarity
                    best_match = obj['id']
        
        return best_match
    
    def parse_material(self, instruction: str) -> Dict[str, Any]:
        """Enhanced material and property parsing"""
        instruction_lower = instruction.lower()
        changes = {}
        
        # Parse material changes
        for material, patterns in self.material_patterns.items():
            if any(pattern in instruction_lower for pattern in patterns):
                changes['material'] = material
                break
        
        # Parse color changes
        properties = {}
        for color, patterns in self.color_patterns.items():
            if any(pattern in instruction_lower for pattern in patterns):
                properties['color'] = color
                break
        
        # Parse other properties
        if 'glossy' in instruction_lower or 'shiny' in instruction_lower:
            properties['finish'] = 'glossy'
        elif 'matte' in instruction_lower or 'flat' in instruction_lower:
            properties['finish'] = 'matte'
        
        if 'thick' in instruction_lower:
            properties['thickness'] = 'thick'
        elif 'thin' in instruction_lower:
            properties['thickness'] = 'thin'
        
        if 'soft' in instruction_lower:
            properties['texture'] = 'soft'
        elif 'hard' in instruction_lower:
            properties['texture'] = 'hard'
        
        if properties:
            changes['properties'] = properties
        
        return changes
    
    def generate_diff(self, before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed diff between before and after states"""
        diff = {
            'changed_fields': [],
            'before': before,
            'after': after
        }
        
        # Compare material
        if before.get('material') != after.get('material'):
            diff['changed_fields'].append('material')
        
        # Compare properties
        before_props = before.get('properties', {})
        after_props = after.get('properties', {})
        
        for key in set(list(before_props.keys()) + list(after_props.keys())):
            if before_props.get(key) != after_props.get(key):
                diff['changed_fields'].append(f'properties.{key}')
        
        return diff


class IterationTracker:
    """Track and save material switching iterations with diffs"""
    
    def __init__(self):
        self.iterations = []
    
    def save_iteration(self, spec_id: str, instruction: str, object_id: str, 
                      before: Dict[str, Any], after: Dict[str, Any]) -> str:
        """Save iteration with detailed diff tracking"""
        import uuid
        from datetime import datetime
        
        iteration_id = str(uuid.uuid4())
        
        # Generate diff
        targeter = ObjectTargeter()
        diff = targeter.generate_diff(before, after)
        
        iteration = {
            'iteration_id': iteration_id,
            'spec_id': spec_id,
            'instruction': instruction,
            'object_id': object_id,
            'timestamp': datetime.now().isoformat(),
            'diff': diff,
            'before': before,
            'after': after
        }
        
        self.iterations.append(iteration)
        
        # Save to file
        self._save_to_file(iteration)
        
        return iteration_id
    
    def _save_to_file(self, iteration: Dict[str, Any]):
        """Save iteration to JSON file"""
        import json
        from pathlib import Path
        
        iterations_dir = Path("iterations")
        iterations_dir.mkdir(exist_ok=True)
        
        file_path = iterations_dir / f"iteration_{iteration['iteration_id']}.json"
        
        with open(file_path, 'w') as f:
            json.dump(iteration, f, indent=2, default=str)
    
    def get_iterations(self, spec_id: str) -> List[Dict[str, Any]]:
        """Get all iterations for a spec"""
        return [it for it in self.iterations if it['spec_id'] == spec_id]