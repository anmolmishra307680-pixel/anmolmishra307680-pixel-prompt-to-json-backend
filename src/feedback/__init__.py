"""Feedback Module - Legacy compatibility"""

from .feedback_loop import FeedbackLoop

# FeedbackAgent moved to src.agents.feedback_agent - use lazy loading
def __getattr__(name):
    if name == 'FeedbackAgent':
        from ..agents.feedback_agent import FeedbackAgent
        return FeedbackAgent
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ['FeedbackLoop', 'FeedbackAgent']