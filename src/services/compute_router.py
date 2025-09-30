"""Compute routing logic for LM inference"""

import os
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import httpx

class ComputeRouter:
    def __init__(self):
        self.complexity_threshold = int(os.getenv("COMPLEXITY_THRESHOLD", "100"))
        self.yotta_url = os.getenv("YOTTA_URL", "http://yotta-service:8000")
        self.local_cost_per_token = 0.001  # $0.001 per token
        self.yotta_cost_per_token = 0.01   # $0.01 per token
        self.job_logs = []
        self._load_job_logs()
    
    def _load_job_logs(self):
        """Load job logs from file"""
        log_file = Path("logs/compute_jobs.json")
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    self.job_logs = json.load(f)
            except Exception:
                self.job_logs = []
    
    def _save_job_logs(self):
        """Save job logs to file"""
        Path("logs").mkdir(exist_ok=True)
        try:
            with open("logs/compute_jobs.json", 'w') as f:
                json.dump(self.job_logs, f, indent=2)
        except Exception:
            pass
    
    def _calculate_complexity(self, prompt: str, context: Optional[Dict] = None) -> int:
        """Calculate prompt complexity score"""
        complexity = len(prompt.split())
        
        if context:
            complexity += len(str(context)) // 10
        
        # Add complexity for specific keywords
        complex_keywords = ['detailed', 'complex', 'advanced', 'comprehensive']
        for keyword in complex_keywords:
            if keyword in prompt.lower():
                complexity += 20
        
        return complexity
    
    def _log_job(self, job_type: str, complexity: int, compute_type: str, cost: float):
        """Log compute job"""
        job_log = {
            "timestamp": datetime.now().isoformat(),
            "job_type": job_type,
            "complexity": complexity,
            "compute_type": compute_type,
            "cost": cost
        }
        self.job_logs.append(job_log)
        self._save_job_logs()
    
    async def route_inference(self, prompt: str, context: Optional[Dict] = None, job_type: str = "generation") -> Dict[str, Any]:
        """Route inference to appropriate compute"""
        complexity = self._calculate_complexity(prompt, context)
        
        if complexity < self.complexity_threshold:
            # Use local RTX-3060
            result = await self._local_inference(prompt, context)
            cost = complexity * self.local_cost_per_token
            compute_type = "local_rtx3060"
        else:
            # Route to Yotta
            result = await self._yotta_inference(prompt, context)
            cost = complexity * self.yotta_cost_per_token
            compute_type = "yotta_cloud"
        
        self._log_job(job_type, complexity, compute_type, cost)
        
        return {
            "result": result,
            "compute_type": compute_type,
            "complexity": complexity,
            "cost": cost
        }
    
    async def _local_inference(self, prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Local RTX-3060 inference"""
        from src.lm_adapter.lm_interface import LocalLMAdapter
        adapter = LocalLMAdapter()
        return adapter.run(prompt, context)
    
    async def _yotta_inference(self, prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Yotta cloud inference"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.yotta_url}/inference",
                    json={"prompt": prompt, "context": context}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Yotta inference failed, falling back to local: {e}")
            return await self._local_inference(prompt, context)
    
    def get_job_stats(self) -> Dict[str, Any]:
        """Get compute job statistics"""
        if not self.job_logs:
            return {"total_jobs": 0, "total_cost": 0, "local_jobs": 0, "yotta_jobs": 0}
        
        total_cost = sum(job["cost"] for job in self.job_logs)
        local_jobs = sum(1 for job in self.job_logs if job["compute_type"] == "local_rtx3060")
        yotta_jobs = sum(1 for job in self.job_logs if job["compute_type"] == "yotta_cloud")
        
        return {
            "total_jobs": len(self.job_logs),
            "total_cost": round(total_cost, 4),
            "local_jobs": local_jobs,
            "yotta_jobs": yotta_jobs,
            "avg_complexity": round(sum(job["complexity"] for job in self.job_logs) / len(self.job_logs), 2)
        }

# Global instance
compute_router = ComputeRouter()