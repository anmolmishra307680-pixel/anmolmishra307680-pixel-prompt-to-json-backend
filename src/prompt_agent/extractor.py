"""Enhanced MainAgent with LM adapter integration"""

from src.schemas.legacy_schema import DesignSpec, MaterialSpec, DimensionSpec
from src.core.lm_adapter import LocalLMAdapter

class MainAgent:
    def __init__(self):
        try:
            self.lm = LocalLMAdapter()
        except Exception:
            self.lm = None
    
    def run(self, prompt: str, params: dict = None) -> DesignSpec:
        """Enhanced generation with LM adapter"""
        if self.lm:
            try:
                return self.lm.run(prompt, params or {})
            except Exception:
                pass
        
        # Fallback to rule-based extraction
        return self._extract_spec_fallback(prompt)
    
    def _extract_spec_fallback(self, prompt: str) -> DesignSpec:
        """Fallback rule-based extraction"""
        prompt_lower = prompt.lower()
        
        building_type = "general"
        if "office" in prompt_lower:
            building_type = "office"
        elif "residential" in prompt_lower or "house" in prompt_lower:
            building_type = "residential"
        elif "warehouse" in prompt_lower:
            building_type = "warehouse"
        elif "hospital" in prompt_lower:
            building_type = "hospital"
        
        stories = 1
        if "story" in prompt_lower or "floor" in prompt_lower:
            words = prompt.split()
            for i, word in enumerate(words):
                if word.lower() in ["story", "stories", "floor", "floors"]:
                    if i > 0 and words[i-1].isdigit():
                        stories = int(words[i-1])
                        break
        
        materials = []
        if "steel" in prompt_lower:
            materials.append(MaterialSpec(type="steel", grade="A36"))
        if "concrete" in prompt_lower:
            materials.append(MaterialSpec(type="concrete", grade="C30"))
        if not materials:
            materials.append(MaterialSpec(type="concrete", grade="standard"))
        
        dimensions = DimensionSpec(
            length=20.0,
            width=15.0,
            height=3.5 * stories,
            area=300.0
        )
        
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

# Backward compatibility
PromptExtractor = MainAgent