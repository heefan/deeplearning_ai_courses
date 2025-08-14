#!/usr/bin/env python3
"""
FastAPI server runner for the weather bot.
"""

import uvicorn
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.weather_bot.services.fastapi_app import app

def main():
    """Run the FastAPI server."""
    print("🚀 Starting Weather Bot FastAPI Server")
    print("=" * 50)
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🌐 Root Endpoint: http://localhost:8000/")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
