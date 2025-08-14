"""
Configuration management for the weather bot.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class WeatherConfig(BaseModel):
    """Configuration for the weather bot."""
    
    # API Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    weather_api_key: Optional[str] = Field(default=None, description="Weather API key")
    
    # Model Configuration
    model_name: str = Field(default="gemini-1.5-flash", description="LLM model to use")
    temperature: float = Field(default=0.7, description="Model temperature")
    
    # Weather API Configuration
    weather_api_url: str = Field(
        default="https://api.openweathermap.org/data/2.5/weather",
        description="Weather API base URL"
    )
    
    # Safety Configuration
    max_temperature: float = Field(default=50.0, description="Maximum temperature in Celsius")
    min_temperature: float = Field(default=-50.0, description="Minimum temperature in Celsius")
    
    @classmethod
    def from_env(cls) -> "WeatherConfig":
        """Create configuration from environment variables."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            weather_api_key=os.getenv("WEATHER_API_KEY"),
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            weather_api_url=os.getenv("WEATHER_API_URL", "https://api.openweathermap.org/data/2.5/weather"),
            max_temperature=float(os.getenv("MAX_TEMPERATURE", "50.0")),
            min_temperature=float(os.getenv("MIN_TEMPERATURE", "-50.0")),
        )

# Global configuration instance
config = WeatherConfig.from_env()
