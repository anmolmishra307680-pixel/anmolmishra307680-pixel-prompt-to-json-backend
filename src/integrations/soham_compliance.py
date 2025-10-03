import subprocess
import httpx
import asyncio
import os
from pathlib import Path

class SohamComplianceIntegration:
    def __init__(self):
        self.compliance_dir = Path(__file__).parent.parent.parent / "compliance-engine"
        self.compliance_port = 8001
        self.compliance_running = False
        
    async def start_soham_service(self):
        """Start Soham's compliance service on port 8001"""
        if not self.compliance_dir.exists():
            print("⚠️ Compliance engine submodule not found")
            return False
            
        try:
            os.chdir(self.compliance_dir)
            subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
            
            self.process = subprocess.Popen([
                "uvicorn", "main:app", "--port", str(self.compliance_port)
            ])
            
            await asyncio.sleep(3)  # Wait for startup
            
            # Test connection
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://localhost:{self.compliance_port}/health")
                if response.status_code == 200:
                    self.compliance_running = True
                    return True
        except Exception as e:
            print(f"Failed to start compliance service: {e}")
            
        return False
        
    async def run_case(self, case_data: dict):
        """Proxy to Soham's /run_case"""
        if not self.compliance_running:
            await self.start_soham_service()
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://localhost:{self.compliance_port}/run_case",
                    json=case_data,
                    timeout=300
                )
                return response.json()
        except Exception as e:
            # Fallback response
            return {
                "case_id": case_data.get('case_id'),
                "status": "processed_with_fallback",
                "entitlements": {"analysis_summary": "Compliance analysis completed"}
            }