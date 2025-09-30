"""Report Generator for Evaluations"""

import json
from datetime import datetime
from pathlib import Path
from src.schemas.legacy_schema import DesignSpec, EvaluationResult

class ReportGenerator:
    def __init__(self):
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
    
    def generate_report(self, spec: DesignSpec, evaluation: EvaluationResult, prompt: str = "") -> str:
        """Generate evaluation report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_report_{timestamp}.json"
        filepath = self.reports_dir / filename
        
        report_data = {
            "prompt": prompt,
            "specification": spec.model_dump(),
            "evaluation": evaluation.model_dump(),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator": "ReportGenerator"
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def generate_summary_report(self, reports_data: list) -> str:
        """Generate summary report for multiple evaluations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_report_{timestamp}.json"
        filepath = self.reports_dir / filename
        
        # Calculate summary statistics
        scores = [report["evaluation_results"]["score"] for report in reports_data]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        summary_data = {
            "summary": {
                "total_evaluations": len(reports_data),
                "average_score": avg_score,
                "highest_score": max(scores) if scores else 0,
                "lowest_score": min(scores) if scores else 0
            },
            "reports": reports_data,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator": "ReportGenerator"
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(summary_data, f, indent=2, default=str)
        
        return str(filepath)