#!/usr/bin/env python3
"""
Render deployment entry point
Re-exports the FastAPI app from main.py for compatibility
"""

import sys
import os

# Add src directory to Python path
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import the app from main module
from main import app

__all__ = ['app']