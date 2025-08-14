"""
Tool implementations for ADK CLI integration.
This file provides the tools interface for `uv run adk web`.
"""

from src.weather_bot.core.tools import get_weather_tools

# Export tools for ADK
tools = get_weather_tools()
