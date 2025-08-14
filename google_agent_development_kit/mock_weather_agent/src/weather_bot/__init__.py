"""
Weather Bot - A unified weather agent supporting both ADK CLI and custom Python services.
"""

__version__ = "0.1.0"

from .core.agents import create_weather_agent
from .core.tools import get_weather_tools
from .core.callbacks import safety_callbacks

__all__ = [
    "create_weather_agent",
    "get_weather_tools", 
    "safety_callbacks",
]