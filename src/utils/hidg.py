# hidg.py
from datetime import datetime, timezone
import os
from pathlib import Path

def append_hidg_entry(stage: str, note: str, branch: str = None, commit_hash: str = None):
    """Append HIDG daily log entry after pipeline runs"""

    # Get git info from environment or defaults
    branch = branch or os.getenv('GIT_BRANCH', 'main')
    commit_hash = commit_hash or os.getenv('GIT_COMMIT', 'local')

    # Ensure reports directory exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Create log entry
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = f"{timestamp} - {stage} - {note} - branch:{branch} commit:{commit_hash}\n"

    # Append to daily log
    log_path = reports_dir / "daily_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"[HIDG] Logged: {stage} - {note}")

def log_pipeline_completion(prompt: str, iterations: int, final_score: float = None):
    """Log completion of RL training pipeline"""
    score_text = f"score:{final_score:.2f}" if final_score else "completed"
    note = f"RL pipeline {iterations} iterations for '{prompt[:30]}...' {score_text}"
    append_hidg_entry("RL_TRAINING", note)

def log_generation_completion(prompt: str, success: bool = True):
    """Log completion of specification generation"""
    status = "success" if success else "failed"
    note = f"Spec generation for '{prompt[:30]}...' {status}"
    append_hidg_entry("GENERATION", note)

def log_evaluation_completion(prompt: str, score: float = None):
    """Log completion of specification evaluation"""
    score_text = f"score:{score:.2f}" if score else "completed"
    note = f"Spec evaluation for '{prompt[:30]}...' {score_text}"
    append_hidg_entry("EVALUATION", note)
