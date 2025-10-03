#!/usr/bin/env python3
"""
Render deployment compatibility layer
Imports the actual FastAPI app from src.main
"""

from src.main import app

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)