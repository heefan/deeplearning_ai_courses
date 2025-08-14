"""
Weather tools for the agent.
"""

import json
import requests
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from google.adk.tools import FunctionTool
from .config import config

class WeatherInfo(BaseModel):
    """Weather information model."""
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    feels_like: float

class WeatherTools:
    """Weather-related tools for the agent."""
    
    def __init__(self):
        self.api_key = config.weather_api_key
        self.base_url = config.weather_api_url
        
    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """
        Get current weather for a specific location.
        
        Args:
            location: City name or coordinates (e.g., "London" or "51.5074,-0.1278")
            
        Returns:
            Dictionary containing weather information
        """
        if not self.api_key:
            return {
                "error": "Weather API key not configured",
                "mock_data": {
                    "location": location,
                    "temperature": 22.5,
                    "description": "Partly cloudy",
                    "humidity": 65,
                    "wind_speed": 12.3,
                    "feels_like": 24.1
                }
            }
        
        try:
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather_info = {
                "location": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "feels_like": data["main"]["feels_like"]
            }
            
            return weather_info
            
        except requests.RequestException as e:
            return {
                "error": f"Failed to fetch weather data: {str(e)}",
                "mock_data": {
                    "location": location,
                    "temperature": 22.5,
                    "description": "Partly cloudy",
                    "humidity": 65,
                    "wind_speed": 12.3,
                    "feels_like": 24.1
                }
            }
    
    def get_weather_forecast(self, location: str, days: int = 5) -> Dict[str, Any]:
        """
        Get weather forecast for a location.
        
        Args:
            location: City name or coordinates
            days: Number of days for forecast (1-5)
            
        Returns:
            Dictionary containing forecast information
        """
        if not self.api_key:
            return {
                "error": "Weather API key not configured",
                "mock_data": {
                    "location": location,
                    "forecast": [
                        {"day": "Today", "temp": 22.5, "description": "Sunny"},
                        {"day": "Tomorrow", "temp": 20.1, "description": "Cloudy"},
                        {"day": "Day 3", "temp": 18.7, "description": "Rainy"},
                    ]
                }
            }
        
        try:
            # Using 5-day forecast endpoint
            forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(forecast_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process forecast data (simplified)
            forecast = []
            for item in data["list"][:days]:
                forecast.append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "humidity": item["main"]["humidity"]
                })
            
            return {
                "location": data["city"]["name"],
                "forecast": forecast
            }
            
        except requests.RequestException as e:
            return {
                "error": f"Failed to fetch forecast data: {str(e)}",
                "mock_data": {
                    "location": location,
                    "forecast": [
                        {"day": "Today", "temp": 22.5, "description": "Sunny"},
                        {"day": "Tomorrow", "temp": 20.1, "description": "Cloudy"},
                        {"day": "Day 3", "temp": 18.7, "description": "Rainy"},
                    ]
                }
            }

# Global tools instance
weather_tools = WeatherTools()

def get_weather_tools() -> List[FunctionTool]:
    """Get weather tools for ADK integration."""
    return [
        FunctionTool(weather_tools.get_current_weather),
        FunctionTool(weather_tools.get_weather_forecast)
    ]
