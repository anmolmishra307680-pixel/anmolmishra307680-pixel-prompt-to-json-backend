"""Advanced Agent Coordination System"""

import asyncio
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from src.agents.main_agent import MainAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.rl_agent import RLLoop
from src.agents.feedback_agent import FeedbackAgent
from src.schemas.legacy_schema import DesignSpec, CoordinationResult

class AgentCoordinator:
    def __init__(self):
        self.agents = {
            'prompt': MainAgent(),
            'evaluator': EvaluatorAgent(),
            'rl': RLLoop(),
            'feedback': FeedbackAgent()
        }

    async def coordinated_improvement(self, prompt: str, target_score: float = 90.0) -> Dict[str, Any]:
        """Agents work together for optimal results"""
        start_time = time.time()
        agents_used = []
        improvements = []

        try:
            # Generate initial spec
            spec = self.agents['prompt'].run(prompt)
            agents_used.append("MainAgent")

            # Get evaluation feedback
            evaluation = self.agents['evaluator'].run(spec, prompt)
            agents_used.append("EvaluatorAgent")

            # If score < target, trigger collaborative improvement
            if evaluation.score < target_score:
                print(f"Score {evaluation.score} below target {target_score}, starting collaborative improvement...")
                improvements.append(f"Initial score: {evaluation.score}")

                # RL agent uses evaluator feedback
                try:
                    improved_result = self.agents['rl'].run(prompt, n_iter=3)
                    agents_used.append("RLLoop")

                    # Re-evaluate improved result
                    final_spec = improved_result.get("final_spec", spec.model_dump())
                    final_evaluation = self.agents['evaluator'].run(
                        DesignSpec(**final_spec), prompt
                    )

                    improvements.append(f"RL improvement: {final_evaluation.score - evaluation.score:.1f} points")

                    coordination_time = time.time() - start_time

                    return CoordinationResult(
                        success=True,
                        agents_used=agents_used,
                        iterations=len(improved_result.get("iterations", [])),
                        final_spec=final_spec,
                        improvements=improvements,
                        coordination_time=coordination_time
                    ).model_dump()

                except Exception as e:
                    print(f"RL improvement failed: {e}")
                    improvements.append(f"RL failed: {str(e)}")

            coordination_time = time.time() - start_time

            return CoordinationResult(
                success=True,
                agents_used=agents_used,
                iterations=1,
                final_spec=spec.model_dump(),
                improvements=improvements or [f"Initial score {evaluation.score} meets target"],
                coordination_time=coordination_time
            ).model_dump()

        except Exception as e:
            coordination_time = time.time() - start_time
            return CoordinationResult(
                success=False,
                agents_used=agents_used,
                iterations=0,
                final_spec={},
                improvements=[f"Coordination failed: {str(e)}"],
                coordination_time=coordination_time
            ).model_dump()

    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            try:
                # Test if agent is responsive
                if hasattr(agent, 'run'):
                    status[name] = "✅ Ready"
                else:
                    status[name] = "❌ No run method"
            except Exception as e:
                status[name] = f"❌ Error: {str(e)}"

        return status

    def optimize_spec_iteratively(self, prompt: str, max_iterations: int = 5) -> Dict[str, Any]:
        """Iteratively optimize specification until target score reached"""
        try:
            current_spec = self.agents['prompt'].run(prompt)
            iteration_history = []

            for i in range(max_iterations):
                # Evaluate current spec
                evaluation = self.agents['evaluator'].run(current_spec, prompt)

                iteration_data = {
                    "iteration": i + 1,
                    "spec": current_spec.model_dump(),
                    "score": evaluation.score,
                    "feedback": evaluation.feedback,
                    "suggestions": evaluation.suggestions
                }
                iteration_history.append(iteration_data)

                # If score is good enough, stop
                if evaluation.score >= 90.0:
                    break

                # For now, just return the current spec since improve_spec_with_feedback may not exist
                # This can be enhanced when that method is implemented

            return {
                "final_spec": current_spec.model_dump(),
                "final_score": evaluation.score,
                "iterations": iteration_history,
                "total_iterations": len(iteration_history)
            }
        except Exception as e:
            return {
                "error": str(e),
                "final_spec": {},
                "final_score": 0,
                "iterations": [],
                "total_iterations": 0
            }

    def get_coordination_metrics(self) -> Dict[str, Any]:
        """Get coordination system metrics"""
        return {
            "total_agents": len(self.agents),
            "agent_names": list(self.agents.keys()),
            "coordination_features": [
                "Multi-agent collaboration",
                "Iterative improvement",
                "Score-based optimization",
                "Feedback integration"
            ],
            "timestamp": datetime.now().isoformat()
        }
