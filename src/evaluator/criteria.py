from src.schema import DesignSpec, EvaluationResult
from src.universal_schema import UniversalDesignSpec
from typing import List, Tuple

class EvaluationCriteria:
    def __init__(self):
        self.weights = {
            'completeness': 0.4,
            'format_validity': 0.3,
            'feasibility': 0.3
        }

    def check_completeness(self, spec) -> Tuple[float, List[str]]:
        """Check completeness of design specification"""
        score = 0
        feedback = []

        # Detect design type
        design_type = getattr(spec, 'design_type', 'building')

        # Type/category check - handle both old and new schema
        category = getattr(spec, 'building_type', None) or getattr(spec, 'category', None)
        
        if category and category != 'general':
            score += 20
        elif design_type and design_type != 'building':
            # For non-building designs, having design_type is sufficient
            score += 20
        else:
            type_name = design_type.title() if design_type != 'building' else 'Building'
            feedback.append(f"{type_name} type not specified or too generic")

        # Design-specific completeness checks
        if design_type == 'building':
            stories = getattr(spec, 'stories', 1)
            if stories and stories > 0:
                score += 20
            else:
                feedback.append("Number of stories not specified")
        elif design_type == 'vehicle':
            # Check for vehicle-specific dimensions
            if (spec.dimensions.height or spec.dimensions.width or
                spec.dimensions.diameter or spec.dimensions.length):
                score += 20
            else:
                feedback.append("Vehicle dimensions not specified")
        else:
            # For electronics, appliances, furniture - check any dimension
            if (spec.dimensions.length or spec.dimensions.width or
                spec.dimensions.height or spec.dimensions.diameter):
                score += 20
            else:
                feedback.append(f"{design_type.title()} dimensions not specified")

        if spec.materials:
            score += 20
        else:
            feedback.append("No materials specified")

        if spec.dimensions.length or spec.dimensions.width or spec.dimensions.area or spec.dimensions.height:
            score += 20
        else:
            feedback.append("No dimensions specified")

        if spec.features:
            score += 20
        else:
            feedback.append("No special features specified")

        return score, feedback

    def check_format_validity(self, spec) -> Tuple[float, List[str]]:
        """Check format validity of specification"""
        score = 100
        feedback = []

        try:
            # Validate Pydantic model
            spec.model_validate(spec.model_dump())
        except Exception as e:
            score -= 50
            feedback.append(f"Schema validation error: {str(e)}")

        # Check data types - handle both schemas
        stories = getattr(spec, 'stories', 1)
        if stories and (not isinstance(stories, int) or stories < 1):
            score -= 25
            feedback.append("Invalid number of stories")

        if spec.dimensions.length and spec.dimensions.length <= 0:
            score -= 25
            feedback.append("Invalid dimensions")

        return max(0, score), feedback

    def check_feasibility(self, spec) -> Tuple[float, List[str]]:
        """Check feasibility of design"""
        score = 100
        feedback = []

        # Get design type
        design_type = getattr(spec, 'design_type', 'building')

        if design_type == 'building':
            # Building-specific feasibility checks
            stories = getattr(spec, 'stories', 1)
            if stories and stories > 50:
                score -= 30
                feedback.append("Excessive number of stories may not be feasible")
            elif stories and stories > 20:
                feedback.append("High-rise building requires advanced engineering")

            if spec.dimensions.height and spec.dimensions.height > 200:
                score -= 20
                feedback.append("Building height may be excessive")
            elif spec.dimensions.height and spec.dimensions.height > 100:
                feedback.append("Tall building requires elevator systems")

            # Material compatibility for buildings
            materials = [m.type for m in spec.materials] if spec.materials else []
            if 'wood' in materials and stories and stories > 5:
                score -= 25
                feedback.append("Wood construction may not be suitable for high-rise buildings")
            elif 'steel' in materials:
                feedback.append("Steel frame provides excellent structural integrity")
            elif 'concrete' in materials:
                feedback.append("Concrete construction offers durability and fire resistance")
            
            if score >= 90:
                feedback.append("Well-designed building with appropriate specifications")

        elif design_type == 'vehicle':
            # Vehicle-specific feasibility checks
            if spec.dimensions.length and spec.dimensions.length > 20:
                score -= 20
                feedback.append("Vehicle length may be excessive for standard roads")
            elif spec.dimensions.length and spec.dimensions.length > 15:
                feedback.append("Large vehicle may have parking limitations")

            if spec.dimensions.height and spec.dimensions.height > 4:
                score -= 15
                feedback.append("Vehicle height may exceed bridge clearances")
            elif spec.dimensions.height and spec.dimensions.height < 1.2:
                feedback.append("Low profile design enhances aerodynamics")

            materials = [m.type for m in spec.materials] if spec.materials else []
            if 'wood' in materials:
                score -= 20
                feedback.append("Wood may not be suitable for vehicle construction")
            elif 'carbon_fiber' in materials:
                feedback.append("Carbon fiber provides excellent strength-to-weight ratio")
            elif 'aluminum' in materials:
                feedback.append("Aluminum construction offers lightweight durability")
            
            if score >= 90:
                feedback.append("Excellent vehicle design with optimal specifications")

        elif design_type == 'electronics':
            # Electronics feasibility checks
            if spec.dimensions.weight and spec.dimensions.weight > 10:
                score -= 15
                feedback.append("Device may be too heavy for portable use")
            elif spec.dimensions.weight and spec.dimensions.weight < 0.5:
                feedback.append("Lightweight design enhances portability")
            
            materials = [m.type for m in spec.materials] if spec.materials else []
            if 'plastic' in materials:
                feedback.append("Plastic housing provides cost-effective protection")
            elif 'aluminum' in materials:
                feedback.append("Aluminum casing offers premium feel and heat dissipation")
            
            if score >= 90:
                feedback.append("Well-engineered electronic device with practical design")

        elif design_type == 'appliance':
            # Appliance feasibility checks
            if spec.dimensions.width and spec.dimensions.width > 3:
                score -= 10
                feedback.append("Appliance may be too wide for standard spaces")
            elif spec.dimensions.width and spec.dimensions.width < 0.6:
                feedback.append("Compact design suitable for small kitchens")
            
            materials = [m.type for m in spec.materials] if spec.materials else []
            if 'stainless_steel' in materials:
                feedback.append("Stainless steel provides durability and easy cleaning")
            elif 'plastic' in materials:
                feedback.append("Plastic components reduce weight and cost")
            
            if score >= 90:
                feedback.append("Practical appliance design with user-friendly features")

        elif design_type == 'furniture':
            # Furniture feasibility checks
            materials = [m.type for m in spec.materials] if spec.materials else []
            
            # Check material combinations
            if 'steel' in materials and spec.dimensions.weight and spec.dimensions.weight > 100:
                score -= 15
                feedback.append("Steel furniture may be too heavy for practical use")
            
            # Check dining table specific dimensions
            if hasattr(spec, 'category') and 'dining' in spec.category.lower():
                if spec.dimensions.length and spec.dimensions.length > 300:
                    score -= 10
                    feedback.append("Dining table length may be excessive for most rooms")
                if spec.dimensions.height and (spec.dimensions.height < 70 or spec.dimensions.height > 80):
                    score -= 5
                    feedback.append("Dining table height should be 70-80cm for comfort")
            
            # Always provide constructive feedback for furniture
            if score == 100:
                feedback.append("Excellent furniture design with practical dimensions and materials")

        return max(0, score), feedback

    def evaluate(self, spec) -> EvaluationResult:
        """Perform complete evaluation of design specification"""
        completeness_score, completeness_feedback = self.check_completeness(spec)
        format_score, format_feedback = self.check_format_validity(spec)
        feasibility_score, feasibility_feedback = self.check_feasibility(spec)

        # Calculate weighted overall score
        overall_score = (
            completeness_score * self.weights['completeness'] +
            format_score * self.weights['format_validity'] +
            feasibility_score * self.weights['feasibility']
        )

        all_feedback = completeness_feedback + format_feedback + feasibility_feedback

        # Generate suggestions - always provide helpful suggestions
        suggestions = []
        if completeness_score < 80:
            suggestions.append("Add more detailed specifications")
        if format_score < 90:
            suggestions.append("Fix format and validation issues")
        if feasibility_score < 80:
            suggestions.append("Review design feasibility constraints")
        
        # Add design-type specific suggestions
        design_type = getattr(spec, 'design_type', 'building')
        if design_type == 'building':
            if not suggestions:
                suggestions.extend([
                    "Consider energy efficiency ratings",
                    "Add accessibility features compliance",
                    "Include seismic resistance specifications"
                ])
        elif design_type == 'furniture':
            if not suggestions:
                suggestions.extend([
                    "Consider adding sustainability certifications",
                    "Specify assembly requirements and hardware",
                    "Include care and maintenance instructions"
                ])
        elif design_type == 'vehicle':
            if not suggestions:
                suggestions.extend([
                    "Add safety features and ratings",
                    "Consider fuel efficiency specifications",
                    "Include emission standards compliance"
                ])
        elif design_type == 'electronics':
            if not suggestions:
                suggestions.extend([
                    "Include power consumption details",
                    "Specify connectivity options",
                    "Add electromagnetic compatibility ratings"
                ])
        elif design_type == 'appliance':
            if not suggestions:
                suggestions.extend([
                    "Include energy efficiency ratings",
                    "Specify noise level measurements",
                    "Add warranty and service information"
                ])
            if not suggestions:
                suggestions.extend([
                    "Include power consumption details",
                    "Specify connectivity options"
                ])

        return EvaluationResult(
            score=round(overall_score, 2),
            completeness=completeness_score,
            format_validity=format_score,
            feedback=all_feedback,
            suggestions=suggestions
        )
