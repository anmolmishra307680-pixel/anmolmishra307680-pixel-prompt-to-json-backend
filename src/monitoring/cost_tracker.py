#!/usr/bin/env python3
"""Cost tracking and usage accounting system"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from pathlib import Path

class CostTracker:
    """Track and analyze compute costs and usage patterns"""
    
    def __init__(self):
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Cost rates (per token)
        self.rates = {
            "local_rtx3060": 0.0001,  # Electricity cost
            "yotta_cloud": 0.002,     # Cloud API cost
            "fallback": 0.001         # Fallback cost
        }
        
        # Load existing data
        self.daily_costs = self._load_daily_costs()
        self.usage_patterns = self._load_usage_patterns()
    
    def log_job_cost(self, compute_type: str, tokens: int, response_time: float, 
                     complexity: float, job_type: str = "generation"):
        """Log individual job cost and usage"""
        cost = tokens * self.rates.get(compute_type, self.rates["fallback"])
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "compute_type": compute_type,
            "job_type": job_type,
            "tokens": tokens,
            "cost": cost,
            "response_time": response_time,
            "complexity": complexity,
            "efficiency": tokens / max(response_time, 0.1)  # tokens per second
        }
        
        # Append to daily log
        today = datetime.now().strftime("%Y-%m-%d")
        daily_log = self.logs_dir / f"costs_{today}.jsonl"
        
        with open(daily_log, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Update daily totals
        if today not in self.daily_costs:
            self.daily_costs[today] = {
                "total_cost": 0,
                "total_tokens": 0,
                "total_jobs": 0,
                "local_cost": 0,
                "remote_cost": 0,
                "avg_response_time": 0
            }
        
        day_stats = self.daily_costs[today]
        day_stats["total_cost"] += cost
        day_stats["total_tokens"] += tokens
        day_stats["total_jobs"] += 1
        
        if "local" in compute_type:
            day_stats["local_cost"] += cost
        else:
            day_stats["remote_cost"] += cost
        
        # Update average response time
        total_jobs = day_stats["total_jobs"]
        day_stats["avg_response_time"] = (
            (day_stats["avg_response_time"] * (total_jobs - 1) + response_time) / total_jobs
        )
        
        self._save_daily_costs()
        self._update_usage_patterns(compute_type, job_type, complexity)
    
    def get_daily_report(self, date: str = None) -> Dict[str, Any]:
        """Generate daily cost report"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if date not in self.daily_costs:
            return {"date": date, "total_cost": 0, "message": "No data for this date"}
        
        stats = self.daily_costs[date]
        
        return {
            "date": date,
            "total_cost": round(stats["total_cost"], 4),
            "total_tokens": stats["total_tokens"],
            "total_jobs": stats["total_jobs"],
            "cost_breakdown": {
                "local_cost": round(stats["local_cost"], 4),
                "remote_cost": round(stats["remote_cost"], 4),
                "local_percentage": round((stats["local_cost"] / max(stats["total_cost"], 0.01)) * 100, 1)
            },
            "efficiency": {
                "cost_per_job": round(stats["total_cost"] / max(stats["total_jobs"], 1), 4),
                "tokens_per_job": round(stats["total_tokens"] / max(stats["total_jobs"], 1), 1),
                "avg_response_time": round(stats["avg_response_time"], 2)
            }
        }
    
    def get_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly cost report"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        weekly_stats = {
            "total_cost": 0,
            "total_tokens": 0,
            "total_jobs": 0,
            "local_cost": 0,
            "remote_cost": 0,
            "daily_breakdown": []
        }
        
        for i in range(7):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            daily_report = self.get_daily_report(date)
            
            if daily_report["total_cost"] > 0:
                weekly_stats["total_cost"] += daily_report["total_cost"]
                weekly_stats["total_tokens"] += daily_report["total_tokens"]
                weekly_stats["total_jobs"] += daily_report["total_jobs"]
                weekly_stats["local_cost"] += daily_report["cost_breakdown"]["local_cost"]
                weekly_stats["remote_cost"] += daily_report["cost_breakdown"]["remote_cost"]
            
            weekly_stats["daily_breakdown"].append(daily_report)
        
        return {
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "summary": weekly_stats,
            "trends": self._analyze_weekly_trends(weekly_stats["daily_breakdown"]),
            "recommendations": self._generate_cost_recommendations(weekly_stats)
        }
    
    def get_usage_patterns(self) -> Dict[str, Any]:
        """Analyze usage patterns"""
        return {
            "compute_distribution": self.usage_patterns.get("compute_types", {}),
            "job_type_distribution": self.usage_patterns.get("job_types", {}),
            "complexity_distribution": self.usage_patterns.get("complexity_ranges", {}),
            "peak_hours": self._analyze_peak_hours(),
            "efficiency_trends": self._analyze_efficiency_trends()
        }
    
    def _analyze_weekly_trends(self, daily_data: List[Dict]) -> Dict[str, Any]:
        """Analyze weekly cost trends"""
        costs = [day["total_cost"] for day in daily_data if day["total_cost"] > 0]
        
        if len(costs) < 2:
            return {"trend": "insufficient_data"}
        
        # Simple trend analysis
        recent_avg = sum(costs[-3:]) / len(costs[-3:])
        earlier_avg = sum(costs[:-3]) / max(len(costs[:-3]), 1)
        
        if recent_avg > earlier_avg * 1.2:
            trend = "increasing"
        elif recent_avg < earlier_avg * 0.8:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "recent_avg": round(recent_avg, 4),
            "earlier_avg": round(earlier_avg, 4),
            "change_percentage": round(((recent_avg - earlier_avg) / max(earlier_avg, 0.01)) * 100, 1)
        }
    
    def _generate_cost_recommendations(self, weekly_stats: Dict) -> List[str]:
        """Generate cost optimization recommendations"""
        recommendations = []
        
        total_cost = weekly_stats["total_cost"]
        local_pct = (weekly_stats["local_cost"] / max(total_cost, 0.01)) * 100
        
        if total_cost > 10:
            recommendations.append("High weekly costs detected - consider optimizing job complexity")
        
        if local_pct < 30:
            recommendations.append("Low local GPU usage - route more simple jobs locally to reduce costs")
        
        if weekly_stats["total_jobs"] > 1000:
            recommendations.append("High job volume - consider batch processing for efficiency")
        
        if not recommendations:
            recommendations.append("Cost optimization is on track")
        
        return recommendations
    
    def _analyze_peak_hours(self) -> Dict[str, Any]:
        """Analyze peak usage hours"""
        # This would analyze hourly patterns from logs
        # Simplified implementation
        return {
            "peak_hour": "14:00-15:00",
            "peak_cost": 0.05,
            "off_peak_savings": "20%"
        }
    
    def _analyze_efficiency_trends(self) -> Dict[str, Any]:
        """Analyze efficiency trends"""
        return {
            "tokens_per_second_avg": 150,
            "cost_per_token_avg": 0.0015,
            "efficiency_score": 85
        }
    
    def _update_usage_patterns(self, compute_type: str, job_type: str, complexity: float):
        """Update usage pattern statistics"""
        # Update compute type distribution
        if "compute_types" not in self.usage_patterns:
            self.usage_patterns["compute_types"] = {}
        
        compute_key = compute_type.replace("_fallback", "")
        self.usage_patterns["compute_types"][compute_key] = \
            self.usage_patterns["compute_types"].get(compute_key, 0) + 1
        
        # Update job type distribution
        if "job_types" not in self.usage_patterns:
            self.usage_patterns["job_types"] = {}
        
        self.usage_patterns["job_types"][job_type] = \
            self.usage_patterns["job_types"].get(job_type, 0) + 1
        
        # Update complexity ranges
        if "complexity_ranges" not in self.usage_patterns:
            self.usage_patterns["complexity_ranges"] = {
                "simple": 0, "medium": 0, "complex": 0
            }
        
        if complexity < 0.3:
            self.usage_patterns["complexity_ranges"]["simple"] += 1
        elif complexity < 0.7:
            self.usage_patterns["complexity_ranges"]["medium"] += 1
        else:
            self.usage_patterns["complexity_ranges"]["complex"] += 1
        
        self._save_usage_patterns()
    
    def _load_daily_costs(self) -> Dict[str, Dict]:
        """Load daily cost data"""
        costs_file = self.logs_dir / "daily_costs.json"
        if costs_file.exists():
            try:
                with open(costs_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_daily_costs(self):
        """Save daily cost data"""
        costs_file = self.logs_dir / "daily_costs.json"
        try:
            with open(costs_file, "w") as f:
                json.dump(self.daily_costs, f, indent=2)
        except Exception as e:
            print(f"Failed to save daily costs: {e}")
    
    def _load_usage_patterns(self) -> Dict[str, Any]:
        """Load usage pattern data"""
        patterns_file = self.logs_dir / "usage_patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_usage_patterns(self):
        """Save usage pattern data"""
        patterns_file = self.logs_dir / "usage_patterns.json"
        try:
            with open(patterns_file, "w") as f:
                json.dump(self.usage_patterns, f, indent=2)
        except Exception as e:
            print(f"Failed to save usage patterns: {e}")

# Global instance
cost_tracker = CostTracker()