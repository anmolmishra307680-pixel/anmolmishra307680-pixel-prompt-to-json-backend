"""Universal Design Prompt Extraction Utilities"""

import re
from typing import List, Dict, Tuple
from src.universal_schema import UniversalDesignSpec, MaterialSpec, DimensionSpec, PerformanceSpec

class UniversalPromptExtractor:
    def __init__(self):
        self.design_categories = {
            'building': {
                'keywords': ['building', 'house', 'office', 'warehouse', 'hospital', 'school', 'apartment', 'residential', 'commercial', 'structure', 'construction', 'story', 'floor'],
                'materials': ['concrete', 'steel', 'brick', 'cement', 'wood', 'glass', 'stone', 'aluminum'],
                'features': ['parking', 'elevator', 'balcony', 'garden', 'pool', 'gym', 'security', 'ac', 'solar'],
                'components': ['foundation', 'walls', 'roof', 'floors', 'windows', 'doors']
            },
            'vehicle': {
                'keywords': ['car', 'truck', 'bus', 'motorcycle', 'bike', 'vehicle', 'automobile', 'suv', 'sedan', 'hatchback'],
                'materials': ['steel', 'aluminum', 'carbon fiber', 'plastic', 'leather', 'fabric', 'rubber'],
                'features': ['gps', 'bluetooth', 'sunroof', 'heated seats', 'cruise control', 'parking sensors', 'backup camera'],
                'components': ['engine', 'transmission', 'wheels', 'brakes', 'suspension', 'interior', 'exterior']
            },
            'electronics': {
                'keywords': ['laptop', 'phone', 'tablet', 'computer', 'smartphone', 'device', 'gadget', 'electronic'],
                'materials': ['aluminum', 'plastic', 'glass', 'silicon', 'copper', 'lithium', 'carbon fiber'],
                'features': ['touchscreen', 'wireless', 'bluetooth', 'camera', 'fingerprint', 'face recognition', 'waterproof'],
                'components': ['processor', 'memory', 'storage', 'display', 'battery', 'camera', 'speakers']
            },
            'appliance': {
                'keywords': ['fridge', 'refrigerator', 'washing machine', 'dishwasher', 'oven', 'microwave', 'appliance'],
                'materials': ['stainless steel', 'plastic', 'glass', 'aluminum', 'ceramic'],
                'features': ['energy efficient', 'smart control', 'timer', 'auto defrost', 'temperature control', 'wifi enabled'],
                'components': ['compressor', 'motor', 'control panel', 'door', 'shelves', 'filters']
            },
            'furniture': {
                'keywords': ['chair', 'table', 'desk', 'bed', 'sofa', 'cabinet', 'furniture', 'shelf'],
                'materials': ['wood', 'metal', 'plastic', 'fabric', 'leather', 'glass', 'bamboo'],
                'features': ['adjustable', 'foldable', 'storage', 'ergonomic', 'cushioned', 'modular'],
                'components': ['frame', 'legs', 'surface', 'cushions', 'drawers', 'handles']
            }
        }

    def extract_spec(self, prompt: str) -> UniversalDesignSpec:
        """Extract universal design specification from prompt"""
        if not self.is_design_related(prompt):
            raise ValueError("Prompt does not appear to be design-related. Please provide a prompt about designing or creating something.")

        design_type, category = self.extract_design_type(prompt)
        materials = self.extract_materials(prompt, design_type)
        dimensions = self.extract_dimensions(prompt)
        performance = self.extract_performance(prompt, design_type)
        features = self.extract_features(prompt, design_type)
        components = self.extract_components(prompt, design_type)
        requirements = self.extract_requirements(prompt)
        constraints = self.extract_constraints(prompt)
        use_cases = self.extract_use_cases(prompt)
        target_audience = self.extract_target_audience(prompt)
        estimated_cost = self.extract_cost(prompt)
        timeline = self.extract_timeline(prompt)

        return UniversalDesignSpec(
            design_type=design_type,
            category=category,
            materials=materials,
            dimensions=dimensions,
            performance=performance,
            features=features,
            components=components,
            requirements=requirements,
            constraints=constraints,
            use_cases=use_cases,
            target_audience=target_audience,
            estimated_cost=estimated_cost,
            timeline=timeline
        )

    def is_design_related(self, prompt: str) -> bool:
        """Check if prompt is related to design/creation"""
        prompt_lower = prompt.lower()

        design_keywords = [
            'design', 'create', 'build', 'make', 'develop', 'construct', 'manufacture',
            'prototype', 'blueprint', 'plan', 'specification', 'model'
        ]

        # Check for design action words
        has_design_action = any(keyword in prompt_lower for keyword in design_keywords)

        # Check for design object categories
        has_design_object = any(
            any(keyword in prompt_lower for keyword in category['keywords'])
            for category in self.design_categories.values()
        )

        # Exclude non-design content (but not 'story' as it can mean building stories)
        non_design_keywords = [
            'tale', 'weather', 'news', 'joke', 'recipe', 'cooking',
            'movie', 'song', 'book', 'poem', 'essay', 'article', 'princess', 'character'
        ]

        has_non_design = any(keyword in prompt_lower for keyword in non_design_keywords)

        # Accept if has design objects even without action words
        return (has_design_action or has_design_object) and not has_non_design

    def extract_design_type(self, prompt: str) -> Tuple[str, str]:
        """Extract design type and specific category"""
        prompt_lower = prompt.lower()

        for design_type, data in self.design_categories.items():
            for keyword in data['keywords']:
                if keyword in prompt_lower:
                    # Extract more specific category
                    category = self._extract_specific_category(prompt_lower, design_type, keyword)
                    return design_type, category

        return "general", "custom"

    def _extract_specific_category(self, prompt: str, design_type: str, matched_keyword: str) -> str:
        """Extract specific category within design type"""
        if design_type == 'building':
            building_types = {
                'residential': ['house', 'home', 'apartment', 'residential'],
                'commercial': ['office', 'commercial', 'business'],
                'industrial': ['warehouse', 'factory', 'industrial'],
                'institutional': ['hospital', 'school', 'university']
            }
            for category, keywords in building_types.items():
                if any(keyword in prompt for keyword in keywords):
                    return category
            return 'general'

        elif design_type == 'vehicle':
            if any(word in prompt for word in ['car', 'sedan', 'hatchback', 'suv']):
                return 'automobile'
            elif any(word in prompt for word in ['truck', 'commercial']):
                return 'commercial_vehicle'
            elif any(word in prompt for word in ['bike', 'motorcycle']):
                return 'two_wheeler'
            return 'general'

        elif design_type == 'electronics':
            if any(word in prompt for word in ['laptop', 'computer']):
                return 'computing'
            elif any(word in prompt for word in ['phone', 'smartphone']):
                return 'mobile'
            elif any(word in prompt for word in ['tablet']):
                return 'tablet'
            return 'general'

        return matched_keyword

    def extract_materials(self, prompt: str, design_type: str) -> List[MaterialSpec]:
        """Extract materials based on design type"""
        materials = []
        prompt_lower = prompt.lower()

        # Get relevant materials for design type
        relevant_materials = self.design_categories.get(design_type, {}).get('materials', [])

        # Add common materials
        all_materials = relevant_materials + ['plastic', 'metal', 'rubber', 'fabric', 'ceramic']

        for material in set(all_materials):  # Remove duplicates
            if material in prompt_lower:
                grade = self._extract_material_grade(prompt_lower, material)
                materials.append(MaterialSpec(type=material, grade=grade))

        # Default material if none found
        if not materials:
            default_material = relevant_materials[0] if relevant_materials else "standard"
            materials.append(MaterialSpec(type=default_material, grade="standard"))

        return materials

    def _extract_material_grade(self, prompt: str, material: str) -> str:
        """Extract material grade/specification"""
        grade_patterns = {
            'steel': r'(stainless|carbon|alloy|grade\s*\d+)',
            'aluminum': r'(6061|7075|anodized|grade\s*\d+)',
            'plastic': r'(abs|pvc|pet|hdpe|grade\s*\d+)',
            'wood': r'(oak|pine|maple|mahogany|grade\s*\d+)'
        }

        if material in grade_patterns:
            match = re.search(grade_patterns[material], prompt)
            if match:
                return match.group(1).upper()

        return "standard"

    def extract_dimensions(self, prompt: str) -> DimensionSpec:
        """Extract dimensions with flexible units"""
        units = "metric"

        # Detect unit system
        if any(unit in prompt.lower() for unit in ['feet', 'ft', 'inch', 'in', 'yard', 'lb', 'lbs']):
            units = "imperial"

        # Enhanced dimension patterns for vehicle parts
        dimension_patterns = {
            'length': [r'length[:\s]*([0-9.]+)', r'([0-9.]+)[:\s]*(?:cm|m|meter|metres?|ft|feet)\s*long'],
            'width': [r'width[:\s]*([0-9.]+)', r'([0-9.]+)[:\s]*(?:cm|m|meter|metres?|ft|feet)\s*wide'],
            'height': [r'height[:\s]*([0-9.]+)', r'([0-9.]+)[:\s]*(?:cm|m|meter|metres?|ft|feet)\s*(?:high|tall)'],
            'depth': [r'depth[:\s]*([0-9.]+)', r'([0-9.]+)[:\s]*(?:cm|m|meter|metres?|ft|feet)\s*deep'],
            'diameter': [r'diameter[:\s]*([0-9.]+)', r'([0-9.]+)[:\s]*(?:cm|m|meter|metres?|ft|feet)\s*diameter'],
            'weight': [r'weight[:\s]*([0-9.]+)', r'([0-9.]+)[:\s]*(?:kg|kilogram|lb|lbs|pound)']
        }

        # Vehicle-specific dimension patterns
        vehicle_patterns = {
            'door': [r'door[s]?[:\s]*(?:of\s*)?([0-9.]+)', r'([0-9.]+)[:\s]*(?:m|meter|metres?|ft|feet)\s*door'],
            'windshield': [r'wind?shield[:\s]*(?:of\s*)?([0-9.]+)', r'([0-9.]+)[:\s]*(?:m|meter|metres?|ft|feet)\s*wind?shield'],
            'wheel': [r'wheel[s]?[:\s]*(?:of\s*)?([0-9.]+)', r'([0-9.]+)[:\s]*(?:inch|in)\s*wheel'],
            'trunk': [r'trunk[:\s]*(?:of\s*)?([0-9.]+)', r'([0-9.]+)[:\s]*(?:m|meter|metres?|ft|feet)\s*trunk']
        }

        extracted_dims = {}

        # Extract standard dimensions
        for dim_type, patterns in dimension_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, prompt.lower())
                if match:
                    extracted_dims[dim_type] = float(match.group(1))
                    break

        # Extract vehicle-specific dimensions and map to standard dimensions
        for part, patterns in vehicle_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, prompt.lower())
                if match:
                    value = float(match.group(1))
                    if part == 'door':
                        extracted_dims['height'] = value  # Door height
                    elif part == 'windshield':
                        extracted_dims['width'] = value   # Windshield width
                    elif part == 'wheel':
                        extracted_dims['diameter'] = value # Wheel diameter
                    elif part == 'trunk':
                        extracted_dims['depth'] = value   # Trunk depth
                    break

        # Handle dimension pairs like "15x10" or "15 by 10"
        pair_patterns = [
            r'([0-9.]+)\s*[x×]\s*([0-9.]+)',
            r'([0-9.]+)\s*by\s*([0-9.]+)'
        ]

        for pattern in pair_patterns:
            match = re.search(pattern, prompt.lower())
            if match and 'length' not in extracted_dims and 'width' not in extracted_dims:
                extracted_dims['length'] = float(match.group(1))
                extracted_dims['width'] = float(match.group(2))
                break

        # Calculate area if length and width available
        if 'length' in extracted_dims and 'width' in extracted_dims:
            extracted_dims['area'] = extracted_dims['length'] * extracted_dims['width']

        return DimensionSpec(
            length=extracted_dims.get('length'),
            width=extracted_dims.get('width'),
            height=extracted_dims.get('height'),
            depth=extracted_dims.get('depth'),
            diameter=extracted_dims.get('diameter'),
            area=extracted_dims.get('area'),
            volume=extracted_dims.get('volume'),
            weight=extracted_dims.get('weight'),
            units=units
        )

    def extract_performance(self, prompt: str, design_type: str) -> PerformanceSpec:
        """Extract performance specifications"""
        prompt_lower = prompt.lower()

        performance_patterns = {
            'power': [r'([0-9.]+)\s*(?:hp|horsepower|kw|kilowatt|watts?)', r'power[:\s]*([0-9.]+)'],
            'efficiency': [r'([0-9.]+)\s*(?:mpg|km/l|efficiency)', r'efficiency[:\s]*([0-9.]+)'],
            'capacity': [r'([0-9.]+)\s*(?:gb|tb|liters?|gallons?)', r'capacity[:\s]*([0-9.]+)'],
            'speed': [r'([0-9.]+)\s*(?:mph|kmh|km/h)', r'speed[:\s]*([0-9.]+)']
        }

        specs = {}
        for spec_type, patterns in performance_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, prompt_lower)
                if match:
                    specs[spec_type] = match.group(0)
                    break

        return PerformanceSpec(
            power=specs.get('power'),
            efficiency=specs.get('efficiency'),
            capacity=specs.get('capacity'),
            speed=specs.get('speed')
        )

    def extract_features(self, prompt: str, design_type: str) -> List[str]:
        """Extract features based on design type"""
        features = []
        prompt_lower = prompt.lower()

        # Get relevant features for design type
        relevant_features = self.design_categories.get(design_type, {}).get('features', [])

        for feature in relevant_features:
            if feature in prompt_lower:
                features.append(feature)

        # Add common features
        common_features = ['smart', 'automatic', 'manual', 'wireless', 'portable', 'compact', 'luxury']
        for feature in common_features:
            if feature in prompt_lower and feature not in features:
                features.append(feature)

        return features

    def extract_components(self, prompt: str, design_type: str) -> List[str]:
        """Extract main components"""
        components = []
        prompt_lower = prompt.lower()

        # Get relevant components for design type
        relevant_components = self.design_categories.get(design_type, {}).get('components', [])

        for component in relevant_components:
            if component in prompt_lower:
                components.append(component)

        return components

    def extract_requirements(self, prompt: str) -> List[str]:
        """Extract design requirements"""
        requirements = [prompt]  # Always include original prompt

        requirement_keywords = ['must', 'should', 'need', 'require', 'essential', 'important']
        sentences = prompt.split('.')

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in requirement_keywords):
                requirements.append(sentence.strip())

        return list(set(requirements))  # Remove duplicates

    def extract_constraints(self, prompt: str) -> List[str]:
        """Extract design constraints"""
        constraints = []
        constraint_keywords = ['budget', 'cost', 'size limit', 'weight limit', 'time', 'deadline']

        for keyword in constraint_keywords:
            if keyword in prompt.lower():
                constraints.append(f"{keyword} constraint")

        return constraints

    def extract_use_cases(self, prompt: str) -> List[str]:
        """Extract intended use cases"""
        use_cases = []
        use_case_keywords = ['for', 'used for', 'intended for', 'purpose', 'application']

        for keyword in use_case_keywords:
            if keyword in prompt.lower():
                # Extract text after the keyword
                parts = prompt.lower().split(keyword)
                if len(parts) > 1:
                    use_case = parts[1].split('.')[0].strip()
                    if use_case:
                        use_cases.append(use_case)

        return use_cases

    def extract_target_audience(self, prompt: str) -> str:
        """Extract target audience"""
        audience_keywords = {
            'professional': ['professional', 'business', 'office', 'commercial'],
            'consumer': ['home', 'personal', 'family', 'consumer'],
            'industrial': ['industrial', 'factory', 'manufacturing'],
            'luxury': ['luxury', 'premium', 'high-end'],
            'budget': ['budget', 'affordable', 'cheap', 'low-cost']
        }

        prompt_lower = prompt.lower()
        for audience, keywords in audience_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return audience

        return None

    def extract_cost(self, prompt: str) -> str:
        """Extract cost information"""
        cost_patterns = [
            r'\$([0-9,]+)',
            r'([0-9,]+)\s*dollars?',
            r'budget[:\s]*\$?([0-9,]+)',
            r'cost[:\s]*\$?([0-9,]+)'
        ]

        for pattern in cost_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                return f"${match.group(1)}"

        # Check for cost ranges
        if any(word in prompt.lower() for word in ['budget', 'affordable', 'cheap']):
            return "budget-friendly"
        elif any(word in prompt.lower() for word in ['luxury', 'premium', 'expensive']):
            return "premium"

        return None

    def extract_timeline(self, prompt: str) -> str:
        """Extract timeline information"""
        timeline_patterns = [
            r'([0-9]+)\s*(?:days?|weeks?|months?|years?)',
            r'deadline[:\s]*([^.]+)',
            r'timeline[:\s]*([^.]+)'
        ]

        for pattern in timeline_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                return match.group(0)

        return None
