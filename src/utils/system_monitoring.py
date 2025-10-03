"""Enhanced monitoring and metrics"""

import os
import time
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
import json

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.job_count = 0
        self.specs_generated = 0
        self.evaluations_completed = 0
        self.rl_iterations_total = 0
        self.agent_calls = {"MainAgent": 0, "EvaluatorAgent": 0, "RLAgent": 0}
        
    def increment_requests(self):
        """Increment request counter"""
        self.request_count += 1
    
    def increment_errors(self):
        """Increment error counter"""
        self.error_count += 1
    
    def increment_jobs(self):
        """Increment job counter"""
        self.job_count += 1
    
    def increment_specs(self):
        """Increment spec generation counter"""
        self.specs_generated += 1
        self.agent_calls["MainAgent"] += 1
    
    def increment_evaluations(self):
        """Increment evaluation counter"""
        self.evaluations_completed += 1
        self.agent_calls["EvaluatorAgent"] += 1
    
    def increment_rl_iterations(self, count: int = 1):
        """Increment RL iteration counter"""
        self.rl_iterations_total += count
        self.agent_calls["RLAgent"] += 1
    
    def get_health_metrics(self) -> Dict[str, Any]:
        """Get system health metrics"""
        uptime = time.time() - self.start_time
        
        # Get compute job stats
        try:
            from src.services.compute_router import compute_router
            job_stats = compute_router.get_job_stats()
        except Exception:
            job_stats = {"total_jobs": 0, "total_cost": 0}
        
        # Get database status
        try:
            from src.data.database import Database
            db = Database()
            session = db.get_session()
            session.close()
            db_status = "healthy"
        except Exception:
            db_status = "degraded"
        
        return {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "uptime_seconds": round(uptime, 2),
            "requests_total": self.request_count,
            "errors_total": self.error_count,
            "jobs_total": self.job_count,
            "specs_generated": self.specs_generated,
            "evaluations_completed": self.evaluations_completed,
            "rl_iterations_total": self.rl_iterations_total,
            "agent_calls": self.agent_calls,
            "compute_jobs": job_stats.get("total_jobs", 0),
            "compute_cost": job_stats.get("total_cost", 0),
            "database_status": db_status,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_prometheus_metrics(self) -> str:
        """Get Prometheus format metrics"""
        metrics = self.get_health_metrics()
        
        prometheus_metrics = f"""# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total {metrics['requests_total']}

# HELP http_errors_total Total HTTP errors
# TYPE http_errors_total counter
http_errors_total {metrics['errors_total']}

# HELP specs_generated_total Total specifications generated
# TYPE specs_generated_total counter
specs_generated_total {metrics['specs_generated']}

# HELP evaluations_completed_total Total evaluations completed
# TYPE evaluations_completed_total counter
evaluations_completed_total {metrics['evaluations_completed']}

# HELP rl_iterations_total Total RL training iterations
# TYPE rl_iterations_total counter
rl_iterations_total {metrics['rl_iterations_total']}

# HELP agent_calls_total Total agent calls by type
# TYPE agent_calls_total counter
agent_calls_total{{agent="MainAgent"}} {metrics['agent_calls']['MainAgent']}
agent_calls_total{{agent="EvaluatorAgent"}} {metrics['agent_calls']['EvaluatorAgent']}
agent_calls_total{{agent="RLAgent"}} {metrics['agent_calls']['RLAgent']}

# HELP compute_jobs_total Total compute jobs
# TYPE compute_jobs_total counter
compute_jobs_total {metrics['compute_jobs']}

# HELP compute_cost_total Total compute cost
# TYPE compute_cost_total gauge
compute_cost_total {metrics['compute_cost']}

# HELP system_uptime_seconds System uptime in seconds
# TYPE system_uptime_seconds gauge
system_uptime_seconds {metrics['uptime_seconds']}
"""
        return prometheus_metrics

# Global instance
system_monitor = SystemMonitor()

# Sentry integration
def init_sentry():
    """Initialize Sentry error tracking"""
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        
        sentry_dsn = os.getenv("SENTRY_DSN")
        if sentry_dsn:
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[FastApiIntegration()],
                traces_sample_rate=0.1,
                environment=os.getenv("ENVIRONMENT", "development")
            )
            print("[OK] Sentry monitoring initialized")
            return True
    except ImportError:
        print("[WARN] Sentry not available")
    return False