"""Main entry point for the application"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from config directory
config_path = Path(__file__).parent / "config" / ".env"
load_dotenv(config_path)

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main API
from api.main_api import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    
    if os.getenv("PRODUCTION_MODE") == "true":
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            workers=int(os.getenv("MAX_WORKERS", 4))
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=port, reload=False)