"""
Safety callbacks for ADK CLI integration.
This file provides the callbacks interface for `uv run adk web`.
"""

from src.weather_bot.core.callbacks import safety_callbacks

# Export callbacks for ADK
callbacks = safety_callbacks()
