"""
Tests for weather tools.
"""

import pytest
from src.weather_bot.core.tools import WeatherTools, get_weather_tools

def test_weather_tools_initialization():
    """Test WeatherTools initialization."""
    tools = WeatherTools()
    assert tools is not None
    assert hasattr(tools, 'api_key')
    assert hasattr(tools, 'base_url')

def test_get_current_weather_mock():
    """Test get_current_weather with mock data (no API key)."""
    tools = WeatherTools()
    tools.api_key = None  # Force mock mode
    
    result = tools.get_current_weather("London")
    
    assert isinstance(result, dict)
    assert "error" in result
    assert "mock_data" in result
    
    mock_data = result["mock_data"]
    assert mock_data["location"] == "London"
    assert "temperature" in mock_data
    assert "description" in mock_data
    assert "humidity" in mock_data

def test_get_weather_forecast_mock():
    """Test get_weather_forecast with mock data (no API key)."""
    tools = WeatherTools()
    tools.api_key = None  # Force mock mode
    
    result = tools.get_weather_forecast("Tokyo", 3)
    
    assert isinstance(result, dict)
    assert "error" in result
    assert "mock_data" in result
    
    mock_data = result["mock_data"]
    assert mock_data["location"] == "Tokyo"
    assert "forecast" in mock_data

def test_get_weather_tools():
    """Test get_weather_tools function."""
    tools = get_weather_tools()
    
    assert isinstance(tools, list)
    assert len(tools) >= 2  # Should have at least 2 tools
    
    # Check tool structure
    for tool in tools:
        assert "name" in tool
        assert "description" in tool
        assert "parameters" in tool
        assert "function" in tool

def test_tool_names():
    """Test that expected tool names are present."""
    tools = get_weather_tools()
    tool_names = [tool["name"] for tool in tools]
    
    assert "get_current_weather" in tool_names
    assert "get_weather_forecast" in tool_names
