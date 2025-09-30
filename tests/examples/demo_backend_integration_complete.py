#!/usr/bin/env python3
"""
Complete Backend Integration Demo
End-to-end workflow: generate → switch → evaluate → iterate → store → preview
"""

import asyncio
import httpx
import json
from datetime import datetime

class BackendIntegrationDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_key = "bhiv-secret-key-2024"
        self.token = None
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
    
    async def authenticate(self):
        """Get JWT token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/token",
                headers=self.headers,
                json={"username": "admin", "password": "bhiv2024"}
            )
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                self.headers["Authorization"] = f"Bearer {self.token}"
                print("✅ Authentication successful")
            else:
                raise Exception(f"Auth failed: {response.text}")
    
    async def generate_design(self, prompt):
        """Step 1: Generate design spec"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json={"prompt": prompt}
            )
            if response.status_code == 200:
                spec = response.json()
                print(f"✅ Generated design: {spec['spec_id']}")
                return spec
            else:
                raise Exception(f"Generation failed: {response.text}")
    
    async def switch_material(self, spec_id, instruction):
        """Step 2: Switch material"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/switch",
                headers=self.headers,
                json={"spec_id": spec_id, "instruction": instruction}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Material switched: {result['changes_made']}")
                return result
            else:
                raise Exception(f"Switch failed: {response.text}")
    
    async def evaluate_design(self, spec_id):
        """Step 3: Evaluate design"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/evaluate",
                headers=self.headers,
                json={"spec_id": spec_id}
            )
            if response.status_code == 200:
                evaluation = response.json()
                print(f"✅ Evaluation complete: Score {evaluation['overall_score']}")
                return evaluation
            else:
                raise Exception(f"Evaluation failed: {response.text}")
    
    async def iterate_design(self, spec_id, iterations=2):
        """Step 4: RL iteration"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/iterate",
                headers=self.headers,
                json={"spec_id": spec_id, "iterations": iterations}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ RL iteration complete: {result['iterations_completed']} iterations")
                return result
            else:
                raise Exception(f"Iteration failed: {response.text}")
    
    async def get_report(self, spec_id):
        """Step 5: Get evaluation report"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/reports/{spec_id}",
                headers=self.headers
            )
            if response.status_code == 200:
                report = response.json()
                print(f"✅ Report retrieved: {len(report)} entries")
                return report
            else:
                print(f"⚠️ Report not found: {response.text}")
                return None
    
    async def run_complete_workflow(self):
        """Run complete end-to-end workflow"""
        print("🚀 Starting Complete Backend Integration Demo")
        print("=" * 60)
        
        try:
            # Step 1: Authenticate
            await self.authenticate()
            
            # Step 2: Generate design
            prompt = "Modern sustainable office building with solar panels and green roof"
            spec = await self.generate_design(prompt)
            spec_id = spec["spec_id"]
            
            # Step 3: Switch material
            switch_result = await self.switch_material(spec_id, "change floor material to marble")
            
            # Step 4: Evaluate
            evaluation = await self.evaluate_design(spec_id)
            
            # Step 5: Iterate with RL
            iteration_result = await self.iterate_design(spec_id, 2)
            
            # Step 6: Get final report
            report = await self.get_report(spec_id)
            
            print("=" * 60)
            print("🎉 Complete workflow successful!")
            print(f"   Spec ID: {spec_id}")
            print(f"   Final Score: {evaluation['overall_score']}")
            print(f"   RL Iterations: {iteration_result['iterations_completed']}")
            
            return {
                "success": True,
                "spec_id": spec_id,
                "final_score": evaluation["overall_score"],
                "workflow_steps": 6
            }
            
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            return {"success": False, "error": str(e)}

async def main():
    demo = BackendIntegrationDemo()
    result = await demo.run_complete_workflow()
    
    if result["success"]:
        print("\n✅ Demo completed successfully!")
    else:
        print(f"\n❌ Demo failed: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())