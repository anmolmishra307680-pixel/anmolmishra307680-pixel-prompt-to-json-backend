import json
from pathlib import Path
from src.schema import DesignSpec

class RLLoop:
    def __init__(self, max_iterations: int = 3, binary_rewards: bool = False):
        from src.prompt_agent import MainAgent
        from src.evaluator import EvaluatorAgent
        from src.feedback import FeedbackLoop

        self.main_agent = MainAgent()
        self.evaluator_agent = EvaluatorAgent()
        self.feedback_loop = FeedbackLoop()
        self.max_iterations = max_iterations
        self.binary_rewards = binary_rewards

        # Create logs directory
        Path("logs").mkdir(exist_ok=True)

    def run(self, prompt: str, n_iter: int = None):
        """BHIV Core Hook: Single entry point for orchestration"""
        iterations = n_iter or self.max_iterations
        self.max_iterations = iterations
        return self.run_training_loop_with_db(prompt)

    def run_training_loop(self, prompt: str) -> dict:
        """Run reinforcement learning training loop"""
        print(f"Starting RL training loop for prompt: '{prompt}'")

        results = {
            "prompt": prompt,
            "iterations": [],
            "final_spec": None,
            "learning_insights": None
        }

        current_spec = None
        previous_score = 0
        evaluation = None

        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")

            # Generate specification
            if iteration == 0:
                # Initial generation
                spec = self.main_agent.generate_spec(prompt)
            else:
                # Improve based on feedback
                try:
                    feedback_suggestions = self.feedback_loop.get_feedback_for_prompt(prompt)
                    spec = self.main_agent.improve_spec_with_feedback(
                        current_spec,
                        evaluation.feedback,
                        evaluation.suggestions + feedback_suggestions
                    )
                except Exception as e:
                    print(f"[INFO] Using current spec due to improvement error: {e}")
                    spec = current_spec

            # Save specification for each iteration
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            spec_filename = f"design_spec_{timestamp}_iter{iteration + 1}.json"
            spec_path = self.main_agent.spec_outputs_dir / spec_filename

            output_data = {
                "prompt": f"{prompt} (RL iteration {iteration + 1})",
                "specification": spec.model_dump(),
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "generator": "MainAgent",
                    "iteration": iteration + 1,
                    "rl_mode": True
                }
            }

            import json
            with open(spec_path, 'w') as f:
                json.dump(output_data, f, indent=2, default=str)

            print(f"Specification saved to: {spec_path}")

            # Evaluate specification
            evaluation = self.evaluator_agent.evaluate_spec(spec, prompt)

            # Calculate reward
            reward = self.feedback_loop.calculate_reward(evaluation, previous_score, self.binary_rewards)

            # Log iteration (always log, use dummy spec for first iteration)
            if current_spec:
                self.feedback_loop.log_iteration(
                    prompt, current_spec, spec, evaluation, reward, iteration + 1
                )
            else:
                # Log first iteration with empty previous spec
                dummy_spec = DesignSpec(building_type="initial", stories=0)
                self.feedback_loop.log_iteration(
                    prompt, dummy_spec, spec, evaluation, reward, iteration + 1
                )

            # Store iteration results with dashboard format
            iteration_result = {
                "iteration": iteration + 1,
                "specification": spec.model_dump(),
                "evaluation": evaluation.model_dump(),
                "reward": reward,
                "improvement": evaluation.score - previous_score if iteration > 0 else 0,
                "spec_file": str(spec_path),
                "dashboard": {
                    "prompt": prompt,
                    "spec_score": evaluation.score,
                    "critic": evaluation.feedback + evaluation.suggestions,
                    "reward": reward
                }
            }
            results["iterations"].append(iteration_result)

            print(f"Score: {evaluation.score:.2f}, Reward: {reward:.3f}")

            # Update for next iteration
            current_spec = spec
            previous_score = evaluation.score

            # Only allow early stopping after minimum iterations and if score is perfect
            if evaluation.score >= 100 and iteration >= (self.max_iterations - 1):
                print("Early stopping: Perfect score achieved")
                break

        # Ensure we have valid results
        if current_spec:
            results["final_spec"] = current_spec.model_dump()
        else:
            results["final_spec"] = None

        try:
            results["learning_insights"] = self.feedback_loop.get_learning_insights()
        except Exception as e:
            print(f"Warning: Failed to get learning insights: {e}")
            results["learning_insights"] = {"error": str(e)}

        # Save training results
        try:
            self._save_training_results(results)
        except Exception as e:
            print(f"Warning: Failed to save training results: {e}")

        return results

    def run_training_loop_with_db(self, prompt: str) -> dict:
        """Run RL training loop with DB iteration logging"""
        print(f"Starting RL training loop for prompt: '{prompt}'")

        from src.db.database import Database
        from src.feedback import FeedbackAgent
        import uuid

        db = Database()
        feedback_agent = FeedbackAgent()
        session_id = str(uuid.uuid4())

        results = {
            "session_id": session_id,
            "prompt": prompt,
            "iterations": [],
            "final_spec": None,
            "learning_insights": None
        }

        current_spec = None
        previous_score = 0
        evaluation = None

        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")

            # Store spec before improvement
            spec_before = current_spec.model_dump() if current_spec else None
            score_before = previous_score

            # Generate or improve specification
            if iteration == 0:
                spec = self.main_agent.generate_spec(prompt)
            else:
                # Get feedback and improve
                feedback_data = feedback_agent.run(current_spec, prompt, evaluation)
                try:
                    spec = self.main_agent.improve_spec_with_feedback(
                        current_spec,
                        evaluation.feedback,
                        feedback_data.get('suggestions', [])
                    )
                except Exception as e:
                    print(f"[INFO] Using current spec due to improvement error: {e}")
                    spec = current_spec

            # Evaluate specification
            evaluation = self.evaluator_agent.evaluate_spec(spec, prompt)

            # Generate feedback
            feedback_data = feedback_agent.run(spec, prompt, evaluation)

            # Calculate reward
            reward = feedback_agent.calculate_reward(evaluation, previous_score, self.binary_rewards)

            # Save to database first, fallback to files if needed
            try:
                iteration_id = db.save_iteration_log(
                    session_id=session_id,
                    iteration_number=iteration + 1,
                    prompt=prompt,
                    spec_before=spec_before,
                    spec_after=spec.model_dump(),
                    evaluation_data=evaluation.model_dump(),
                    feedback_data=feedback_data,
                    score_before=score_before,
                    score_after=evaluation.score,
                    reward=reward
                )
                print(f"Iteration {iteration + 1} saved to database with ID: {iteration_id}")
            except Exception as e:
                print(f"Database save failed: {e}")
                iteration_id = f"fallback_{iteration + 1}"
                self._create_fallback_logs(session_id, iteration + 1, prompt, spec_before,
                                         spec.model_dump(), evaluation.model_dump(),
                                         feedback_data, score_before, evaluation.score, reward)

            # Store iteration results
            iteration_result = {
                "iteration": iteration + 1,
                "iteration_id": iteration_id,
                "spec_before": spec_before,
                "spec_after": spec.model_dump(),
                "evaluation": evaluation.model_dump(),
                "feedback": feedback_data,
                "score_before": score_before,
                "score_after": evaluation.score,
                "reward": reward,
                "improvement": evaluation.score - previous_score if iteration > 0 else 0
            }
            results["iterations"].append(iteration_result)

            print(f"Score: {evaluation.score:.2f}, Reward: {reward:.3f}")

            # Update for next iteration
            current_spec = spec
            previous_score = evaluation.score

        # Finalize results
        if current_spec:
            results["final_spec"] = current_spec.model_dump()

        try:
            results["learning_insights"] = self.feedback_loop.get_learning_insights()
        except Exception as e:
            print(f"Warning: Failed to get learning insights: {e}")
            results["learning_insights"] = {"error": str(e)}

        return results

    def _create_fallback_logs(self, session_id, iteration, prompt, spec_before, spec_after,
                             evaluation_data, feedback_data, score_before, score_after, reward):
        """Create log files when DB fails"""
        from pathlib import Path
        from datetime import datetime
        import json

        Path("logs").mkdir(exist_ok=True)

        # Create iteration log
        iteration_entry = {
            "session_id": session_id,
            "iteration": iteration,
            "prompt": prompt,
            "spec_before": spec_before,
            "spec_after": spec_after,
            "evaluation": evaluation_data,
            "feedback": feedback_data,
            "score_before": score_before,
            "score_after": score_after,
            "reward": reward,
            "timestamp": datetime.now().isoformat()
        }

        # Save to iteration logs
        iteration_file = Path("logs/iteration_logs.json")
        logs = []
        if iteration_file.exists():
            with open(iteration_file, 'r') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []

        logs.append(iteration_entry)
        with open(iteration_file, 'w') as f:
            json.dump(logs, f, indent=2)

        # Save to feedback logs
        feedback_entry = {
            "session_id": session_id,
            "iteration": iteration,
            "prompt": prompt,
            "feedback": feedback_data,
            "timestamp": datetime.now().isoformat()
        }

        feedback_file = Path("logs/feedback_log.json")
        feedback_logs = []
        if feedback_file.exists():
            with open(feedback_file, 'r') as f:
                try:
                    feedback_logs = json.load(f)
                except:
                    feedback_logs = []

        feedback_logs.append(feedback_entry)
        with open(feedback_file, 'w') as f:
            json.dump(feedback_logs, f, indent=2)

        print(f"Fallback logs created for iteration {iteration}")

    def _save_training_results(self, results: dict):
        """Save training results to logs"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Path("logs") / f"rl_training_{timestamp}.json"

        with open(log_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"Training results saved to: {log_file}")

    def run_single_iteration(self, prompt: str) -> dict:
        """Run a single iteration of the loop"""
        # Generate specification
        spec = self.main_agent.generate_spec(prompt)

        # Evaluate specification
        evaluation = self.evaluator_agent.evaluate_spec(spec, prompt)

        # Calculate reward
        reward = self.feedback_loop.calculate_reward(evaluation)

        # Save specification
        spec_path = self.main_agent.save_spec(spec, prompt)

        return {
            "specification": spec,
            "evaluation": evaluation,
            "reward": reward,
            "spec_file": spec_path
        }

    def compare_approaches(self, prompt: str) -> dict:
        """Compare rule-based vs advanced RL approaches"""
        print("Comparing rule-based vs Advanced RL...")

        try:
            # Standard rule-based approach
            standard_result = self.run_single_iteration(prompt)

            # Advanced RL approach
            from src.rl_agent.advanced_rl import AdvancedRLEnvironment
            env = AdvancedRLEnvironment()
            rl_result = env.train_episode(prompt, max_steps=3)

            comparison = {
                "prompt": prompt,
                "rule_based": {
                    "score": standard_result["evaluation"].score,
                    "reward": standard_result["reward"]
                },
                "advanced_rl": {
                    "score": rl_result["final_score"],
                    "reward": rl_result["total_reward"]
                },
                "winner": "rule_based" if standard_result["evaluation"].score > rl_result["final_score"] else "advanced_rl"
            }

            print(f"Rule-based score: {standard_result['evaluation'].score:.2f}")
            print(f"Advanced RL score: {rl_result['final_score']:.2f}")
            print(f"Winner: {comparison['winner']}")

            # Log comparison to feedback log
            try:
                self.feedback_loop.log_comparison(
                    prompt,
                    standard_result["specification"],
                    rl_result["final_spec"],
                    standard_result["evaluation"],
                    rl_result["final_score"]
                )
            except Exception as log_error:
                print(f"Warning: Failed to log comparison: {log_error}")

            return comparison

        except Exception as e:
            print(f"Comparison failed: {e}")
            return {
                "prompt": prompt,
                "rule_based": {"score": 0, "reward": 0},
                "advanced_rl": {"score": 0, "reward": 0},
                "winner": "none",
                "error": str(e)
            }
