"""LM Adapter Layer for language model integration"""

from typing import Dict, Any
import os
import json

class LMAdapter:
    def __init__(self, model_client=None):
        self.client = model_client
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.use_llm = bool(self.openai_api_key)

    def run(self, prompt: str, params: dict = None) -> dict:
        """Run language model generation with compute routing"""
        if params is None:
            params = {}
        
        # Route computation based on job complexity
        if params.get("heavy_job") or len(prompt) > 500 or params.get("iterations", 0) > 5:
            return self._route_to_yotta(prompt, params)
        elif self.use_llm and self.client:
            return self.client.generate(prompt=prompt, **params)
        elif self.use_llm:
            return self._openai_generate(prompt, params)
        else:
            return self._heuristic_generate(prompt, params)
    
    def _route_to_yotta(self, prompt: str, params: dict) -> dict:
        """Route to Yotta cloud compute"""
        try:
            # Mock Yotta client call
            result = self._yotta_client_run(prompt, params)
            self._log_usage("yotta", 0.05, prompt, params)
            return result
        except Exception as e:
            print(f"Yotta compute failed: {e}")
            self._log_usage("yotta_failed", 0.0, prompt, params)
            return self._heuristic_generate(prompt, params)
    
    def _yotta_client_run(self, prompt: str, params: dict) -> dict:
        """Mock Yotta cloud compute client"""
        import time
        time.sleep(0.1)  # Simulate processing
        
        base_result = self._heuristic_generate(prompt, params)
        base_result["enhanced"] = True
        base_result["compute_provider"] = "yotta"
        base_result["objects"][0]["properties"]["quality"] = "high"
        return base_result
    
    def _log_usage(self, provider: str, cost: float, prompt: str, params: dict):
        """Log compute usage and cost"""
        try:
            from src.data.database import Database
            import uuid
            from datetime import datetime
            
            db = Database()
            usage_data = {
                "job_id": str(uuid.uuid4()),
                "provider": provider,
                "cost": cost,
                "prompt_length": len(prompt),
                "params": params,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save to usage_logs (fallback to file)
            from pathlib import Path
            import json
            
            Path("logs").mkdir(exist_ok=True)
            usage_file = Path("logs/usage_logs.json")
            
            existing_logs = []
            if usage_file.exists():
                with open(usage_file, 'r') as f:
                    existing_logs = json.load(f)
            
            existing_logs.append(usage_data)
            
            with open(usage_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)
                
        except Exception as e:
            print(f"Usage logging failed: {e}")

    def _openai_generate(self, prompt: str, params: dict) -> dict:
        """Generate using OpenAI API"""
        try:
            import openai
            openai.api_key = self.openai_api_key

            system_prompt = """Generate a JSON specification for the requested design. 
            Include objects with id, type, material, and properties."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON from response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback to heuristic if JSON parsing fails
                return self._heuristic_generate(prompt, params)

        except Exception as e:
            print(f"OpenAI generation failed: {e}")
            return self._heuristic_generate(prompt, params)

    def _heuristic_generate(self, prompt: str, params: dict) -> dict:
        """Fallback heuristic generation"""
        prompt_lower = prompt.lower()
        
        # Determine design type
        if any(word in prompt_lower for word in ['building', 'house', 'office', 'structure']):
            design_type = 'building'
        elif any(word in prompt_lower for word in ['car', 'vehicle', 'truck', 'bike']):
            design_type = 'vehicle'
        elif any(word in prompt_lower for word in ['phone', 'computer', 'device', 'electronics']):
            design_type = 'electronics'
        elif any(word in prompt_lower for word in ['chair', 'table', 'furniture', 'desk']):
            design_type = 'furniture'
        else:
            design_type = 'appliance'

        # Log local usage
        self._log_usage("local", 0.01, prompt, params)
        
        return {
            "design_type": design_type,
            "objects": [
                {
                    "id": "obj_001",
                    "type": "main_structure",
                    "material": "steel" if design_type == 'building' else "plastic",
                    "editable": True,
                    "properties": {
                        "width": 10.0,
                        "height": 8.0,
                        "depth": 12.0
                    }
                }
            ],
            "scene": {
                "environment": "indoor",
                "lighting": "natural",
                "scale": 1.0
            }
        }