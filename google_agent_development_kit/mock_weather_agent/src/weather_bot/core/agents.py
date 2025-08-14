"""
Agent factory for the weather bot.
"""

from typing import Dict, Any, List
from google.adk import Agent
from .config import config
from .tools import get_weather_tools
from .callbacks import safety_callbacks

class WeatherAgent(Agent):
    """Weather agent implementation that inherits from ADK Agent."""
    
    def __init__(self):
        super().__init__(
            name="weather_bot",
            description="A helpful weather assistant that can provide current weather conditions and forecasts for any location.",
            instruction="""You are a helpful weather assistant. You can provide current weather information and forecasts for any location.

Your capabilities include:
- Getting current weather conditions for a specific location
- Providing weather forecasts for up to 5 days
- Converting between different temperature units when needed
- Providing weather-related advice and recommendations

When providing weather information, always include:
- Current temperature (in Celsius)
- Weather description
- Humidity percentage
- Wind speed
- "Feels like" temperature

If the weather API is not available, you can provide mock data for demonstration purposes.

Be friendly, helpful, and provide context about the weather conditions. If temperatures are extreme, provide appropriate warnings or advice.""",
            tools=get_weather_tools(),
            model="gemini-1.5-flash"
        )
        
    def get_system_prompt(self) -> str:
        """Get the system prompt for the weather agent."""
        return self.instruction

    def get_tools(self) -> List[Any]:
        """Get available tools."""
        return self.tools
    
    def get_callbacks(self) -> List[Dict[str, Any]]:
        """Get safety callbacks."""
        return safety_callbacks()

def create_weather_agent() -> WeatherAgent:
    """
    Create and configure a weather agent.
    
    Returns:
        Configured WeatherAgent instance
    """
    agent = WeatherAgent()
    
    # Validate configuration
    if not config.openai_api_key:
        print("Warning: OpenAI API key not configured. Using mock data.")
    
    if not config.weather_api_key:
        print("Warning: Weather API key not configured. Using mock data.")
    
    return agent

# For ADK compatibility, we need to expose these at module level
def get_agent_config() -> Dict[str, Any]:
    """Get agent configuration for ADK."""
    return {
        "model": config.model_name,
        "temperature": config.temperature,
        "system_prompt": create_weather_agent().get_system_prompt(),
        "tools": get_weather_tools(),
        "callbacks": safety_callbacks()
    }
