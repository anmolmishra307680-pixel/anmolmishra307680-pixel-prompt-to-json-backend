"""RL Agent Module - Legacy compatibility"""

# RLLoop moved to src.agents.rl_agent - use lazy loading
def __getattr__(name):
    if name == 'RLLoop':
        from ..agents.rl_agent import RLLoop
        return RLLoop
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ['RLLoop']