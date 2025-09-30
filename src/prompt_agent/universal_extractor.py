"""Universal PromptExtractor for all design types"""

from src.schemas.universal_schema import UniversalDesignSpec, MaterialSpec, DimensionSpec

class UniversalPromptExtractor:
    def __init__(self):
        pass
    
    def extract_spec(self, prompt: str) -> UniversalDesignSpec:
        """Extract universal design specification from prompt"""
        prompt_lower = prompt.lower()
        
        # Detect design type
        design_type = self._detect_design_type(prompt_lower)
        
        # Extract category based on design type
        category = self._extract_category(prompt_lower, design_type)
        
        # Extract materials
        materials = self._extract_materials(prompt_lower, design_type)
        
        # Extract dimensions
        dimensions = self._extract_dimensions(prompt_lower, design_type)
        
        # Extract features
        features = self._extract_features(prompt_lower, design_type)
        
        # Extract components
        components = self._extract_components(prompt_lower, design_type)
        
        return UniversalDesignSpec(
            design_type=design_type,
            category=category,
            materials=materials,
            dimensions=dimensions,
            features=features,
            requirements=[prompt],
            components=components
        )
    
    def _detect_design_type(self, prompt_lower: str) -> str:
        """Detect the type of design from prompt"""
        if any(word in prompt_lower for word in ['building', 'house', 'office', 'warehouse', 'apartment', 'residential']):
            return "building"
        elif any(word in prompt_lower for word in ['car', 'vehicle', 'truck', 'motorcycle']):
            return "vehicle"
        elif any(word in prompt_lower for word in ['phone', 'computer', 'device', 'electronics']):
            return "electronics"
        elif any(word in prompt_lower for word in ['chair', 'table', 'furniture', 'desk']):
            return "furniture"
        elif any(word in prompt_lower for word in ['appliance', 'refrigerator', 'washer', 'dryer']):
            return "appliance"
        else:
            return "general"
    
    def _extract_category(self, prompt_lower: str, design_type: str) -> str:
        """Extract category based on design type"""
        if design_type == "building":
            if "office" in prompt_lower:
                return "office"
            elif "residential" in prompt_lower or "house" in prompt_lower or "apartment" in prompt_lower:
                return "residential"
            elif "warehouse" in prompt_lower:
                return "warehouse"
            else:
                return "general"
        elif design_type == "vehicle":
            if "car" in prompt_lower:
                return "car"
            elif "truck" in prompt_lower:
                return "truck"
            else:
                return "general"
        else:
            return "standard"
    
    def _extract_materials(self, prompt_lower: str, design_type: str) -> list:
        """Extract materials based on design type"""
        materials = []
        
        if design_type == "building":
            if "steel" in prompt_lower:
                materials.append(MaterialSpec(type="steel", grade="A36"))
            if "concrete" in prompt_lower:
                materials.append(MaterialSpec(type="concrete", grade="C30"))
            if "wood" in prompt_lower:
                materials.append(MaterialSpec(type="wood", grade="hardwood"))
        elif design_type == "vehicle":
            if "aluminum" in prompt_lower:
                materials.append(MaterialSpec(type="aluminum", grade="6061"))
            if "steel" in prompt_lower:
                materials.append(MaterialSpec(type="steel", grade="automotive"))
        elif design_type == "electronics":
            materials.append(MaterialSpec(type="silicon", grade="semiconductor"))
            materials.append(MaterialSpec(type="plastic", grade="ABS"))
        
        if not materials:
            materials.append(MaterialSpec(type="standard", grade="basic"))
        
        return materials
    
    def _extract_dimensions(self, prompt_lower: str, design_type: str) -> DimensionSpec:
        """Extract dimensions based on design type"""
        if design_type == "building":
            return DimensionSpec(
                length=20.0,
                width=15.0,
                height=10.0,
                area=300.0,
                units="metric"
            )
        elif design_type == "vehicle":
            return DimensionSpec(
                length=4.5,
                width=1.8,
                height=1.5,
                area=8.1,
                units="metric"
            )
        else:
            return DimensionSpec(units="metric")
    
    def _extract_features(self, prompt_lower: str, design_type: str) -> list:
        """Extract features based on design type"""
        features = []
        
        if design_type == "building":
            if "parking" in prompt_lower:
                features.append("parking")
            if "elevator" in prompt_lower:
                features.append("elevator")
            if "solar" in prompt_lower:
                features.append("solar_panels")
        elif design_type == "vehicle":
            if "electric" in prompt_lower:
                features.append("electric_motor")
            if "gps" in prompt_lower:
                features.append("gps")
            if "bluetooth" in prompt_lower:
                features.append("bluetooth")
        elif design_type == "electronics":
            if "touchscreen" in prompt_lower:
                features.append("touchscreen")
            if "wireless" in prompt_lower:
                features.append("wireless")
        
        if not features:
            features.append("basic_functionality")
        
        return features
    
    def _extract_components(self, prompt_lower: str, design_type: str) -> list:
        """Extract components based on design type"""
        if design_type == "building":
            return ["foundation", "structure", "roof"]
        elif design_type == "vehicle":
            return ["chassis", "engine", "wheels"]
        elif design_type == "electronics":
            return ["processor", "memory", "display"]
        else:
            return ["main_component"]