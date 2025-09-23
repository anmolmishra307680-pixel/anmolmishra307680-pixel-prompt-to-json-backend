"""Database connection and operations for BHIV Bucket"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .models import Base, Spec, Eval, FeedbackLog, HidgLog
from .iteration_models import IterationLog
import json
from typing import Dict, Any, Optional, List
import uuid

# Load environment variables from config directory
from pathlib import Path
config_path = Path(__file__).parent.parent.parent / "config" / ".env"
load_dotenv(config_path)

# Initialize Supabase client
try:
    from supabase import create_client, Client
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    if url and key:
        supabase: Client = create_client(url, key)
        print("[OK] Supabase client initialized")
    else:
        supabase = None
        print("[WARN] Supabase credentials not found, using PostgreSQL only")
except ImportError:
    supabase = None
    print("[WARN] Supabase library not installed, using PostgreSQL only")

class Database:
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        if not self.database_url or self.database_url.strip() == '':
            print("[WARN] No DATABASE_URL found, using SQLite fallback")
            self.database_url = 'sqlite:///prompt_to_json.db'
        elif 'postgresql' in self.database_url:
            print("[INFO] Using Supabase PostgreSQL database")
        else:
            print("[INFO] Using SQLite database")
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.create_tables()

    def create_tables(self):
        """Create all tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
        except Exception as e:
            print(f"Warning: Could not create tables: {e}")

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()

    def save_spec(self, prompt: str, spec_data: Dict[Any, Any], agent_type: str = 'MainAgent') -> str:
        """Save specification to database"""
        try:
            with self.get_session() as session:
                spec = Spec(
                    prompt=prompt,
                    spec_data=spec_data,
                    agent_type=agent_type
                )
                session.add(spec)
                session.commit()
                return spec.id
        except Exception as e:
            print(f"DB save failed, using fallback: {e}")
            return self._fallback_save_spec(prompt, spec_data)

    def save_eval(self, spec_id: str, prompt: str, eval_data: Dict[Any, Any], score: float) -> str:
        """Save evaluation to database"""
        try:
            with self.get_session() as session:
                eval_record = Eval(
                    spec_id=spec_id,
                    prompt=prompt,
                    eval_data=eval_data,
                    score=score
                )
                session.add(eval_record)
                session.commit()
                return eval_record.id
        except Exception as e:
            print(f"DB save failed, using fallback: {e}")
            return self._fallback_save_eval(spec_id, prompt, eval_data, score)

    def save_feedback(self, spec_id: str, iteration: int, feedback_data: Dict[Any, Any], reward: float = None) -> str:
        """Save feedback to database"""
        try:
            with self.get_session() as session:
                feedback = FeedbackLog(
                    spec_id=spec_id,
                    iteration=iteration,
                    feedback_data=feedback_data,
                    reward=reward
                )
                session.add(feedback)
                session.commit()
                print(f"[DB] Feedback saved to Supabase with ID: {feedback.id}")
                return feedback.id
        except Exception as e:
            print(f"[ERROR] DB feedback save failed: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_save_feedback(spec_id, iteration, feedback_data, reward)

    def save_hidg_log(self, date: str, day: str, task: str, values_reflection: Dict[Any, Any],
                      achievements: Dict[Any, Any] = None, technical_notes: Dict[Any, Any] = None) -> str:
        """Save HIDG values log to database"""
        try:
            with self.get_session() as session:
                hidg_log = HidgLog(
                    date=date,
                    day=day,
                    task=task,
                    values_reflection=values_reflection,
                    achievements=achievements,
                    technical_notes=technical_notes
                )
                session.add(hidg_log)
                session.commit()
                return hidg_log.id
        except Exception as e:
            print(f"DB save failed, using fallback: {e}")
            return self._fallback_save_hidg(date, day, task, values_reflection, achievements, technical_notes)

    def get_spec(self, spec_id: str) -> Optional[Dict[Any, Any]]:
        """Get specification by ID"""
        try:
            with self.get_session() as session:
                spec = session.query(Spec).filter(Spec.id == spec_id).first()
                if spec:
                    return {
                        'id': spec.id,
                        'prompt': spec.prompt,
                        'spec_data': spec.spec_data,
                        'agent_type': spec.agent_type,
                        'created_at': spec.created_at.isoformat()
                    }
        except Exception as e:
            print(f"DB query failed: {e}")
        return None

    def get_eval(self, eval_id: str) -> Optional[Dict[Any, Any]]:
        """Get evaluation by ID"""
        try:
            with self.get_session() as session:
                eval_record = session.query(Eval).filter(Eval.id == eval_id).first()
                if eval_record:
                    return {
                        'id': eval_record.id,
                        'spec_id': eval_record.spec_id,
                        'prompt': eval_record.prompt,
                        'eval_data': eval_record.eval_data,
                        'score': eval_record.score,
                        'created_at': eval_record.created_at.isoformat()
                    }
        except Exception as e:
            print(f"DB query failed: {e}")
        return None

    def get_report(self, report_id: str) -> Optional[Dict[Any, Any]]:
        """Get full report (spec + eval) by ID"""
        try:
            with self.get_session() as session:
                eval_record = session.query(Eval).filter(Eval.id == report_id).first()
                if eval_record:
                    spec = session.query(Spec).filter(Spec.id == eval_record.spec_id).first()
                    return {
                        'report_id': report_id,
                        'spec': {
                            'id': spec.id,
                            'prompt': spec.prompt,
                            'spec_data': spec.spec_data,
                            'created_at': spec.created_at.isoformat()
                        } if spec else None,
                        'evaluation': {
                            'id': eval_record.id,
                            'eval_data': eval_record.eval_data,
                            'score': eval_record.score,
                            'created_at': eval_record.created_at.isoformat()
                        }
                    }
        except Exception as e:
            print(f"DB query failed: {e}")
        return None

    def _fallback_save_spec(self, prompt: str, spec_data: Dict[Any, Any]) -> str:
        """Fallback to file storage"""
        import uuid
        from pathlib import Path
        from datetime import datetime

        spec_id = str(uuid.uuid4())
        Path("spec_outputs").mkdir(exist_ok=True)

        with open(f"spec_outputs/spec_{spec_id}.json", 'w') as f:
            json.dump({
                'id': spec_id,
                'prompt': prompt,
                'spec_data': spec_data,
                'created_at': datetime.now().isoformat()
            }, f, indent=2)

        return spec_id

    def _fallback_save_eval(self, spec_id: str, prompt: str, eval_data: Dict[Any, Any], score: float) -> str:
        """Fallback to file storage"""
        import uuid
        from pathlib import Path
        from datetime import datetime

        eval_id = str(uuid.uuid4())
        Path("reports").mkdir(exist_ok=True)

        with open(f"reports/eval_{eval_id}.json", 'w') as f:
            json.dump({
                'id': eval_id,
                'spec_id': spec_id,
                'prompt': prompt,
                'eval_data': eval_data,
                'score': score,
                'created_at': datetime.now().isoformat()
            }, f, indent=2)

        return eval_id

    def _fallback_save_feedback(self, spec_id: str, iteration: int, feedback_data: Dict[Any, Any], reward: float) -> str:
        """Fallback to file storage"""
        import uuid
        from pathlib import Path
        from datetime import datetime

        feedback_id = str(uuid.uuid4())
        Path("logs").mkdir(exist_ok=True)

        existing_logs = []
        feedback_file = Path("logs/feedback_log.json")
        if feedback_file.exists():
            with open(feedback_file, 'r') as f:
                existing_logs = json.load(f)

        existing_logs.append({
            'id': feedback_id,
            'spec_id': spec_id,
            'iteration': iteration,
            'feedback_data': feedback_data,
            'reward': reward,
            'created_at': datetime.now().isoformat()
        })

        with open(feedback_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)

        return feedback_id

    def _fallback_save_hidg(self, date: str, day: str, task: str, values_reflection: Dict[Any, Any],
                           achievements: Dict[Any, Any], technical_notes: Dict[Any, Any]) -> str:
        """Fallback to file storage"""
        import uuid
        from pathlib import Path
        from datetime import datetime

        hidg_id = str(uuid.uuid4())
        Path("logs").mkdir(exist_ok=True)

        existing_logs = []
        values_file = Path("logs/values_log.json")
        if values_file.exists():
            with open(values_file, 'r') as f:
                existing_logs = json.load(f)

        existing_logs.append({
            'id': hidg_id,
            'date': date,
            'day': day,
            'task': task,
            'values_reflection': values_reflection,
            'achievements': achievements,
            'technical_notes': technical_notes,
            'created_at': datetime.now().isoformat()
        })

        with open(values_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)

        return hidg_id

    def save_iteration_log(self, session_id: str, iteration_number: int, prompt: str,
                          spec_before: Dict[Any, Any], spec_after: Dict[Any, Any],
                          evaluation_data: Dict[Any, Any], feedback_data: Dict[Any, Any],
                          score_before: float, score_after: float, reward: float) -> str:
        """Save RL iteration log to database"""
        try:
            with self.get_session() as session:
                iteration_log = IterationLog(
                    session_id=session_id,
                    iteration_number=iteration_number,
                    prompt=prompt,
                    spec_before=spec_before,
                    spec_after=spec_after,
                    evaluation_data=evaluation_data,
                    feedback_data=feedback_data,
                    score_before=score_before,
                    score_after=score_after,
                    reward=reward
                )
                session.add(iteration_log)
                session.commit()
                print(f"[DB] Iteration log saved to Supabase with ID: {iteration_log.id}")
                return iteration_log.id
        except Exception as e:
            print(f"[ERROR] DB iteration save failed: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_save_iteration(session_id, iteration_number, prompt,
                                               spec_before, spec_after, evaluation_data,
                                               feedback_data, score_before, score_after, reward)

    def get_iteration_logs(self, session_id: str) -> List[Dict[Any, Any]]:
        """Get all iteration logs for a session"""
        try:
            with self.get_session() as session:
                logs = session.query(IterationLog).filter(
                    IterationLog.session_id == session_id
                ).order_by(IterationLog.iteration_number).all()

                return [{
                    'id': log.id,
                    'session_id': log.session_id,
                    'iteration_number': log.iteration_number,
                    'prompt': log.prompt,
                    'spec_before': log.spec_before,
                    'spec_after': log.spec_after,
                    'evaluation_data': log.evaluation_data,
                    'feedback_data': log.feedback_data,
                    'score_before': log.score_before,
                    'score_after': log.score_after,
                    'reward': log.reward,
                    'created_at': log.created_at.isoformat()
                } for log in logs]
        except Exception as e:
            print(f"DB query failed: {e}")
            return []

    def _fallback_save_iteration(self, session_id: str, iteration_number: int, prompt: str,
                               spec_before: Dict[Any, Any], spec_after: Dict[Any, Any],
                               evaluation_data: Dict[Any, Any], feedback_data: Dict[Any, Any],
                               score_before: float, score_after: float, reward: float) -> str:
        """Fallback to file storage for iteration logs"""
        from pathlib import Path
        from datetime import datetime

        iteration_id = str(uuid.uuid4())
        Path("logs").mkdir(exist_ok=True)

        existing_logs = []
        iteration_file = Path("logs/iteration_logs.json")
        if iteration_file.exists():
            with open(iteration_file, 'r') as f:
                existing_logs = json.load(f)

        existing_logs.append({
            'id': iteration_id,
            'session_id': session_id,
            'iteration_number': iteration_number,
            'prompt': prompt,
            'spec_before': spec_before,
            'spec_after': spec_after,
            'evaluation_data': evaluation_data,
            'feedback_data': feedback_data,
            'score_before': score_before,
            'score_after': score_after,
            'reward': reward,
            'created_at': datetime.now().isoformat()
        })

        with open(iteration_file, 'w') as f:
            json.dump(existing_logs, f, indent=2)

        return iteration_id

# Global database instance
db = Database()
