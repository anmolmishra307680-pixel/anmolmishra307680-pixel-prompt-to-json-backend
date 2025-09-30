from src.schemas.legacy_schema import DesignSpec, EvaluationResult
from src.evaluator.criteria import EvaluationCriteria
from src.evaluator.report import ReportGenerator

class EvaluatorAgent:
    def __init__(self):
        self.criteria = EvaluationCriteria()
        self.report_generator = ReportGenerator()

    def run(self, spec, prompt: str):
        """BHIV Core Hook: Single entry point for orchestration"""
        evaluation = self.evaluate_spec(spec, prompt)

        # Save to DB via clean interface
        try:
            from src.data.database import Database
            db = Database()
            spec_id = getattr(spec, 'id', 'unknown')
            eval_id = db.save_eval(spec_id, prompt, evaluation.model_dump(), evaluation.score)
            print(f"Evaluation saved to DB with ID: {eval_id}")
        except Exception as e:
            print(f"DB save failed, using fallback: {e}")

        return evaluation

    def evaluate_spec(self, spec: DesignSpec, prompt: str = "") -> EvaluationResult:
        """Evaluate a design specification"""
        evaluation = self.criteria.evaluate(spec)

        # Generate report
        report_path = self.report_generator.generate_report(spec, evaluation, prompt)
        print(f"Evaluation report saved to: {report_path}")

        return evaluation

    def batch_evaluate(self, specs_and_prompts: list) -> list:
        """Evaluate multiple specifications"""
        results = []
        reports_data = []

        for spec, prompt in specs_and_prompts:
            evaluation = self.criteria.evaluate(spec)
            results.append(evaluation)

            # Collect data for summary report
            report_data = {
                "prompt": prompt,
                "design_specification": spec.model_dump(),
                "evaluation_results": evaluation.model_dump()
            }
            reports_data.append(report_data)

        # Generate summary report
        summary_path = self.report_generator.generate_summary_report(reports_data)
        print(f"Summary report saved to: {summary_path}")

        return results

    def get_improvement_suggestions(self, evaluation: EvaluationResult) -> list:
        """Get specific improvement suggestions based on evaluation"""
        suggestions = evaluation.suggestions.copy()

        # Add specific suggestions based on scores
        if evaluation.completeness < 70:
            suggestions.append("Add more detailed material specifications")
            suggestions.append("Include specific building dimensions")

        if evaluation.format_validity < 80:
            suggestions.append("Ensure all required fields are properly formatted")

        return suggestions
