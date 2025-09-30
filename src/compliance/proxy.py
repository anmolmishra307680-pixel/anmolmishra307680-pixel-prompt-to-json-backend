"""Compliance proxy for Soham's endpoints"""

import httpx
import os
from typing import Dict, Any

class ComplianceProxy:
    def __init__(self):
        self.base_url = os.getenv("SOHAM_COMPLIANCE_URL", "http://localhost:8001")
        self.timeout = 30.0
    
    async def run_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Proxy to Soham's /run_case endpoint"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/run_case",
                json=case_data
            )
            response.raise_for_status()
            return response.json()
    
    async def send_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Proxy to Soham's /feedback endpoint"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/feedback", 
                json=feedback_data
            )
            response.raise_for_status()
            return response.json()

# Global instance
compliance_proxy = ComplianceProxy()