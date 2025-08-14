"""
Session management for ADK integration.
"""

from typing import Dict, Any, Optional
from ..core.agents import WeatherAgent
from ..core.tools import weather_tools
from ..core.callbacks import apply_safety_checks

class WeatherSession:
    """Session management for weather bot ADK integration."""
    
    def __init__(self):
        self.agent = WeatherAgent()
        self.conversation_history = []
        self.current_location = None
        
    def start_session(self, initial_location: Optional[str] = None) -> Dict[str, Any]:
        """
        Start a new weather session.
        
        Args:
            initial_location: Optional initial location to set
            
        Returns:
            Session initialization response
        """
        if initial_location:
            self.current_location = initial_location
            
        return {
            "session_id": id(self),
            "status": "started",
            "current_location": self.current_location,
            "welcome_message": "Hello! I'm your weather assistant. I can help you get current weather conditions and forecasts for any location. What would you like to know?"
        }
    
    def process_message(self, message: str, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a user message in the session.
        
        Args:
            message: User's message
            location: Optional location override
            
        Returns:
            Response with weather information
        """
        # Add to conversation history
        self.conversation_history.append({
            "user": message,
            "timestamp": "now"  # In real implementation, use actual timestamp
        })
        
        # Determine location to use
        target_location = location or self.current_location or "London"
        
        # Process the message and determine what weather info to fetch
        response = self._generate_response(message, target_location)
        
        # Add response to history
        self.conversation_history.append({
            "assistant": response,
            "timestamp": "now"
        })
        
        return response
    
    def _generate_response(self, message: str, location: str) -> Dict[str, Any]:
        """
        Generate a response based on the user message.
        
        Args:
            message: User's message
            location: Location to get weather for
            
        Returns:
            Response dictionary
        """
        message_lower = message.lower()
        
        # Check if user is asking for current weather
        if any(word in message_lower for word in ["current", "now", "today", "weather"]):
            weather_data = weather_tools.get_current_weather(location)
            weather_data = apply_safety_checks(weather_data)
            
            if "error" in weather_data:
                return {
                    "type": "weather_current",
                    "location": location,
                    "data": weather_data,
                    "message": f"I'm showing you the current weather for {location}. Note: Using mock data as the weather API is not configured."
                }
            else:
                return {
                    "type": "weather_current",
                    "location": location,
                    "data": weather_data,
                    "message": f"Here's the current weather for {location}: {weather_data['temperature']}°C, {weather_data['description']} with {weather_data['humidity']}% humidity."
                }
        
        # Check if user is asking for forecast
        elif any(word in message_lower for word in ["forecast", "tomorrow", "week", "future"]):
            days = 5  # Default to 5 days
            if "tomorrow" in message_lower:
                days = 1
            elif "week" in message_lower:
                days = 7
                
            forecast_data = weather_tools.get_weather_forecast(location, days)
            forecast_data = apply_safety_checks(forecast_data)
            
            if "error" in forecast_data:
                return {
                    "type": "weather_forecast",
                    "location": location,
                    "data": forecast_data,
                    "message": f"I'm showing you the {days}-day forecast for {location}. Note: Using mock data as the weather API is not configured."
                }
            else:
                return {
                    "type": "weather_forecast",
                    "location": location,
                    "data": forecast_data,
                    "message": f"Here's the {days}-day forecast for {location}."
                }
        
        # Default response
        else:
            return {
                "type": "general",
                "message": f"I can help you with weather information for {location}. Try asking for 'current weather' or 'weather forecast'."
            }
    
    def set_location(self, location: str) -> Dict[str, Any]:
        """
        Set the current location for the session.
        
        Args:
            location: New location
            
        Returns:
            Confirmation response
        """
        self.current_location = location
        return {
            "type": "location_set",
            "location": location,
            "message": f"Location set to {location}. You can now ask me about the weather there!"
        }
    
    def get_session_info(self) -> Dict[str, Any]:
        """
        Get current session information.
        
        Returns:
            Session information
        """
        return {
            "session_id": id(self),
            "current_location": self.current_location,
            "conversation_count": len(self.conversation_history),
            "tools_available": len(self.agent.get_tools()),
            "callbacks_available": len(self.agent.get_callbacks())
        }
