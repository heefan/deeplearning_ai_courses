"""
FastAPI service for the weather bot.
"""

from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ..adk_integration.session import WeatherSession

# Request/Response models
class WeatherRequest(BaseModel):
    message: str
    location: Optional[str] = None

class WeatherResponse(BaseModel):
    type: str
    message: str
    data: Optional[Dict[str, Any]] = None
    location: Optional[str] = None

class LocationRequest(BaseModel):
    location: str

class SessionInfo(BaseModel):
    session_id: int
    current_location: Optional[str]
    conversation_count: int
    tools_available: int
    callbacks_available: int

def create_fastapi_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="Weather Bot API",
        description="A unified weather bot supporting both ADK CLI and custom Python services",
        version="0.1.0"
    )
    
    # Global session (in production, use proper session management)
    weather_session = WeatherSession()
    
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "Weather Bot API",
            "version": "0.1.0",
            "endpoints": [
                "/weather - Get weather information",
                "/location - Set location",
                "/session - Get session info",
                "/docs - API documentation"
            ]
        }
    
    @app.post("/weather", response_model=WeatherResponse)
    async def get_weather(request: WeatherRequest):
        """Get weather information based on user message."""
        try:
            response = weather_session.process_message(
                message=request.message,
                location=request.location
            )
            return WeatherResponse(**response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/location")
    async def set_location(request: LocationRequest):
        """Set the current location for the session."""
        try:
            response = weather_session.set_location(request.location)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/session", response_model=SessionInfo)
    async def get_session_info():
        """Get current session information."""
        try:
            info = weather_session.get_session_info()
            return SessionInfo(**info)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/session/start")
    async def start_session(location: Optional[str] = None):
        """Start a new weather session."""
        try:
            response = weather_session.start_session(location)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "weather-bot",
            "version": "0.1.0"
        }
    
    return app

# For direct usage
app = create_fastapi_app()
