"""Log pruning system for production scalability"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List

class LogPruner:
    def __init__(self, retention_days: int = 30):
        self.retention_days = retention_days
        self.cutoff_date = datetime.now() - timedelta(days=retention_days)

    def prune_feedback_logs(self) -> Dict[str, Any]:
        """Prune old feedback logs"""
        feedback_file = Path("logs/feedback_log.json")
        if not feedback_file.exists():
            return {"pruned": 0, "message": "No feedback log file found"}

        with open(feedback_file, 'r') as f:
            logs = json.load(f)

        original_count = len(logs)
        pruned_logs = []

        for log in logs:
            try:
                log_date = datetime.fromisoformat(log.get('timestamp', ''))
                if log_date > self.cutoff_date:
                    pruned_logs.append(log)
            except:
                # Keep logs with invalid timestamps
                pruned_logs.append(log)

        with open(feedback_file, 'w') as f:
            json.dump(pruned_logs, f, indent=2)

        return {
            "pruned": original_count - len(pruned_logs),
            "remaining": len(pruned_logs),
            "message": f"Pruned {original_count - len(pruned_logs)} old feedback logs"
        }

    def prune_iteration_logs(self) -> Dict[str, Any]:
        """Prune old iteration logs"""
        iteration_file = Path("logs/iteration_logs.json")
        if not iteration_file.exists():
            return {"pruned": 0, "message": "No iteration log file found"}

        with open(iteration_file, 'r') as f:
            logs = json.load(f)

        original_count = len(logs)
        pruned_logs = []

        for log in logs:
            try:
                log_date = datetime.fromisoformat(log.get('created_at', ''))
                if log_date > self.cutoff_date:
                    pruned_logs.append(log)
            except:
                pruned_logs.append(log)

        with open(iteration_file, 'w') as f:
            json.dump(pruned_logs, f, indent=2)

        return {
            "pruned": original_count - len(pruned_logs),
            "remaining": len(pruned_logs),
            "message": f"Pruned {original_count - len(pruned_logs)} old iteration logs"
        }

    def prune_all_logs(self) -> Dict[str, Any]:
        """Prune all log types"""
        results = {
            "feedback": self.prune_feedback_logs(),
            "iterations": self.prune_iteration_logs(),
            "total_pruned": 0
        }

        results["total_pruned"] = (
            results["feedback"]["pruned"] +
            results["iterations"]["pruned"]
        )

        return results
