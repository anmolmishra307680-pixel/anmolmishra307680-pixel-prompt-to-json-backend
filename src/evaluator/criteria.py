"""Evaluation Criteria for Design Specifications"""

from src.schemas.legacy_schema import DesignSpec, EvaluationResult

class EvaluationCriteria:
    def __init__(self):
        pass
    
    def evaluate(self, spec) -> EvaluationResult:
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
    
    def _calculate_completeness(self, spec) -> float:
        """Calculate completeness score - handles both legacy and universal schemas"""
        score = 0
        total_checks = 6
        
        # Handle both building_type (legacy) and category (universal)
        building_type = getattr(spec, 'building_type', None) or getattr(spec, 'category', None)
        if building_type and building_type != "general":
            score += 1
        
        # Stories only exists in legacy schema
        stories = getattr(spec, 'stories', None)
        if stories and stories > 0:
            score += 1
        else:
            score += 0.5  # Partial credit for universal schema
        
        if spec.materials and len(spec.materials) > 0:
            score += 1
        if spec.dimensions and getattr(spec.dimensions, 'area', None) and spec.dimensions.area > 0:
            score += 1
        if spec.features and len(spec.features) > 0:
            score += 1
        if spec.requirements and len(spec.requirements) > 0:
            score += 1
        
        return (score / total_checks) * 100
    
    def _calculate_format_validity(self, spec) -> float:
        """Calculate format validity score - handles both schemas"""
        score = 0
        total_checks = 4
        
        # Check building type/category is valid
        valid_types = ["residential", "commercial", "office", "warehouse", "industrial", "hospital", "general", "building", "vehicle", "electronics"]
        building_type = getattr(spec, 'building_type', None) or getattr(spec, 'category', None)
        if building_type in valid_types:
            score += 1
        
        # Check stories is reasonable (legacy only)
        stories = getattr(spec, 'stories', None)
        if stories and 1 <= stories <= 100:
            score += 1
        else:
            score += 0.5  # Partial credit for universal schema
        
        # Check dimensions are positive
        if (spec.dimensions and getattr(spec.dimensions, 'length', None) and spec.dimensions.length > 0 and
            getattr(spec.dimensions, 'width', None) and spec.dimensions.width > 0):
            score += 1
        
        # Check materials have valid types
        if spec.materials and all(getattr(m, 'type', None) for m in spec.materials):
            score += 1
        
        return (score / total_checks) * 100
    
    def _calculate_feasibility(self, spec) -> float:
        """Calculate feasibility score - handles both schemas"""
        score = 0
        total_checks = 3
        
        # Check reasonable dimensions
        if (spec.dimensions and getattr(spec.dimensions, 'area', None) and 
            10 <= spec.dimensions.area <= 100000):  # 10 to 100k sq meters
            score += 1
        
        # Check reasonable story count for building type (legacy only)
        building_type = getattr(spec, 'building_type', None) or getattr(spec, 'category', None)
        stories = getattr(spec, 'stories', None)
        
        if stories:
            if building_type == "residential" and stories <= 50:
                score += 1
            elif building_type in ["commercial", "office"] and stories <= 200:
                score += 1
            elif building_type in ["warehouse", "industrial"] and stories <= 10:
                score += 1
            else:
                score += 0.5  # Partial credit for other types
        else:
            score += 0.7  # Partial credit for universal schema without stories
        
        # Check material compatibility
        if spec.materials and len(spec.materials) <= 5:  # Reasonable number of materials
            score += 1
        
        return (score / total_checks) * 100
    
    def _generate_suggestions(self, spec, completeness: float, 
                            format_validity: float, feasibility: float) -> list:
        """Generate improvement suggestions - handles both schemas"""
        suggestions = []
        
        if completeness < 80:
            if not spec.materials or len(spec.materials) == 0:
                suggestions.append("Add material specifications")
            if not spec.features or len(spec.features) == 0:
                suggestions.append("Add design features")
            if not spec.dimensions or not getattr(spec.dimensions, 'area', None):
                suggestions.append("Specify dimensions")
        
        if format_validity < 80:
            building_type = getattr(spec, 'building_type', None) or getattr(spec, 'category', None)
            if building_type == "general":
                suggestions.append("Specify a more specific design type")
            stories = getattr(spec, 'stories', None)
            if stories and stories <= 0:
                suggestions.append("Specify number of stories")
        
        if feasibility < 80:
            if spec.dimensions and getattr(spec.dimensions, 'area', None) and spec.dimensions.area > 50000:
                suggestions.append("Consider reducing size for feasibility")
            stories = getattr(spec, 'stories', None)
            if stories and stories > 50:
                suggestions.append("Consider reducing number of stories")
        
        if not suggestions:
            suggestions.append("Specification looks good!")
        
        return suggestions