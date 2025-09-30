"""Prompt Agent Module - Legacy compatibility"""

from .extractor import PromptExtractor
from .universal_extractor import UniversalPromptExtractor
from ..agents.main_agent import MainAgent

__all__ = ['PromptExtractor', 'UniversalPromptExtractor', 'MainAgent']