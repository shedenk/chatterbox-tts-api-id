#!/usr/bin/env python3
"""
Chatterbox TTS API Entry Point

This is the main entry point for the application.
It imports the FastAPI app from the organized app package.
"""

import uvicorn
import warnings
from app.main import app
from app.config import Config

# Silence redundant audio loading warnings
warnings.filterwarnings("ignore", category=UserWarning, module="chatterbox.tts")
warnings.filterwarnings("ignore", category=FutureWarning, module="librosa.core.audio")


def main():
    """Main entry point"""
    try:
        Config.validate()
        print(f"Starting Chatterbox TTS API server...")
        print(f"Server will run on http://{Config.HOST}:{Config.PORT}")
        print(f"API documentation available at http://{Config.HOST}:{Config.PORT}/docs")
        
        uvicorn.run(
            "app.main:app",
            host=Config.HOST,
            port=Config.PORT,
            reload=False,
            access_log=True,
            timeout_keep_alive=600,      # 10 minutes
            limit_concurrency=50,        # Reduce concurrency to save CPU for each job
            backlog=2048                 # Higher request backlog
        )
    except Exception as e:
        import traceback
        print(f"CRITICAL: Failed to start server: {e}")
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main() 