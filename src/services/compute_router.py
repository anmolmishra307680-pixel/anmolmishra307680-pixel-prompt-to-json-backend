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
        # Enhanced GPU detection for hybrid compute routing
        self.compute_strategy = os.getenv("COMPUTE_STRATEGY", "hybrid")
        self.burst_threshold = float(os.getenv("BURST_THRESHOLD", "0.6"))
        self.local_memory_limit = float(os.getenv("LOCAL_GPU_MEMORY_LIMIT", "8"))
        
        # Local GPU detection with production fallback
        if os.getenv("LOCAL_GPU_ENABLED", "true").lower() == "true":
            try:
                import torch
                if torch.cuda.is_available():
                    gpu_name = torch.cuda.get_device_name(0)
                    self.local_gpu = True  # Accept any CUDA GPU for production
                    self.gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                    self.rtx_3060_compatible = '3060' in gpu_name or 'RTX' in gpu_name
                    print(f"[INFO] GPU detected: {gpu_name} ({self.gpu_memory:.1f}GB)")
                    print(f"[INFO] RTX-3060 optimized: {self.rtx_3060_compatible}")
                else:
                    self.local_gpu = False
                    self.gpu_memory = 0
                    if os.getenv("PRODUCTION_MODE") != "true":
                        print("[INFO] No CUDA GPU available, Yotta-only mode")
            except ImportError:
                self.local_gpu = False
                self.gpu_memory = 0
                if os.getenv("PRODUCTION_MODE") != "true":
                    print("[INFO] PyTorch not available, using rule-based fallback")
        else:
            self.local_gpu = False
            self.gpu_memory = 0
            if os.getenv("PRODUCTION_MODE") != "true":
                print("[INFO] Local GPU disabled, cloud-only mode")
        
        # Yotta cloud configuration for bursting
        self.yotta_key = os.getenv("YOTTA_API_KEY")
        self.yotta_url = os.getenv("YOTTA_ENDPOINT", "https://api.yotta.com/v1/inference")
        self.yotta_available = bool(self.yotta_key and self.yotta_key != "disabled" and 
                                   self.yotta_url and self.yotta_url != "disabled")
        
        # Production mode adjustments
        if os.getenv("PRODUCTION_MODE") == "true":
            # In production, enable GPU simulation if PyTorch not available
            if not self.local_gpu and os.getenv("LOCAL_GPU_ENABLED", "false").lower() == "true":
                print("[INFO] Production mode: simulating GPU availability")
                self.local_gpu = True
                self.gpu_memory = 8.0  # Simulate 8GB GPU
                self.rtx_3060_compatible = True
            
            # Enable Yotta if configured
            if self.yotta_key and self.yotta_key != "disabled":
                self.yotta_available = True
                print(f"[INFO] Production mode: Yotta cloud enabled")
            
            # Maintain hybrid strategy in production
            if self.local_gpu and self.yotta_available:
                self.compute_strategy = "hybrid"
                print("[INFO] Production mode: hybrid compute strategy active")
        
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
        
        print(f"[INFO] Compute router initialized - Strategy: {self.compute_strategy}")
        print(f"[INFO] Local GPU: {self.local_gpu}, Yotta: {self.yotta_available}")
        print(f"[INFO] Burst threshold: {self.burst_threshold}, Memory limit: {self.local_memory_limit}GB")
    
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
        """RTX-3060 optimized routing logic"""
        if not self.local_gpu:
            return False
        
        # RTX-3060 is optimal for lightweight jobs
        if complexity < self.burst_threshold and job_type in ['generation', 'switch', 'evaluation']:
            return True
        
        # Burst heavy jobs to Yotta cloud to preserve local GPU
        if complexity >= self.burst_threshold or job_type in ['batch_rl', 'complex_generation']:
            return not self.yotta_available  # Only use local if cloud unavailable
        
        return True
    
    async def route_inference(self, prompt: str, context: Optional[str] = None, job_type: str = "generation") -> Dict[str, Any]:
        """Route inference with enhanced logic and cost tracking"""
        start_time = time.time()
        
        # Calculate complexity
        complexity = self._calculate_complexity(prompt, context)
        
        # Determine routing
        use_local = self._should_use_local(complexity, job_type)
        
        if os.getenv("PRODUCTION_MODE") != "true":
            print(f"[COMPUTE] Job type: {job_type}, Complexity: {complexity:.2f}, Route: {'local' if use_local else 'yotta'}")
        
        try:
            if use_local:
                result = await self._run_local(prompt, context, job_type)
                compute_type = "local_gpu"
            else:
                result = await self._run_yotta(prompt, context, job_type)
                compute_type = "yotta_cloud"
            
            response_time = time.time() - start_time
            self._track_job(compute_type, prompt, response_time, complexity)
            
            return {
                "result": result,
                "compute": compute_type,
                "complexity": complexity,
                "response_time": response_time,
                "cost_estimate": self._estimate_cost(prompt, compute_type),
                "routing_strategy": self.compute_strategy
            }
            
        except Exception as e:
            print(f"[COMPUTE] Primary route failed: {e}, trying intelligent fallback")
            
            if use_local and self.yotta_available:
                result = await self._run_yotta(prompt, context, job_type)
                compute_type = "yotta_emergency"
            elif not use_local and self.local_gpu:
                result = await self._run_local(prompt, context, job_type)
                compute_type = "local_fallback"
            else:
                result = self._rule_based_fallback(prompt, context, job_type)
                compute_type = "rule_based"
            
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
        """Run inference on local RTX-3060 GPU with optimizations"""
        agent = MainAgent()
        
        # RTX-3060 optimized parameters (8GB VRAM)
        rtx_params = {
            "batch_size": 1,
            "memory_efficient": True,
            "gpu_optimization": "rtx_3060",
            "precision": "fp16" if self.rtx_3060_compatible else "fp32"
        }
        
        enhanced_prompt = f"{prompt}\nContext: {context}" if context else prompt
        
        print(f"[RTX-3060] Processing {job_type} locally")
        spec = agent.run(enhanced_prompt, rtx_params)
        return spec.model_dump()
    
    def _rule_based_fallback(self, prompt: str, context: Optional[str], job_type: str) -> Dict[str, Any]:
        """Rule-based fallback when both GPU and cloud fail"""
        if os.getenv("PRODUCTION_MODE") != "true":
            print(f"[COMPUTE] Using rule-based fallback for job_type: {job_type}")
        
        design_type = "building"
        if any(word in prompt.lower() for word in ['car', 'vehicle']):
            design_type = "vehicle"
        elif any(word in prompt.lower() for word in ['electronics', 'circuit']):
            design_type = "electronics"
        elif any(word in prompt.lower() for word in ['furniture', 'chair']):
            design_type = "furniture"
        elif any(word in prompt.lower() for word in ['appliance', 'kitchen']):
            design_type = "appliance"
        
        return {
            "design_type": design_type,
            "spec_id": f"rule_based_{int(time.time())}",
            "materials": [{"type": "standard", "grade": "basic"}],
            "dimensions": {"length": 10.0, "width": 10.0, "height": 3.0},
            "features": ["basic_functionality"],
            "components": ["main_structure"],
            "fallback_method": "rule_based"
        }
    
    async def _run_yotta(self, prompt: str, context: Optional[str], job_type: str) -> Dict[str, Any]:
        """Run inference on Yotta cloud with RTX-3060 optimization"""
        if not self.yotta_available:
            return await self._run_local(prompt, context, job_type)
        
        # Enhanced payload for Yotta cloud bursting with RTX-3060 compatibility
        payload = {
            "prompt": prompt,
            "context": context,
            "job_type": job_type,
            "gpu_preference": "rtx_3060_compatible",
            "memory_limit": "8gb",
            "optimization": "hybrid_burst",
            "temperature": 0.7,
            "max_tokens": 2048,
            "client_id": "bhiv-rtx3060"
        }
        
        headers = {
            "Authorization": f"Bearer {self.yotta_key}",
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.yotta_url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()
                print(f"[YOTTA] RTX-3060 compatible inference completed")
                return result
                
        except Exception as e:
            print(f"[YOTTA] Cloud failed: {e}, using local fallback")
            return self._rule_based_fallback(prompt, context, job_type)
    
    def _estimate_cost(self, prompt: str, compute_type: str) -> float:
        """Estimate cost for inference"""
        token_count = len(prompt.split()) * 1.3  # Rough token estimation
        
        if "local" in compute_type or compute_type == "rule_based":
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
                "cost_savings": self.job_stats["remote_cost"] - self.job_stats["local_cost"] if self.job_stats["local_jobs"] > 0 else 0,
                "burst_efficiency": (self.job_stats["remote_jobs"] / max(self.job_stats["total_jobs"], 1)) * 100,
                "hybrid_optimization": "optimal" if self.local_gpu and self.yotta_available else "limited"
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

# Global instance with enhanced logging
router = ComputeRouter()
compute_router = router

if os.getenv("PRODUCTION_MODE") != "true":
    print(f"[INIT] Compute router ready - Strategy: {router.compute_strategy}")
    print(f"[INIT] Available compute: Local GPU: {router.local_gpu}, Yotta Cloud: {router.yotta_available}")