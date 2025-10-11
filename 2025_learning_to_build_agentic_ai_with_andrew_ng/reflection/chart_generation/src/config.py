"""
Configuration module for the chart generation agent.

This module handles configuration for LMStudio, ADK, and application settings.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

from google.adk.models import ModelConfig

# Load environment variables
load_dotenv()


@dataclass
class LMStudioConfig:
    """Configuration for LMStudio integration."""
    base_url: str
    model: str
    api_key: Optional[str] = None
    timeout: int = 30


@dataclass
class ADKConfig:
    """Configuration for Google ADK."""
    project_id: str
    location: str = "us-central1"


@dataclass
class AppConfig:
    """Application configuration."""
    max_reflection_iterations: int = 3
    code_execution_timeout: int = 30
    chart_output_dir: str = "./outputs"
    debug: bool = False
    log_level: str = "INFO"


class Config:
    """
    Main configuration class for the chart generation agent.
    
    This class manages all configuration settings from environment variables
    with sensible defaults.
    """
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.lmstudio = LMStudioConfig(
            base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
            model=os.getenv("LMSTUDIO_MODEL", "gpt-oss-20b"),
            api_key=os.getenv("LMSTUDIO_API_KEY"),
            timeout=int(os.getenv("LMSTUDIO_TIMEOUT", "30"))
        )
        
        self.adk = ADKConfig(
            project_id=os.getenv("ADK_PROJECT_ID", ""),
            location=os.getenv("ADK_LOCATION", "us-central1")
        )
        
        self.app = AppConfig(
            max_reflection_iterations=int(os.getenv("MAX_REFLECTION_ITERATIONS", "3")),
            code_execution_timeout=int(os.getenv("CODE_EXECUTION_TIMEOUT", "30")),
            chart_output_dir=os.getenv("CHART_OUTPUT_DIR", "./outputs"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )
    
    def get_model_config(self) -> ModelConfig:
        """
        Get ADK ModelConfig for LMStudio.
        
        Returns:
            ModelConfig configured for LMStudio
        """
        return ModelConfig(
            model_name=self.lmstudio.model,
            endpoint=self.lmstudio.base_url,
            api_key=self.lmstudio.api_key,
            timeout=self.lmstudio.timeout
        )
    
    def validate(self) -> None:
        """
        Validate configuration settings.
        
        Raises:
            ValueError: If required configuration is missing or invalid
        """
        if not self.lmstudio.base_url:
            raise ValueError("LMStudio base URL is required")
        
        if not self.lmstudio.model:
            raise ValueError("LMStudio model is required")
        
        if not self.adk.project_id:
            raise ValueError("ADK project ID is required")
        
        if self.app.max_reflection_iterations < 1:
            raise ValueError("Max reflection iterations must be at least 1")
        
        if self.app.code_execution_timeout < 1:
            raise ValueError("Code execution timeout must be at least 1 second")


# Global configuration instance
config = Config()
