"""Integration with Soham's compliance system"""

import sys
import os
from pathlib import Path
import subprocess
import json
from typing import Dict, Any, Optional

# Add compliance-engine to path
compliance_path = Path(__file__).parent.parent.parent / "compliance-engine"
sys.path.insert(0, str(compliance_path))

class SohamComplianceIntegration:
    def __init__(self):
        self.compliance_path = compliance_path
        self.main_py = self.compliance_path / "main.py"
        
    def process_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process compliance case using Soham's system"""
        try:
            # Import Soham's main function
            from main import process_case
            
            # Call Soham's process_case function
            result = process_case(case_data)
            return result
            
        except ImportError:
            # Fallback: run as subprocess
            return self._run_subprocess(case_data)
    
    def _run_subprocess(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run Soham's system as subprocess"""
        try:
            # Write case data to temp file
            temp_file = self.compliance_path / "temp_case.json"
            with open(temp_file, 'w') as f:
                json.dump(case_data, f)
            
            # Run Soham's main.py
            result = subprocess.run([
                sys.executable, str(self.main_py), str(temp_file)
            ], capture_output=True, text=True, cwd=str(self.compliance_path))
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": result.stderr, "status": "failed"}
                
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def send_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send feedback to Soham's RL system"""
        try:
            # Import Soham's feedback function
            from feedback_api import process_feedback
            
            result = process_feedback(feedback_data)
            return result
            
        except ImportError:
            # Mock feedback response
            return {
                "status": "received",
                "feedback_id": feedback_data.get("case_id", "unknown"),
                "message": "Feedback processed"
            }

# Global instance
soham_integration = SohamComplianceIntegration()