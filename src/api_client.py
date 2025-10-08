"""API Client for backend integration"""

import requests
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = "bhiv-secret-key-2024", token: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.token = token
        self.session = requests.Session()
        
        # Set headers
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })
        
        if self.token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login and get JWT token"""
        response = self.session.post(f"{self.base_url}/api/v1/auth/login", data={
            "username": username,
            "password": password
        })
        response.raise_for_status()
        
        data = response.json()
        self.token = data["access_token"]
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })
        return data
    
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate specification"""
        payload = {"prompt": prompt}
        if context:
            payload["context"] = context
            
        response = self.session.post(f"{self.base_url}/api/v1/generate", json=payload)
        response.raise_for_status()
        return response.json()
    
    def switch(self, spec_id: str, target: Dict[str, str], update: Dict[str, Any], note: str = None) -> Dict[str, Any]:
        """Switch object material"""
        payload = {
            "spec_id": spec_id,
            "target": target,
            "update": update
        }
        if note:
            payload["note"] = note
            
        response = self.session.post(f"{self.base_url}/api/v1/switch", json=payload)
        response.raise_for_status()
        return response.json()
    
    def compliance_run_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run compliance case"""
        response = self.session.post(f"{self.base_url}/api/v1/compliance/run_case", json=case_data)
        response.raise_for_status()
        return response.json()
    
    def get_report(self, spec_id: str) -> Dict[str, Any]:
        """Get evaluation report"""
        response = self.session.get(f"{self.base_url}/reports/{spec_id}")
        response.raise_for_status()
        return response.json()
    
    def core_run(self, prompt: str, iterations: int = 3, compliance_check: bool = False) -> Dict[str, Any]:
        """Run core pipeline"""
        payload = {
            "prompt": prompt,
            "iterations": iterations,
            "compliance_check": compliance_check
        }
        
        response = self.session.post(f"{self.base_url}/api/v1/core/run", json=payload)
        response.raise_for_status()
        return response.json()