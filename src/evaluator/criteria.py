"""Evaluation Criteria for Design Specifications"""

from src.schemas.legacy_schema import DesignSpec, EvaluationResult

class EvaluationCriteria:
    def __init__(self):
        pass
    
    def evaluate(self, spec: DesignSpec) -> EvaluationResult:
        """Evaluate a design specification"""
        
        # Calculate completeness score
        completeness = self._calculate_completeness(spec)
        
        # Calculate format validity
        format_validity = self._calculate_format_validity(spec)
        
        # Calculate feasibility
        feasibility = self._calculate_feasibility(spec)
        
        # Calculate overall score
        overall_score = (completeness + format_validity + feasibility) / 3
        
        # Generate suggestions
        suggestions = self._generate_suggestions(spec, completeness, format_validity, feasibility)
        
        return EvaluationResult(
            score=overall_score,
            completeness=completeness,
            format_validity=format_validity,
            feasibility=feasibility,
            suggestions=suggestions
        )
    
    def _calculate_completeness(self, spec: DesignSpec) -> float:
        """Calculate completeness score"""
        score = 0
        total_checks = 6
        
        if spec.building_type and spec.building_type != "general":
            score += 1
        if spec.stories and spec.stories > 0:
            score += 1
        if spec.materials and len(spec.materials) > 0:
            score += 1
        if spec.dimensions and spec.dimensions.area and spec.dimensions.area > 0:
            score += 1
        if spec.features and len(spec.features) > 0:
            score += 1
        if spec.requirements and len(spec.requirements) > 0:
            score += 1
        
        return (score / total_checks) * 100
    
    def _calculate_format_validity(self, spec: DesignSpec) -> float:
        """Calculate format validity score"""
        score = 0
        total_checks = 4
        
        # Check building type is valid
        valid_types = ["residential", "commercial", "office", "warehouse", "industrial", "hospital", "general"]
        if spec.building_type in valid_types:
            score += 1
        
        # Check stories is reasonable
        if spec.stories and 1 <= spec.stories <= 100:
            score += 1
        
        # Check dimensions are positive
        if (spec.dimensions and spec.dimensions.length and spec.dimensions.length > 0 and
            spec.dimensions.width and spec.dimensions.width > 0):
            score += 1
        
        # Check materials have valid types
        if spec.materials and all(m.type for m in spec.materials):
            score += 1
        
        return (score / total_checks) * 100
    
    def _calculate_feasibility(self, spec: DesignSpec) -> float:
        """Calculate feasibility score"""
        score = 0
        total_checks = 3
        
        # Check reasonable dimensions
        if (spec.dimensions and spec.dimensions.area and 
            10 <= spec.dimensions.area <= 100000):  # 10 to 100k sq meters
            score += 1
        
        # Check reasonable story count for building type
        if spec.building_type == "residential" and spec.stories <= 50:
            score += 1
        elif spec.building_type in ["commercial", "office"] and spec.stories <= 200:
            score += 1
        elif spec.building_type in ["warehouse", "industrial"] and spec.stories <= 10:
            score += 1
        else:
            score += 0.5  # Partial credit for other types
        
        # Check material compatibility
        if spec.materials and len(spec.materials) <= 5:  # Reasonable number of materials
            score += 1
        
        return (score / total_checks) * 100
    
    def _generate_suggestions(self, spec: DesignSpec, completeness: float, 
                            format_validity: float, feasibility: float) -> list:
        """Generate improvement suggestions"""
        suggestions = []
        
        if completeness < 80:
            if not spec.materials or len(spec.materials) == 0:
                suggestions.append("Add material specifications")
            if not spec.features or len(spec.features) == 0:
                suggestions.append("Add building features")
            if not spec.dimensions or not spec.dimensions.area:
                suggestions.append("Specify building dimensions")
        
        if format_validity < 80:
            if spec.building_type == "general":
                suggestions.append("Specify a more specific building type")
            if not spec.stories or spec.stories <= 0:
                suggestions.append("Specify number of stories")
        
        if feasibility < 80:
            if spec.dimensions and spec.dimensions.area and spec.dimensions.area > 50000:
                suggestions.append("Consider reducing building size for feasibility")
            if spec.stories and spec.stories > 50:
                suggestions.append("Consider reducing number of stories")
        
        if not suggestions:
            suggestions.append("Specification looks good!")
        
        return suggestions