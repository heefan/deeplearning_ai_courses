"""
Weather Agent for ADK
"""

from src.weather_bot.core.agents import create_weather_agent
from src.weather_bot.core.tools import get_weather_tools
from src.weather_bot.core.callbacks import safety_callbacks

# Create the agent instance
root_agent = create_weather_agent()

# Export tools and callbacks for ADK
tools = get_weather_tools()
callbacks = safety_callbacks()
