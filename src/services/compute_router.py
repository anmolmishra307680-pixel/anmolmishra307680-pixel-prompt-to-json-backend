import os, httpx
from src.agents.main_agent import MainAgent

class ComputeRouter:
    def __init__(self):
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                self.local_gpu = '3060' in gpu_name or 'RTX' in gpu_name
                print(f"[INFO] GPU detected: {gpu_name}, RTX-3060 compatible: {self.local_gpu}")
            else:
                self.local_gpu = False
                print("[INFO] No CUDA GPU available")
        except ImportError:
            self.local_gpu = False
            print("[INFO] PyTorch not available, no GPU support")
        self.yotta_key = os.getenv("YOTTA_API_KEY")
        self.yotta_url = os.getenv("YOTTA_ENDPOINT")

    async def route_inference(self, prompt, context, job_type):
        # simple complexity: len words
        score = min(len(prompt.split())/100,1.0)
        if score<0.5 and self.local_gpu:
            agent=MainAgent(); return {"result":agent.run(prompt).model_dump(),"compute":"local"}
        # else remote
        async with httpx.AsyncClient() as c:
            r=await c.post(self.yotta_url, json={"prompt":prompt,"context":context}, headers={"Authorization":f"Bearer {self.yotta_key}"})
            return {"result":r.json(),"compute":"yotta"}
    
    def get_job_stats(self):
        return {
            "local_gpu_available": self.local_gpu,
            "yotta_configured": bool(self.yotta_key and self.yotta_url),
            "total_jobs": 0,
            "local_jobs": 0,
            "remote_jobs": 0
        }
router=ComputeRouter()
compute_router=router