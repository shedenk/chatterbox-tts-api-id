#!/usr/bin/env python3
"""
Chatterbox TTS API Entry Point

This is the main entry point for the application.
It imports the FastAPI app from the organized app package.
"""
import sys

# Silence redundant audio loading warnings early
try:
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="chatterbox.tts")
    warnings.filterwarnings("ignore", category=FutureWarning, module="librosa.core.audio")
except ImportError:
    pass

def main():
    """Main entry point"""
    try:
        # Local imports to catch errors during specific module initialization
        print("🔍 Loading application modules...")
        import uvicorn
        from app.main import app
        from app.config import Config
        
        Config.validate()
        
        # User-friendly host message
        display_host = "localhost" if Config.HOST == "0.0.0.0" else Config.HOST
        print(f"🚀 Starting Chatterbox TTS API server...")
        print(f"📡 Server will run on http://{display_host}:{Config.PORT}")
        print(f"📚 API documentation available at http://{display_host}:{Config.PORT}/docs")
        print(f"🔗 Health check available at http://{display_host}:{Config.PORT}/")
        
        # Simplified uvicorn call - use defaults for stability
        uvicorn.run(
            "app.main:app",
            host=Config.HOST,
            port=Config.PORT,
            reload=False,
            access_log=True,
            timeout_keep_alive=300,  # Match nginx proxy_read_timeout (5 minutes)
            timeout_graceful_shutdown=30
        )
    except ImportError as e:
        print(f"\n❌ CRITICAL: Dependency error: {e}")
        print("Ensure all requirements are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ FATAL ERROR during server startup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 