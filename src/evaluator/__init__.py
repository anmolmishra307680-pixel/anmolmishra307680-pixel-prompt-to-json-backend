"""Evaluator Module - Legacy compatibility"""

from .criteria import EvaluationCriteria
from .report import ReportGenerator

# EvaluatorAgent moved to src.agents.evaluator_agent - use lazy loading
def __getattr__(name):
    if name == 'EvaluatorAgent':
        from ..agents.evaluator_agent import EvaluatorAgent
        return EvaluatorAgent
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ['EvaluationCriteria', 'ReportGenerator', 'EvaluatorAgent']