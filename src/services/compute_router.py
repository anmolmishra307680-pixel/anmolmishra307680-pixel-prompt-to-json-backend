import os, httpx
from src.agents.main_agent import MainAgent

class ComputeRouter:
    def __init__(self):
        try:
            import torch
            self.local_gpu = torch.cuda.is_available() and '3060' in torch.cuda.get_device_name(0)
        except ImportError:
            self.local_gpu = False
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
router=ComputeRouter()
compute_router=router