"""
Tests for weather services.
"""

import pytest
from src.weather_bot.services.fastapi_app import create_fastapi_app
from src.weather_bot.services.flask_app import create_flask_app
from src.weather_bot.adk_integration.session import WeatherSession

def test_fastapi_app_creation():
    """Test FastAPI app creation."""
    app = create_fastapi_app()
    
    assert app is not None
    assert hasattr(app, 'routes')
    
    # Check that expected routes exist
    routes = [route.path for route in app.routes]
    assert "/" in routes
    assert "/weather" in routes
    assert "/health" in routes

def test_flask_app_creation():
    """Test Flask app creation."""
    app = create_flask_app()
    
    assert app is not None
    assert hasattr(app, 'routes')
    
    # Check that expected routes exist
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    assert "/" in routes
    assert "/weather" in routes
    assert "/health" in routes

def test_weather_session_initialization():
    """Test WeatherSession initialization."""
    session = WeatherSession()
    
    assert session is not None
    assert hasattr(session, 'agent')
    assert hasattr(session, 'conversation_history')
    assert hasattr(session, 'current_location')

def test_session_start():
    """Test session start functionality."""
    session = WeatherSession()
    response = session.start_session("London")
    
    assert isinstance(response, dict)
    assert "session_id" in response
    assert "status" in response
    assert response["status"] == "started"
    assert response["current_location"] == "London"

def test_session_message_processing():
    """Test session message processing."""
    session = WeatherSession()
    session.start_session("Tokyo")
    
    response = session.process_message("What's the weather like?")
    
    assert isinstance(response, dict)
    assert "type" in response
    assert "message" in response

def test_session_location_setting():
    """Test session location setting."""
    session = WeatherSession()
    response = session.set_location("Paris")
    
    assert isinstance(response, dict)
    assert "type" in response
    assert response["type"] == "location_set"
    assert response["location"] == "Paris"

def test_session_info():
    """Test session info retrieval."""
    session = WeatherSession()
    info = session.get_session_info()
    
    assert isinstance(info, dict)
    assert "session_id" in info
    assert "current_location" in info
    assert "conversation_count" in info
    assert "tools_available" in info
    assert "callbacks_available" in info
