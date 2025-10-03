import os, httpx, sys, json, tempfile
sys.path.append('compliance-engine')

class ComplianceProxy:
    def __init__(self):
        self.url=os.getenv("SOHAM_COMPLIANCE_URL")
    async def run_case(self,data):
        try:
            from main import initialize_system, process_case
            vs,llm,ea,env,rl,geo=initialize_system()
            # write temp JSON
            tf=tempfile.NamedTemporaryFile(delete=False,suffix='.json')
            json.dump(data,tf); tf.close()
            res=process_case(tf.name,vs,llm,ea,env,rl,geo)
            os.unlink(tf.name)
            return res
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    async def send_feedback(self,data):
        async with httpx.AsyncClient() as c:
            r=await c.post(f"{self.url}/feedback",json=data)
            return r.json()

proxy=ComplianceProxy()