"""SQLAlchemy models for BHIV Bucket"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Spec(Base):
    __tablename__ = 'specs'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt = Column(Text, nullable=False)
    spec_data = Column(JSON, nullable=False)
    agent_type = Column(String, default='MainAgent')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Eval(Base):
    __tablename__ = 'evals'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    spec_id = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    eval_data = Column(JSON, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class FeedbackLog(Base):
    __tablename__ = 'feedback_logs'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    spec_id = Column(String, nullable=False)
    iteration = Column(Integer, nullable=False)
    feedback_data = Column(JSON, nullable=False)
    reward = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class HidgLog(Base):
    __tablename__ = 'hidg_logs'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(String, nullable=False)
    day = Column(String, nullable=False)
    task = Column(String, nullable=False)
    values_reflection = Column(JSON, nullable=False)
    achievements = Column(JSON, nullable=True)
    technical_notes = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
