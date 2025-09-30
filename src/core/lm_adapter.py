from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import logging

class LMAdapter(ABC):
    @abstractmethod
    def run(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run LM inference and return parsed JSON spec"""
        pass

class LocalLMAdapter(LMAdapter):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def run(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Local RTX-3060 LM inference implementation"""
        # Validate prompt
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
            
        try:
            # For now, return a structured response based on prompt analysis
            # This would be replaced with actual RTX-3060 inference
            design_type = self._detect_design_type(prompt)
            
            spec_data = {
                "design_type": design_type,
                "category": self._extract_category(prompt, design_type),
                "materials": self._extract_materials(prompt),
                "dimensions": self._extract_dimensions(prompt),
                "performance": self._extract_performance(prompt),
                "features": self._extract_features(prompt),
                "components": self._extract_components(prompt),
                "requirements": self._extract_requirements(prompt),
                "constraints": [],
                "use_cases": [prompt.split('.')[0]],
                "target_audience": "general",
                "estimated_cost": "TBD",
                "timeline": "TBD"
            }
            
            return spec_data
            
        except Exception as e:
            self.logger.error(f"LM inference failed: {e}")
            return self._fallback_response(prompt)
    
    def _detect_design_type(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in ['building', 'house', 'office', 'structure']):
            return 'building'
        elif any(word in prompt_lower for word in ['car', 'vehicle', 'truck', 'bike']):
            return 'vehicle'
        elif any(word in prompt_lower for word in ['phone', 'computer', 'device', 'electronic']):
            return 'electronics'
        elif any(word in prompt_lower for word in ['chair', 'table', 'furniture', 'desk']):
            return 'furniture'
        elif any(word in prompt_lower for word in ['appliance', 'refrigerator', 'washer']):
            return 'appliance'
        return 'general'
    
    def _extract_category(self, prompt: str, design_type: str) -> str:
        if design_type == 'building':
            return 'residential' if 'house' in prompt.lower() else 'commercial'
        elif design_type == 'vehicle':
            return 'electric' if 'electric' in prompt.lower() else 'standard'
        return 'standard'
    
    def _extract_materials(self, prompt: str) -> list:
        materials = []
        if 'steel' in prompt.lower():
            materials.append({"type": "steel", "grade": "standard", "properties": {}})
        if 'wood' in prompt.lower():
            materials.append({"type": "wood", "grade": "hardwood", "properties": {}})
        if not materials:
            materials.append({"type": "standard", "grade": None, "properties": {}})
        return materials
    
    def _extract_dimensions(self, prompt: str) -> dict:
        return {
            "length": None,
            "width": None, 
            "height": None,
            "units": "metric"
        }
    
    def _extract_performance(self, prompt: str) -> dict:
        return {
            "power": None,
            "efficiency": "high" if 'efficient' in prompt.lower() else None,
            "capacity": None,
            "speed": None,
            "other_specs": {}
        }
    
    def _extract_features(self, prompt: str) -> list:
        features = []
        if 'smart' in prompt.lower():
            features.append('smart technology')
        if 'sustainable' in prompt.lower():
            features.append('sustainable design')
        if 'modern' in prompt.lower():
            features.append('modern aesthetics')
        return features
    
    def _extract_components(self, prompt: str) -> list:
        return ['main structure', 'control system', 'interface']
    
    def _extract_requirements(self, prompt: str) -> list:
        requirements = []
        if 'durable' in prompt.lower():
            requirements.append('high durability')
        if 'efficient' in prompt.lower():
            requirements.append('energy efficiency')
        return requirements
    
    def _fallback_response(self, prompt: str) -> dict:
        return {
            "design_type": "general",
            "category": "standard",
            "materials": [{"type": "standard", "grade": None, "properties": {}}],
            "dimensions": {"units": "metric"},
            "performance": {"other_specs": {}},
            "features": ["basic functionality"],
            "components": ["main component"],
            "requirements": ["functional"],
            "constraints": [],
            "use_cases": [prompt[:50]],
            "target_audience": "general",
            "estimated_cost": "TBD",
            "timeline": "TBD"
        }