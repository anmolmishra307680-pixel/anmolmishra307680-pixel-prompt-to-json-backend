"""Prompt Agent Module - Legacy compatibility"""

from .extractor import PromptExtractor
from .universal_extractor import UniversalPromptExtractor

# MainAgent moved to src.agents.main_agent - use direct import to avoid circular dependency
def __getattr__(name):
    if name == 'MainAgent':
        from ..agents.main_agent import MainAgent
        return MainAgent
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ['PromptExtractor', 'UniversalPromptExtractor', 'MainAgent']