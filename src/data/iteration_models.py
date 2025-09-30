"""Additional models for RL iteration tracking"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from .models import Base
from sqlalchemy.sql import func
import uuid

class IterationLog(Base):
    __tablename__ = 'iteration_logs'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, nullable=False)  # Groups iterations together
    iteration_number = Column(Integer, nullable=False)
    prompt = Column(Text, nullable=False)

    # Before and after specs
    spec_before = Column(JSON, nullable=True)
    spec_after = Column(JSON, nullable=False)

    # Evaluation and feedback
    evaluation_data = Column(JSON, nullable=False)
    feedback_data = Column(JSON, nullable=False)

    # Scores and rewards
    score_before = Column(Float, nullable=True)
    score_after = Column(Float, nullable=False)
    reward = Column(Float, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
