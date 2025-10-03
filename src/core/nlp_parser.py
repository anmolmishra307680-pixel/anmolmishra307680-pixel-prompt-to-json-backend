import re
from typing import Dict, Any

class ObjectTargeter:
    def __init__(self):
        self.object_patterns = {
            'floor': ['floor','flooring'],
            'wall': ['wall'],
            'window': ['window'],
            'furniture': ['sofa','chair','cushion']
        }
        self.material_patterns = {
            'marble': ['marble'], 'wood': ['wood'], 'glass': ['glass']
        }
        self.color_patterns = {
            'orange': ['orange'], 'red': ['red'], 'blue': ['blue']
        }

    def parse_target(self, instruction: str, spec_data: Dict[str,Any]) -> str:
        ins = instruction.lower()
        for typ, pats in self.object_patterns.items():
            if any(p in ins for p in pats):
                for obj in spec_data.get('objects',[]):
                    if typ in obj.get('type','').lower():
                        return obj['id']
        return None

    def parse_material(self, instruction: str) -> Dict[str,Any]:
        ins = instruction.lower()
        changes = {}
        for mat, pats in self.material_patterns.items():
            if any(p in ins for p in pats):
                changes['material']=mat; break
        props={}
        for col, pats in self.color_patterns.items():
            if any(p in ins for p in pats):
                props['color']=col; break
        if props: changes['properties']=props
        return changes