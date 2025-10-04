"""Cost tracking and billing for hybrid compute routing"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

class CostTracker:
    """Track compute costs and usage for RTX-3060 + Yotta hybrid setup"""
    
    def __init__(self):
        self.costs_dir = Path("logs/costs")
        self.costs_dir.mkdir(parents=True, exist_ok=True)
        
        # Cost rates (per token)
        self.local_cost = 0.0001  # $0.0001 per token (electricity)
        self.yotta_cost = 0.002   # $0.002 per token (cloud)
        
        # Daily tracking
        self.daily_costs = {}
        self.load_daily_costs()
    
    def load_daily_costs(self):
        """Load daily cost data"""
        costs_file = self.costs_dir / "daily_costs.json"
        if costs_file.exists():
            try:
                with open(costs_file, 'r') as f:
                    self.daily_costs = json.load(f)
            except Exception:
                self.daily_costs = {}
    
    def save_daily_costs(self):
        """Save daily cost data"""
        costs_file = self.costs_dir / "daily_costs.json"
        try:
            with open(costs_file, 'w') as f:
                json.dump(self.daily_costs, f, indent=2)
        except Exception as e:
            print(f"[COST] Failed to save costs: {e}")
    
    async def log_job(self, compute_type: str, prompt: str, job_type: str = "generation", 
                     response_time: float = 0.0, complexity: float = 0.0):
        """Log job cost and usage"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Estimate tokens and cost
        token_count = len(prompt.split()) * 1.3  # Rough estimation
        
        if "local" in compute_type:
            cost = token_count * self.local_cost
        else:
            cost = token_count * self.yotta_cost
        
        # Initialize day if needed
        if today not in self.daily_costs:
            self.daily_costs[today] = {
                "local_jobs": 0,
                "yotta_jobs": 0,
                "local_cost": 0.0,
                "yotta_cost": 0.0,
                "total_tokens": 0,
                "jobs": []
            }
        
        # Update daily totals
        day_data = self.daily_costs[today]
        day_data["total_tokens"] += token_count
        
        if "local" in compute_type:
            day_data["local_jobs"] += 1
            day_data["local_cost"] += cost
        else:
            day_data["yotta_jobs"] += 1
            day_data["yotta_cost"] += cost
        
        # Log individual job
        job_entry = {
            "timestamp": datetime.now().isoformat(),
            "compute_type": compute_type,
            "job_type": job_type,
            "tokens": token_count,
            "cost": cost,
            "response_time": response_time,
            "complexity": complexity
        }
        day_data["jobs"].append(job_entry)
        
        # Save updated costs
        self.save_daily_costs()
        
        print(f"[COST] Logged {compute_type} job: ${cost:.4f}")
    
    def get_daily_report(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Get daily cost report"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if date not in self.daily_costs:
            return {
                "date": date,
                "total_cost": 0.0,
                "local_cost": 0.0,
                "yotta_cost": 0.0,
                "total_jobs": 0,
                "cost_savings": 0.0
            }
        
        day_data = self.daily_costs[date]
        total_cost = day_data["local_cost"] + day_data["yotta_cost"]
        total_jobs = day_data["local_jobs"] + day_data["yotta_jobs"]
        
        # Calculate savings vs all-cloud
        all_cloud_cost = day_data["total_tokens"] * self.yotta_cost
        cost_savings = all_cloud_cost - total_cost
        
        return {
            "date": date,
            "total_cost": total_cost,
            "local_cost": day_data["local_cost"],
            "yotta_cost": day_data["yotta_cost"],
            "total_jobs": total_jobs,
            "local_jobs": day_data["local_jobs"],
            "yotta_jobs": day_data["yotta_jobs"],
            "cost_savings": cost_savings,
            "savings_percentage": (cost_savings / max(all_cloud_cost, 0.01)) * 100,
            "avg_cost_per_job": total_cost / max(total_jobs, 1)
        }
    
    def get_weekly_report(self) -> Dict[str, Any]:
        """Get weekly cost report with trends"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        weekly_data = {
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "daily_reports": [],
            "totals": {
                "total_cost": 0.0,
                "local_cost": 0.0,
                "yotta_cost": 0.0,
                "total_jobs": 0,
                "cost_savings": 0.0
            }
        }
        
        # Collect daily data
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            daily_report = self.get_daily_report(date_str)
            weekly_data["daily_reports"].append(daily_report)
            
            # Add to totals
            weekly_data["totals"]["total_cost"] += daily_report["total_cost"]
            weekly_data["totals"]["local_cost"] += daily_report["local_cost"]
            weekly_data["totals"]["yotta_cost"] += daily_report["yotta_cost"]
            weekly_data["totals"]["total_jobs"] += daily_report["total_jobs"]
            weekly_data["totals"]["cost_savings"] += daily_report["cost_savings"]
            
            current_date += timedelta(days=1)
        
        # Calculate trends
        if len(weekly_data["daily_reports"]) >= 2:
            recent_avg = sum(d["total_cost"] for d in weekly_data["daily_reports"][-3:]) / 3
            older_avg = sum(d["total_cost"] for d in weekly_data["daily_reports"][:3]) / 3
            trend = "increasing" if recent_avg > older_avg else "decreasing"
        else:
            trend = "stable"
        
        weekly_data["trend"] = trend
        weekly_data["avg_daily_cost"] = weekly_data["totals"]["total_cost"] / 7
        
        return weekly_data
    
    def get_usage_patterns(self) -> Dict[str, Any]:
        """Analyze usage patterns for optimization"""
        if not self.daily_costs:
            return {"message": "No usage data available"}
        
        # Analyze recent 30 days
        recent_days = list(self.daily_costs.keys())[-30:]
        
        local_jobs = sum(self.daily_costs[day]["local_jobs"] for day in recent_days)
        yotta_jobs = sum(self.daily_costs[day]["yotta_jobs"] for day in recent_days)
        total_jobs = local_jobs + yotta_jobs
        
        if total_jobs == 0:
            return {"message": "No jobs in recent period"}
        
        local_percentage = (local_jobs / total_jobs) * 100
        
        # Cost efficiency
        total_cost = sum(
            self.daily_costs[day]["local_cost"] + self.daily_costs[day]["yotta_cost"] 
            for day in recent_days
        )
        total_savings = sum(
            self.get_daily_report(day)["cost_savings"] for day in recent_days
        )
        
        return {
            "period_days": len(recent_days),
            "total_jobs": total_jobs,
            "local_percentage": local_percentage,
            "yotta_percentage": 100 - local_percentage,
            "total_cost": total_cost,
            "total_savings": total_savings,
            "efficiency_score": min(100, (total_savings / max(total_cost, 0.01)) * 100),
            "recommendations": self._get_optimization_recommendations(local_percentage, total_cost)
        }
    
    def _get_optimization_recommendations(self, local_percentage: float, total_cost: float) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if local_percentage < 50:
            recommendations.append("Consider routing more simple jobs to local RTX-3060 to reduce costs")
        
        if local_percentage > 90:
            recommendations.append("High local usage - consider Yotta cloud for heavy workloads")
        
        if total_cost > 50:
            recommendations.append("High compute costs - review job complexity and routing thresholds")
        
        if not recommendations:
            recommendations.append("Compute routing is well-optimized for cost efficiency")
        
        return recommendations

# Global instance
cost_tracker = CostTracker()