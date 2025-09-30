"""Legacy PromptExtractor for backward compatibility"""

from src.schemas.legacy_schema import DesignSpec, MaterialSpec, DimensionSpec

class PromptExtractor:
    def __init__(self):
        pass
    
    def extract_spec(self, prompt: str) -> DesignSpec:
        """Extract building specification from prompt"""
        prompt_lower = prompt.lower()
        
        # Extract building type
        building_type = "general"
        if "office" in prompt_lower:
            building_type = "office"
        elif "residential" in prompt_lower or "house" in prompt_lower:
            building_type = "residential"
        elif "warehouse" in prompt_lower:
            building_type = "warehouse"
        elif "hospital" in prompt_lower:
            building_type = "hospital"
        
        # Extract stories
        stories = 1
        if "story" in prompt_lower or "floor" in prompt_lower:
            words = prompt.split()
            for i, word in enumerate(words):
                if word.lower() in ["story", "stories", "floor", "floors"]:
                    if i > 0 and words[i-1].isdigit():
                        stories = int(words[i-1])
                        break
        
        # Extract materials
        materials = []
        if "steel" in prompt_lower:
            materials.append(MaterialSpec(type="steel", grade="A36"))
        if "concrete" in prompt_lower:
            materials.append(MaterialSpec(type="concrete", grade="C30"))
        if not materials:
            materials.append(MaterialSpec(type="concrete", grade="standard"))
        
        # Extract dimensions
        dimensions = DimensionSpec(
            length=20.0,
            width=15.0,
            height=3.5 * stories,
            area=300.0
        )
        
        # Extract features
        features = []
        if "parking" in prompt_lower:
            features.append("parking")
        if "elevator" in prompt_lower:
            features.append("elevator")
        if "balcony" in prompt_lower:
            features.append("balcony")
        
        return DesignSpec(
            building_type=building_type,
            stories=stories,
            materials=materials,
            dimensions=dimensions,
            features=features,
            requirements=[prompt]
        )