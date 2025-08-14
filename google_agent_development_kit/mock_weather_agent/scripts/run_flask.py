#!/usr/bin/env python3
"""
Flask server runner for the weather bot.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.weather_bot.services.flask_app import app

def main():
    """Run the Flask server."""
    print("🚀 Starting Weather Bot Flask Server")
    print("=" * 50)
    print("🌐 Root Endpoint: http://localhost:5000/")
    print("🔍 Health Check: http://localhost:5000/health")
    print("=" * 50)
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

if __name__ == "__main__":
    main()
