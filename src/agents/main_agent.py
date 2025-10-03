import json
import os
from typing import Optional
from pathlib import Path
from datetime import datetime
from src.schemas.legacy_schema import DesignSpec, MaterialSpec, DimensionSpec
from src.schemas.universal_schema import UniversalDesignSpec
from src.prompt_agent.extractor import PromptExtractor
from src.prompt_agent.universal_extractor import UniversalPromptExtractor
from src.core.lm_adapter import LocalLMAdapter

class MainAgent:
    def __init__(self):
        self.extractor = PromptExtractor()  # Keep for backward compatibility
        self.universal_extractor = UniversalPromptExtractor()  # New universal extractor
        self.lm_adapter = LocalLMAdapter()  # True LM adapter with standardized interface
        self.spec_outputs_dir = Path("spec_outputs")
        self.spec_outputs_dir.mkdir(exist_ok=True)

    def run(self, prompt: str, params: Optional[dict] = None) -> UniversalDesignSpec:
        """Standardized LM interface: lm.run(prompt, params)"""
        # Use true LM adapter for generation
        spec_data = self.lm_adapter.run(prompt, params)
        
        # Convert to UniversalDesignSpec
        spec = self._create_universal_spec_from_data(spec_data)
        
        # Always save spec to file
        try:
            spec_file = self.save_spec(spec, prompt)
            print(f"[LM] Spec saved to file: {spec_file}")
        except Exception as e:
            print(f"[LM] Failed to save spec file: {e}")

        # Save to DB via clean interface
        try:
            from src.data.database import Database
            db = Database()
            spec_id = db.save_spec(prompt, spec.model_dump(), 'LMAdapter')
            print(f"[LM] Spec saved to DB with ID: {spec_id}")
        except Exception as e:
            print(f"[LM] DB save failed, using fallback: {e}")

        return spec

    def _create_universal_spec_from_data(self, spec_data: dict) -> UniversalDesignSpec:
        """Create UniversalDesignSpec from LM adapter output"""
        try:
            from src.schemas.universal_schema import MaterialSpec as UniversalMaterialSpec, DimensionSpec as UniversalDimensionSpec
            
            # Convert materials with IDs
            materials = []
            for mat in spec_data.get('materials', []):
                materials.append(UniversalMaterialSpec(
                    type=mat.get('type', 'standard'),
                    grade=mat.get('grade'),
                    properties=mat.get('properties', {})
                ))
            
            # Convert dimensions
            dim_data = spec_data.get('dimensions', {})
            dimensions = UniversalDimensionSpec(
                length=dim_data.get('length'),
                width=dim_data.get('width'),
                height=dim_data.get('height'),
                depth=dim_data.get('depth'),
                diameter=dim_data.get('diameter'),
                area=dim_data.get('area'),
                volume=dim_data.get('volume'),
                weight=dim_data.get('weight'),
                units=dim_data.get('units', 'metric')
            )
            
            # Create performance specs
            performance = spec_data.get('performance', {})
            
            return UniversalDesignSpec(
                design_type=spec_data.get('design_type', 'general'),
                category=spec_data.get('category', 'standard'),
                objects=spec_data.get('objects', []),
                materials=materials,
                dimensions=dimensions,
                performance=performance,
                features=spec_data.get('features', []),
                components=spec_data.get('components', []),
                requirements=spec_data.get('requirements', []),
                constraints=spec_data.get('constraints', []),
                use_cases=spec_data.get('use_cases', []),
                target_audience=spec_data.get('target_audience'),
                estimated_cost=spec_data.get('estimated_cost'),
                timeline=spec_data.get('timeline'),
                metadata=spec_data.get('metadata', {}),
                timestamp=spec_data.get('timestamp')
            )
            
        except Exception as e:
            print(f"[LM] Failed to create UniversalDesignSpec: {e}")
            return self._create_fallback_spec(spec_data.get('requirements', ['Unknown prompt'])[0])

    def generate_spec(self, prompt: str, params: Optional[dict] = None) -> UniversalDesignSpec:
        """Legacy method - redirects to standardized interface"""
        return self.run(prompt, params)
    
    def _generate_with_llm(self, prompt: str) -> DesignSpec:
        """Generate specs using LLM processing"""
        try:
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "Generate building specifications as JSON with: building_type, stories, materials, dimensions, features, requirements"
                }, {
                    "role": "user",
                    "content": f"Design specifications for: {prompt}"
                }],
                temperature=0.7
            )

            content = response.choices[0].message.content
            return self._parse_llm_response(content, prompt)
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")

    def _parse_llm_response(self, content: str, prompt: str) -> UniversalDesignSpec:
        """Parse LLM response into DesignSpec"""
        try:
            import json
            data = json.loads(content)
            from src.schemas.universal_schema import MaterialSpec as UniversalMaterialSpec, DimensionSpec as UniversalDimensionSpec
            return UniversalDesignSpec(
                design_type="building",
                category=data.get("building_type", "general"),
                materials=[UniversalMaterialSpec(type=m) for m in data.get("materials", ["concrete"])],
                dimensions=UniversalDimensionSpec(**data.get("dimensions", {"length": 20, "width": 15, "height": 3, "area": 300})),
                features=data.get("features", []),
                requirements=data.get("requirements", [prompt])
            )
        except Exception:
            return self._convert_to_universal(self._generate_with_rules(prompt))

    def _generate_with_universal_rules(self, prompt: str) -> UniversalDesignSpec:
        """Generate universal specification from any design prompt"""
        try:
            return self.universal_extractor.extract_spec(prompt)
        except ValueError as e:
            # If not design-related, raise the error
            raise e
        except Exception as e:
            # For other errors, create a basic spec
            return self._create_fallback_spec(prompt)

    def _generate_with_rules(self, prompt: str) -> DesignSpec:
        """Generate specification from any design prompt"""
        # Extract design type from prompt
        design_type = self._extract_design_type(prompt)

        if design_type == "building":
            # Generate building specification
            base_spec = self.extractor.extract_spec(prompt)
            enhanced_spec = self._enhance_specification(base_spec, prompt)
            return enhanced_spec
        else:
            # Generate specification for other design types
            return self._generate_general_spec(prompt, design_type)


    def _enhance_specification(self, spec: DesignSpec, prompt: str) -> DesignSpec:
        """Enhance specification with additional logic"""
        # Add default materials if none specified
        if not spec.materials:
            if 'steel' in prompt.lower():
                spec.materials.append(MaterialSpec(type="steel", grade="A36"))
            elif 'concrete' in prompt.lower():
                spec.materials.append(MaterialSpec(type="concrete", grade="C30"))
            else:
                spec.materials.append(MaterialSpec(type="steel", grade="standard"))

        # Estimate dimensions if not provided
        if spec.dimensions.length is None and spec.dimensions.width is None:
            # Default dimensions based on building type and stories
            if spec.building_type == 'warehouse' or spec.building_type == 'industrial':
                spec.dimensions.length = 40.0
                spec.dimensions.width = 30.0
            elif spec.stories <= 2:
                spec.dimensions.length = 20.0
                spec.dimensions.width = 15.0
            else:
                spec.dimensions.length = 30.0
                spec.dimensions.width = 25.0

            spec.dimensions.height = spec.stories * 3.5  # 3.5m per story
            spec.dimensions.area = spec.dimensions.length * spec.dimensions.width

        # Add default features based on building type
        if not spec.features:
            if spec.building_type == 'residential':
                spec.features.extend(['balcony', 'parking'])
            elif spec.building_type == 'commercial' or spec.building_type == 'office':
                spec.features.extend(['elevator', 'parking'])
            elif spec.building_type == 'warehouse' or spec.building_type == 'industrial':
                spec.features.extend(['parking', 'loading'])
            else:
                spec.features.append('parking')

        return spec


    def save_spec(self, spec: UniversalDesignSpec, prompt: str = "") -> str:
        """Save specification to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"design_spec_{timestamp}.json"
        filepath = self.spec_outputs_dir / filename

        output_data = {
            "prompt": prompt,
            "specification": spec.model_dump(),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator": "MainAgent"
            }
        }

        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)

        return str(filepath)

    def improve_spec_with_feedback(self, spec: UniversalDesignSpec, feedback: list, suggestions: list) -> UniversalDesignSpec:
        """Improve specification based on feedback with enhanced error handling"""
        try:
            improved_spec = spec.model_copy() if hasattr(spec, 'model_copy') else spec

            # Validate inputs
            if not isinstance(feedback, list) or not isinstance(suggestions, list):
                raise ValueError("Feedback and suggestions must be lists")

            # Apply improvements based on feedback
            improvements_applied = 0
            for suggestion in suggestions:
                if not isinstance(suggestion, str):
                    continue

                suggestion_lower = suggestion.lower()

                if "materials" in suggestion_lower or "material" in suggestion_lower:
                    if not improved_spec.materials:
                        from src.schemas.universal_schema import MaterialSpec
                        improved_spec.materials.append(MaterialSpec(type="steel"))
                        improvements_applied += 1

                elif "dimensions" in suggestion_lower or "size" in suggestion_lower:
                    if not improved_spec.dimensions.length:
                        improved_spec.dimensions.length = 25.0
                        improved_spec.dimensions.width = 20.0
                        improved_spec.dimensions.area = 500.0
                        improvements_applied += 1

                elif "features" in suggestion_lower or "feature" in suggestion_lower:
                    if len(improved_spec.features) < 3:
                        # Context-aware feature suggestions based on design type
                        if improved_spec.design_type == "building":
                            if improved_spec.category == "office":
                                new_features = ['elevator', 'parking', 'conference_room']
                            elif improved_spec.category == "residential":
                                new_features = ['balcony', 'parking', 'garden']
                            else:
                                new_features = ['parking', 'security']
                        elif improved_spec.design_type == "vehicle":
                            new_features = ['gps', 'bluetooth', 'safety_features']
                        elif improved_spec.design_type == "electronics":
                            new_features = ['touchscreen', 'wireless', 'fast_charging']
                        else:
                            new_features = ['smart', 'efficient', 'durable']

                        for feature in new_features:
                            if feature not in improved_spec.features:
                                improved_spec.features.append(feature)
                        improvements_applied += 1

            if improvements_applied == 0:
                print("[INFO] No applicable improvements found in suggestions")

            return improved_spec

        except Exception as e:
            print(f"[ERROR] Failed to improve spec: {str(e)}")
            return spec  # Return original spec on error

    def _extract_design_type(self, prompt: str) -> str:
        """Extract the type of design from prompt"""
        prompt_lower = prompt.lower()

        # Email keywords
        if any(word in prompt_lower for word in ['email', 'message', 'letter', 'announcement', 'communication']):
            return "email"

        # Task/Project keywords
        elif any(word in prompt_lower for word in ['task', 'project', 'plan', 'timeline', 'schedule', 'launch']):
            return "task"

        # Building-related keywords (including residential)
        elif any(word in prompt_lower for word in ['building', 'house', 'office', 'warehouse', 'hospital', 'construction', 'architect', 'residential', 'apartment']):
            return "building"

        # Software/App keywords
        elif any(word in prompt_lower for word in ['chatbot', 'app', 'software', 'system', 'platform', 'website', 'api']):
            return "software"

        # Product keywords
        elif any(word in prompt_lower for word in ['product', 'device', 'gadget', 'thermostat', 'sensor', 'controller']):
            return "product"

        # Default to general design
        else:
            return "general"

    def _generate_general_spec(self, prompt: str, design_type: str) -> DesignSpec:
        """Generate specification for non-building designs"""
        from src.schemas.legacy_schema import DimensionSpec, MaterialSpec

        # Extract key components from prompt
        components = self._extract_components(prompt)
        features = self._extract_general_features(prompt)

        # For email/task prompts, create more appropriate specs
        if design_type in ['email', 'task']:
            spec = DesignSpec(
                building_type=design_type,
                stories=1,
                materials=[MaterialSpec(type="content", grade="professional")],
                dimensions=DimensionSpec(length=len(prompt.split()), width=1, height=1, area=len(prompt.split())),
                features=features + ["professional", "concise"],
                requirements=[prompt]
            )
        else:
            spec = DesignSpec(
                building_type=design_type,
                stories=len(components) if components else 1,
                materials=[MaterialSpec(type=comp, grade="standard") for comp in components[:3]],
                dimensions=DimensionSpec(length=1, width=1, height=1, area=1),
                features=features,
                requirements=[prompt]
            )

        return spec

    def _extract_components(self, prompt: str) -> list:
        """Extract main components from prompt"""
        components = []
        prompt_lower = prompt.lower()

        # Common design components
        component_keywords = {
            'interface': ['ui', 'interface', 'screen', 'display'],
            'database': ['database', 'storage', 'data'],
            'api': ['api', 'endpoint', 'service'],
            'sensor': ['sensor', 'detector', 'monitor'],
            'controller': ['controller', 'control', 'processor'],
            'network': ['network', 'wifi', 'bluetooth', 'connection']
        }

        for component, keywords in component_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                components.append(component)

        return components

    def _extract_general_features(self, prompt: str) -> list:
        """Extract features from any design prompt"""
        features = []
        prompt_lower = prompt.lower()

        # Common features across designs
        feature_keywords = {
            'professional': ['professional', 'business', 'formal'],
            'concise': ['short', 'brief', 'concise', 'quick'],
            'announcement': ['announce', 'launch', 'release'],
            'team_communication': ['team', 'marketing', 'group'],
            'automation': ['auto', 'automatic', 'smart'],
            'security': ['secure', 'security', 'auth', 'login'],
            'mobile': ['mobile', 'phone', 'app'],
            'cloud': ['cloud', 'online', 'remote'],
            'analytics': ['analytics', 'reporting', 'data'],
            'notification': ['notify', 'alert', 'notification']
        }

        for feature, keywords in feature_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                features.append(feature)

        # Default feature if none found
        if not features:
            features.append('basic_functionality')

        return features

    def _convert_to_universal(self, old_spec: DesignSpec) -> UniversalDesignSpec:
        """Convert old DesignSpec to UniversalDesignSpec"""
        from src.universal_schema import MaterialSpec as UniversalMaterialSpec, DimensionSpec as UniversalDimensionSpec

        # Convert materials
        universal_materials = []
        for material in old_spec.materials:
            universal_materials.append(UniversalMaterialSpec(
                type=material.type,
                grade=material.grade,
                properties=material.properties
            ))

        # Convert dimensions
        universal_dimensions = UniversalDimensionSpec(
            length=old_spec.dimensions.length,
            width=old_spec.dimensions.width,
            height=old_spec.dimensions.height,
            area=old_spec.dimensions.area,
            units="metric"
        )

        return UniversalDesignSpec(
            design_type="building",
            category=old_spec.building_type,
            materials=universal_materials,
            dimensions=universal_dimensions,
            features=old_spec.features,
            requirements=old_spec.requirements,
            components=["structure", "foundation"] if old_spec.building_type != "general" else []
        )

    def _create_fallback_spec(self, prompt: str) -> UniversalDesignSpec:
        """Create a basic fallback specification with proper structure"""
        from src.schemas.universal_schema import MaterialSpec as UniversalMaterialSpec, DimensionSpec as UniversalDimensionSpec
        import uuid
        from datetime import datetime

        return UniversalDesignSpec(
            design_type="general",
            category="custom",
            objects=[{
                "id": str(uuid.uuid4()),
                "type": "main_component",
                "material": "standard",
                "editable": True,
                "properties": {}
            }],
            materials=[UniversalMaterialSpec(type="standard", grade="basic", properties={})],
            dimensions=UniversalDimensionSpec(units="metric"),
            performance={"other_specs": {}},
            features=["basic_functionality"],
            requirements=[prompt],
            components=["main_component"],
            constraints=[],
            use_cases=[prompt[:50]],
            target_audience="general",
            estimated_cost="medium",
            timeline="medium_term",
            metadata={
                "editable": True,
                "version": "1.0",
                "author": "MainAgent_Fallback",
                "created_at": datetime.now().isoformat(),
                "modified_at": datetime.now().isoformat(),
                "tags": [],
                "notes": "Fallback specification"
            },
            timestamp=datetime.now().isoformat()
        )
