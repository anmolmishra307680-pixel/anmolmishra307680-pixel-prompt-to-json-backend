"""Feedback Loop for RL Training"""

import json
from pathlib import Path
from datetime import datetime
from src.schemas.legacy_schema import DesignSpec, EvaluationResult

class FeedbackLoop:
    def __init__(self):
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
    
    def calculate_reward(self, evaluation: EvaluationResult, previous_score: float = 0, binary_rewards: bool = False) -> float:
        """Calculate reward based on evaluation"""
        if binary_rewards:
            return 1.0 if evaluation.score > 80 else 0.0
        else:
            # Continuous reward based on improvement
            improvement = evaluation.score - previous_score
            base_reward = evaluation.score / 100.0
            improvement_bonus = max(0, improvement / 100.0)
            return base_reward + improvement_bonus
    
    def log_iteration(self, prompt: str, spec_before: DesignSpec, spec_after: DesignSpec, 
                     evaluation: EvaluationResult, reward: float, iteration: int):
        """Log iteration data"""
        log_entry = {
            "iteration": iteration,
            "prompt": prompt,
            "spec_before": spec_before.model_dump(),
            "spec_after": spec_after.model_dump(),
            "evaluation": evaluation.model_dump(),
            "reward": reward,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to iteration logs
        iteration_file = self.logs_dir / "iteration_logs.json"
        logs = []
        if iteration_file.exists():
            with open(iteration_file, 'r') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
        
        logs.append(log_entry)
        with open(iteration_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)
    
    def get_feedback_for_prompt(self, prompt: str) -> list:
        """Get feedback suggestions for a prompt"""
        # Simple rule-based feedback
        suggestions = []
        prompt_lower = prompt.lower()
        
        if "sustainable" in prompt_lower or "green" in prompt_lower:
            suggestions.append("Consider solar panels")
            suggestions.append("Use eco-friendly materials")
        
        if "office" in prompt_lower:
            suggestions.append("Include elevator for multi-story")
            suggestions.append("Add parking facilities")
        
        if "residential" in prompt_lower:
            suggestions.append("Include balcony")
            suggestions.append("Consider garden space")
        
        return suggestions
    
    def get_learning_insights(self) -> dict:
        """Get learning insights from logs"""
        iteration_file = self.logs_dir / "iteration_logs.json"
        if not iteration_file.exists():
            return {"total_iterations": 0, "average_score": 0}
        
        with open(iteration_file, 'r') as f:
            try:
                logs = json.load(f)
            except:
                return {"total_iterations": 0, "average_score": 0}
        
        if not logs:
            return {"total_iterations": 0, "average_score": 0}
        
        scores = [log["evaluation"]["score"] for log in logs if "evaluation" in log]
        
        return {
            "total_iterations": len(logs),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "final_score": scores[-1] if scores else 0,
            "improvement": scores[-1] - scores[0] if len(scores) > 1 else 0
        }
    
    def log_comparison(self, prompt: str, rule_spec: DesignSpec, rl_spec: dict, 
                      rule_eval: EvaluationResult, rl_score: float):
        """Log comparison between approaches"""
        comparison_entry = {
            "prompt": prompt,
            "rule_based": {
                "spec": rule_spec.model_dump(),
                "evaluation": rule_eval.model_dump()
            },
            "advanced_rl": {
                "spec": rl_spec,
                "score": rl_score
            },
            "timestamp": datetime.now().isoformat()
        }
        
        comparison_file = self.logs_dir / "comparison_logs.json"
        logs = []
        if comparison_file.exists():
            with open(comparison_file, 'r') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
        
        logs.append(comparison_entry)
        with open(comparison_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)