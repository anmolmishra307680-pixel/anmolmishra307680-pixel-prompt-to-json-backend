import os
import time
import json
import httpx
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from src.agents.main_agent import MainAgent

class ComputeRouter:
    """Enhanced compute routing with cost tracking and usage logging"""
    
    def __init__(self):
        # GPU detection
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                self.local_gpu = '3060' in gpu_name or 'RTX' in gpu_name
                self.gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3  # GB
                print(f"[INFO] GPU detected: {gpu_name}, RTX-3060 compatible: {self.local_gpu}")
                print(f"[INFO] GPU memory: {self.gpu_memory:.1f}GB")
            else:
                self.local_gpu = False
                self.gpu_memory = 0
                print("[INFO] No CUDA GPU available")
        except ImportError:
            self.local_gpu = False
            self.gpu_memory = 0
            print("[INFO] PyTorch not available, no GPU support")
        
        # Yotta cloud configuration
        self.yotta_key = os.getenv("YOTTA_API_KEY")
        self.yotta_url = os.getenv("YOTTA_ENDPOINT", "https://api.yotta.ai/v1/inference")
        
        # Cost tracking
        self.local_cost_per_token = 0.0001  # $0.0001 per token (electricity)
        self.yotta_cost_per_token = 0.002   # $0.002 per token (cloud)
        
        # Usage tracking
        self.job_stats = {
            "total_jobs": 0,
            "local_jobs": 0,
            "remote_jobs": 0,
            "total_cost": 0.0,
            "local_cost": 0.0,
            "remote_cost": 0.0,
            "total_tokens": 0,
            "avg_response_time": 0.0
        }
        
        # Load existing stats
        self._load_job_stats()
        
        print(f"[INFO] Compute router initialized - Local GPU: {self.local_gpu}, Yotta: {bool(self.yotta_key)}")
    
    def _calculate_complexity(self, prompt: str, context: Optional[str] = None) -> float:
        """Calculate prompt complexity score (0.0 - 1.0)"""
        # Word count factor
        word_count = len(prompt.split())
        word_factor = min(word_count / 100, 0.4)
        
        # Context factor
        context_factor = 0.0
        if context:
            context_factor = min(len(context.split()) / 200, 0.3)
        
        # Complexity keywords
        complex_keywords = ['complex', 'detailed', 'comprehensive', 'advanced', 'multi-story', 'industrial']
        keyword_factor = sum(0.05 for keyword in complex_keywords if keyword in prompt.lower())
        
        # Design type factor
        if any(word in prompt.lower() for word in ['building', 'architecture', 'structure']):
            design_factor = 0.1
        else:
            design_factor = 0.0
        
        total_complexity = min(word_factor + context_factor + keyword_factor + design_factor, 1.0)
        return total_complexity
    
    def _should_use_local(self, complexity: float, job_type: str) -> bool:
        """Determine if job should run locally"""
        if not self.local_gpu:
            return False
        
        # Local GPU thresholds
        if complexity < 0.3:  # Simple jobs
            return True
        elif complexity < 0.6 and job_type in ['generation', 'switch']:  # Medium jobs for specific types
            return True
        elif complexity < 0.8 and self.gpu_memory > 8:  # Complex jobs only if enough memory
            return True
        
        return False
    
    async def route_inference(self, prompt: str, context: Optional[str] = None, job_type: str = "generation") -> Dict[str, Any]:
        """Route inference with enhanced logic and cost tracking"""
        start_time = time.time()
        
        # Calculate complexity
        complexity = self._calculate_complexity(prompt, context)
        
        # Determine routing
        use_local = self._should_use_local(complexity, job_type)
        
        print(f"[COMPUTE] Job type: {job_type}, Complexity: {complexity:.2f}, Route: {'local' if use_local else 'yotta'}")
        
        try:
            if use_local:
                result = await self._run_local(prompt, context, job_type)
                compute_type = "local"
            else:
                result = await self._run_yotta(prompt, context, job_type)
                compute_type = "yotta"
            
            # Track usage and cost
            response_time = time.time() - start_time
            self._track_job(compute_type, prompt, response_time, complexity)
            
            return {
                "result": result,
                "compute": compute_type,
                "complexity": complexity,
                "response_time": response_time,
                "cost_estimate": self._estimate_cost(prompt, compute_type)
            }
            
        except Exception as e:
            # Fallback routing
            print(f"[COMPUTE] Primary route failed: {e}, trying fallback")
            
            if use_local:
                # Fallback to Yotta
                result = await self._run_yotta(prompt, context, job_type)
                compute_type = "yotta_fallback"
            else:
                # Fallback to local
                result = await self._run_local(prompt, context, job_type)
                compute_type = "local_fallback"
            
            response_time = time.time() - start_time
            self._track_job(compute_type, prompt, response_time, complexity)
            
            return {
                "result": result,
                "compute": compute_type,
                "complexity": complexity,
                "response_time": response_time,
                "cost_estimate": self._estimate_cost(prompt, compute_type),
                "fallback": True
            }
    
    async def _run_local(self, prompt: str, context: Optional[str], job_type: str) -> Dict[str, Any]:
        """Run inference on local RTX-3060"""
        agent = MainAgent()
        
        # Add context to prompt if provided
        if context:
            enhanced_prompt = f"{prompt}\n\nContext: {context}"
        else:
            enhanced_prompt = prompt
        
        # Run with parameters optimized for local GPU
        params = {
            "temperature": 0.7,
            "max_tokens": 1024 if job_type == "generation" else 512
        }
        
        spec = agent.run(enhanced_prompt, params)
        return spec.model_dump()
    
    async def _run_yotta(self, prompt: str, context: Optional[str], job_type: str) -> Dict[str, Any]:
        """Run inference on Yotta cloud"""
        if not self.yotta_key or not self.yotta_url:
            raise Exception("Yotta cloud not configured")
        
        payload = {
            "prompt": prompt,
            "context": context,
            "job_type": job_type,
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        headers = {
            "Authorization": f"Bearer {self.yotta_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.yotta_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    
    def _estimate_cost(self, prompt: str, compute_type: str) -> float:
        """Estimate cost for inference"""
        token_count = len(prompt.split()) * 1.3  # Rough token estimation
        
        if "local" in compute_type:
            return token_count * self.local_cost_per_token
        else:
            return token_count * self.yotta_cost_per_token
    
    def _track_job(self, compute_type: str, prompt: str, response_time: float, complexity: float):
        """Track job statistics and costs"""
        token_count = len(prompt.split()) * 1.3
        cost = self._estimate_cost(prompt, compute_type)
        
        # Update stats
        self.job_stats["total_jobs"] += 1
        self.job_stats["total_tokens"] += token_count
        self.job_stats["total_cost"] += cost
        
        if "local" in compute_type:
            self.job_stats["local_jobs"] += 1
            self.job_stats["local_cost"] += cost
        else:
            self.job_stats["remote_jobs"] += 1
            self.job_stats["remote_cost"] += cost
        
        # Update average response time
        total_jobs = self.job_stats["total_jobs"]
        self.job_stats["avg_response_time"] = (
            (self.job_stats["avg_response_time"] * (total_jobs - 1) + response_time) / total_jobs
        )
        
        # Log usage
        self._log_usage(compute_type, prompt, response_time, complexity, cost)
        
        # Save stats
        self._save_job_stats()
    
    def _log_usage(self, compute_type: str, prompt: str, response_time: float, complexity: float, cost: float):
        """Log detailed usage information"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "compute_type": compute_type,
            "prompt_length": len(prompt),
            "complexity": complexity,
            "response_time": response_time,
            "estimated_cost": cost,
            "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt
        }
        
        # Save to usage log file
        log_file = Path("logs/compute_usage.jsonl")
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def _load_job_stats(self):
        """Load job statistics from file"""
        stats_file = Path("logs/job_stats.json")
        if stats_file.exists():
            try:
                with open(stats_file, "r") as f:
                    saved_stats = json.load(f)
                    self.job_stats.update(saved_stats)
            except Exception as e:
                print(f"[WARN] Failed to load job stats: {e}")
    
    def _save_job_stats(self):
        """Save job statistics to file"""
        stats_file = Path("logs/job_stats.json")
        stats_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(stats_file, "w") as f:
                json.dump(self.job_stats, f, indent=2)
        except Exception as e:
            print(f"[WARN] Failed to save job stats: {e}")
    
    def get_job_stats(self) -> Dict[str, Any]:
        """Get comprehensive job statistics"""
        return {
            **self.job_stats,
            "local_gpu_available": self.local_gpu,
            "gpu_memory_gb": self.gpu_memory,
            "yotta_configured": bool(self.yotta_key and self.yotta_url),
            "cost_per_token": {
                "local": self.local_cost_per_token,
                "yotta": self.yotta_cost_per_token
            },
            "efficiency_metrics": {
                "local_percentage": (self.job_stats["local_jobs"] / max(self.job_stats["total_jobs"], 1)) * 100,
                "cost_savings": self.job_stats["remote_cost"] - self.job_stats["local_cost"] if self.job_stats["local_jobs"] > 0 else 0
            }
        }
    
    def get_cost_report(self) -> Dict[str, Any]:
        """Generate detailed cost report"""
        stats = self.get_job_stats()
        
        return {
            "period": "all_time",
            "total_cost": stats["total_cost"],
            "local_cost": stats["local_cost"],
            "remote_cost": stats["remote_cost"],
            "cost_breakdown": {
                "local_percentage": (stats["local_cost"] / max(stats["total_cost"], 0.01)) * 100,
                "remote_percentage": (stats["remote_cost"] / max(stats["total_cost"], 0.01)) * 100
            },
            "efficiency": {
                "jobs_per_dollar": stats["total_jobs"] / max(stats["total_cost"], 0.01),
                "avg_cost_per_job": stats["total_cost"] / max(stats["total_jobs"], 1),
                "cost_savings_vs_all_cloud": (stats["total_jobs"] * self.yotta_cost_per_token * 50) - stats["total_cost"]
            },
            "recommendations": self._get_cost_recommendations(stats)
        }
    
    def _get_cost_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Generate cost optimization recommendations"""
        recommendations = []
        
        local_pct = stats["efficiency_metrics"]["local_percentage"]
        
        if local_pct < 30 and self.local_gpu:
            recommendations.append("Consider routing more simple jobs to local GPU to reduce costs")
        
        if stats["avg_response_time"] > 5.0:
            recommendations.append("High response times detected - consider optimizing model parameters")
        
        if stats["total_cost"] > 100:
            recommendations.append("High compute costs - review job complexity and routing logic")
        
        if not recommendations:
            recommendations.append("Compute routing is optimized for current workload")
        
        return recommendations

# Global instance
router = ComputeRouter()
compute_router = router