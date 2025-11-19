# run.py - Backend Startup Script

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("DEBUG", "true").lower() == "true"
    
    print("=" * 60)
    print("🌾 FarmaSathi Backend Server")
    print("=" * 60)
    print(f"📡 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"📖 ReDoc: http://{host}:{port}/redoc")
    print(f"🔄 Auto-reload: {reload}")
    print("=" * 60)
    print("\n✅ Starting server...\n")
    
    # Run uvicorn server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
        access_log=True
    )
