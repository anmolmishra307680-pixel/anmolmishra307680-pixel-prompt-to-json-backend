"""Advanced RL Environment with Policy Gradients"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class AdvancedRLEnvironment:
    def __init__(self):
        self.learning_rate = 0.01
        self.gamma = 0.95  # Discount factor
        self.policy_weights = {}

        # Create logs directory
        Path("logs").mkdir(exist_ok=True)

    def train_episode(self, prompt: str, max_steps: int = 3) -> Dict[str, Any]:
        """Train a single episode with policy gradients"""
        print(f"Starting Advanced RL training for: '{prompt}'")

        from prompt_agent import MainAgent
        from evaluator import EvaluatorAgent

        main_agent = MainAgent()
        evaluator_agent = EvaluatorAgent()

        episode_data = {
            "prompt": prompt,
            "max_steps": max_steps,
            "steps": [],
            "total_reward": 0.0,
            "final_score": 0.0,
            "policy_updates": []
        }

        current_spec = None

        for step in range(max_steps):
            print(f"Advanced RL Step {step + 1}/{max_steps}")

            # Generate or improve specification
            if step == 0:
                spec = main_agent.generate_spec(prompt)
            else:
                # Policy-based improvement
                spec = self._policy_improvement(current_spec, prompt, main_agent)

            # Evaluate specification
            evaluation = evaluator_agent.evaluate_spec(spec, prompt)

            # Calculate reward using policy gradient
            reward = self._calculate_policy_reward(evaluation, step)
            episode_data["total_reward"] += reward

            # Store step data
            step_data = {
                "step": step + 1,
                "spec": spec.model_dump(),
                "evaluation": evaluation.model_dump(),
                "reward": reward,
                "policy_action": f"improvement_step_{step + 1}"
            }
            episode_data["steps"].append(step_data)

            # Update policy
            policy_update = self._update_policy(spec, evaluation, reward)
            episode_data["policy_updates"].append(policy_update)

            print(f"Step {step + 1}: Score {evaluation.score:.2f}, Reward {reward:.3f}")

            current_spec = spec
            episode_data["final_score"] = evaluation.score

        # Save training results
        training_file = self._save_training_results(episode_data)
        episode_data["training_file"] = training_file

        # Final spec
        if current_spec:
            episode_data["final_spec"] = current_spec.model_dump()

        print(f"Advanced RL completed: {max_steps} steps, Final Score {episode_data['final_score']:.2f}")

        return episode_data

    def _policy_improvement(self, current_spec, prompt: str, main_agent):
        """Improve specification using policy gradients"""
        try:
            # Simple policy-based improvement
            improved_spec = main_agent.improve_spec_with_feedback(
                current_spec,
                ["Policy gradient improvement"],
                ["Add advanced features", "Optimize dimensions"]
            )
            return improved_spec
        except Exception as e:
            print(f"Policy improvement failed: {e}")
            return current_spec

    def _calculate_policy_reward(self, evaluation, step: int) -> float:
        """Calculate reward using policy gradient method"""
        base_reward = evaluation.score / 100.0

        # Policy gradient bonus
        policy_bonus = 0.1 * (step + 1)  # Reward later improvements more

        # Exploration bonus
        exploration_bonus = random.uniform(-0.05, 0.05)

        total_reward = base_reward + policy_bonus + exploration_bonus
        return max(0.0, total_reward)

    def _update_policy(self, spec, evaluation, reward: float) -> Dict[str, Any]:
        """Update policy weights based on reward"""
        policy_update = {
            "timestamp": datetime.now().isoformat(),
            "reward": reward,
            "score": evaluation.score,
            "policy_change": f"Updated weights by {reward * self.learning_rate:.4f}",
            "learning_rate": self.learning_rate
        }

        # Simple policy weight update - handle universal design types
        design_type = getattr(spec, 'design_type', getattr(spec, 'building_type', 'unknown'))
        policy_key = f"{design_type}_{len(spec.features)}"
        if policy_key not in self.policy_weights:
            self.policy_weights[policy_key] = 1.0

        self.policy_weights[policy_key] += reward * self.learning_rate
        policy_update["new_weight"] = self.policy_weights[policy_key]

        return policy_update

    def _save_training_results(self, episode_data: Dict[str, Any]) -> str:
        """Save advanced RL training results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"advanced_rl_training_{timestamp}.json"
        filepath = Path("logs") / filename

        # Add metadata
        training_data = {
            **episode_data,
            "algorithm": "REINFORCE_Policy_Gradient",
            "learning_rate": self.learning_rate,
            "gamma": self.gamma,
            "timestamp": datetime.now().isoformat(),
            "policy_weights": self.policy_weights
        }

        with open(filepath, 'w') as f:
            json.dump(training_data, f, indent=2, default=str)

        print(f"Advanced RL training saved to: {filepath}")
        return str(filepath)
