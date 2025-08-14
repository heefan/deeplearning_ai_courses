"""
Flask service for the weather bot.
"""

from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from ..adk_integration.session import WeatherSession

def create_flask_app() -> Flask:
    """Create and configure the Flask application."""
    
    app = Flask(__name__)
    
    # Global session (in production, use proper session management)
    weather_session = WeatherSession()
    
    @app.route("/", methods=["GET"])
    def root():
        """Root endpoint with API information."""
        return jsonify({
            "message": "Weather Bot API",
            "version": "0.1.0",
            "endpoints": [
                "/weather - Get weather information",
                "/location - Set location", 
                "/session - Get session info"
            ]
        })
    
    @app.route("/weather", methods=["POST"])
    def get_weather():
        """Get weather information based on user message."""
        try:
            data = request.get_json()
            if not data or "message" not in data:
                return jsonify({"error": "Message is required"}), 400
            
            response = weather_session.process_message(
                message=data["message"],
                location=data.get("location")
            )
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/location", methods=["POST"])
    def set_location():
        """Set the current location for the session."""
        try:
            data = request.get_json()
            if not data or "location" not in data:
                return jsonify({"error": "Location is required"}), 400
            
            response = weather_session.set_location(data["location"])
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/session", methods=["GET"])
    def get_session_info():
        """Get current session information."""
        try:
            info = weather_session.get_session_info()
            return jsonify(info)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/session/start", methods=["POST"])
    def start_session():
        """Start a new weather session."""
        try:
            data = request.get_json() or {}
            location = data.get("location")
            
            response = weather_session.start_session(location)
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "weather-bot",
            "version": "0.1.0"
        })
    
    return app

# For direct usage
app = create_flask_app()
