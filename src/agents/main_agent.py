import json
import os
from typing import Optional
from pathlib import Path
from datetime import datetime
from src.schemas.legacy_schema import DesignSpec, MaterialSpec, DimensionSpec
from src.schemas.universal_schema import UniversalDesignSpec
from src.prompt_agent.extractor import PromptExtractor
from src.prompt_agent.universal_extractor import UniversalPromptExtractor

class MainAgent:
    def __init__(self):
        self.extractor = PromptExtractor()  # Keep for backward compatibility
        self.universal_extractor = UniversalPromptExtractor()  # New universal extractor
        self.spec_outputs_dir = Path("spec_outputs")
        self.spec_outputs_dir.mkdir(exist_ok=True)

    def run(self, prompt: str, use_universal: bool = True) -> UniversalDesignSpec:
        """BHIV Core Hook: Single entry point for orchestration"""
        spec = self.generate_spec(prompt, use_universal=use_universal)

        # Always save spec to file
        try:
            spec_file = self.save_spec(spec, prompt)
            print(f"Spec saved to file: {spec_file}")
        except Exception as e:
            print(f"Failed to save spec file: {e}")

        # Save to DB via clean interface
        try:
            from src.data.database import Database
            db = Database()
            spec_id = db.save_spec(prompt, spec.model_dump(), 'MainAgent')
            print(f"Spec saved to DB with ID: {spec_id}")
        except Exception as e:
            print(f"DB save failed, using fallback: {e}")

        return spec

    def generate_spec(self, prompt: str, use_llm: bool = False, use_universal: bool = True) -> UniversalDesignSpec:
        """Generate design specification with LLM integration"""
        if not prompt or len(prompt.strip()) < 3:
            raise ValueError("Prompt must be at least 3 characters long")

        # Try LLM generation if API key available
        if os.getenv("OPENAI_API_KEY") and use_llm:
            try:
                return self._generate_with_llm(prompt)
            except Exception as e:
                print(f"[WARNING] LLM generation failed: {e}, using rule-based")

        try:
            if use_universal:
                return self._generate_with_universal_rules(prompt)
            else:
                return self._convert_to_universal(self._generate_with_rules(prompt))
        except Exception as e:
            raise RuntimeError(f"Failed to generate specification: {str(e)}")

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
        """Create a basic fallback specification"""
        from src.schemas.universal_schema import MaterialSpec as UniversalMaterialSpec, DimensionSpec as UniversalDimensionSpec

        return UniversalDesignSpec(
            design_type="general",
            category="custom",
            materials=[UniversalMaterialSpec(type="standard", grade="basic")],
            dimensions=UniversalDimensionSpec(units="metric"),
            features=["basic_functionality"],
            requirements=[prompt],
            components=["main_component"]
        )
