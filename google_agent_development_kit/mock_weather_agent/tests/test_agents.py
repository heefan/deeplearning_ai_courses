"""
Tests for weather agents.
"""

import pytest
from src.weather_bot.core.agents import WeatherAgent, create_weather_agent

def test_weather_agent_initialization():
    """Test WeatherAgent initialization."""
    agent = WeatherAgent()
    
    assert agent is not None
    assert hasattr(agent, 'tools')
    assert hasattr(agent, 'callbacks')
    assert hasattr(agent, 'config')

def test_agent_system_prompt():
    """Test that agent has a system prompt."""
    agent = WeatherAgent()
    prompt = agent.get_system_prompt()
    
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "weather" in prompt.lower()

def test_agent_tools():
    """Test that agent has tools."""
    agent = WeatherAgent()
    tools = agent.get_tools()
    
    assert isinstance(tools, list)
    assert len(tools) >= 2

def test_agent_callbacks():
    """Test that agent has callbacks."""
    agent = WeatherAgent()
    callbacks = agent.get_callbacks()
    
    assert isinstance(callbacks, list)
    assert len(callbacks) >= 1

def test_create_weather_agent():
    """Test create_weather_agent factory function."""
    agent = create_weather_agent()
    
    assert isinstance(agent, WeatherAgent)
    assert agent is not None

@pytest.mark.asyncio
async def test_agent_run():
    """Test agent run method."""
    agent = WeatherAgent()
    response = await agent.run("What's the weather like?")
    
    assert isinstance(response, str)
    assert "weather" in response.lower()
