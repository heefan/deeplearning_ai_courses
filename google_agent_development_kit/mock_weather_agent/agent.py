"""
ADK CLI entry point for the weather bot.
This file enables the weather bot to work with `uv run adk web`.
"""

from src.weather_bot.core.agents import create_weather_agent
from src.weather_bot.core.tools import get_weather_tools
from src.weather_bot.core.callbacks import safety_callbacks

# ADK expects these to be available at module level
root_agent = create_weather_agent()
tools = get_weather_tools()
callbacks = safety_callbacks()

if __name__ == "__main__":
    print("Weather Bot ADK Agent initialized")
    print("Use 'uv run adk web' to start the web interface")
