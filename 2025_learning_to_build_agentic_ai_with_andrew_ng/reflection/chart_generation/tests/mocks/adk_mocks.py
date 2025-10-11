"""
Mock ADK modules for testing without requiring the actual Google ADK package.
"""

import sys
import types
from unittest.mock import Mock, AsyncMock


class MockModelConfig:
    """Mock ModelConfig for testing."""
    def __init__(self, model_name="test-model", endpoint="http://localhost:1234/v1", **kwargs):
        self.model_name = model_name
        self.endpoint = endpoint
        for k, v in kwargs.items():
            setattr(self, k, v)


class MockAgentConfig:
    """Mock AgentConfig for testing."""
    def __init__(self, model_config=None, system_prompt="", structured_output=True, **kwargs):
        self.model_config = model_config
        self.system_prompt = system_prompt
        self.structured_output = structured_output
        for k, v in kwargs.items():
            setattr(self, k, v)


class MockAgent:
    """Mock Agent for testing."""
    def __init__(self, agent_config=None):
        self.agent_config = agent_config
        self._closed = False
    
    async def generate(self, prompt="", structured_output=True, **kwargs):
        if self._closed:
            raise RuntimeError("Agent is closed")
        return {
            "code": "import matplotlib.pyplot as plt\nplt.plot([1,2,3])\nplt.show()",
            "explanation": "Test chart generation",
            "confidence": 0.8
        }
    
    async def close(self):
        self._closed = True


def setup_adk_mocks():
    """Set up mock ADK modules in sys.modules."""
    # Create mock modules
    adk_module = types.ModuleType('google.adk')
    adk_module.Agent = MockAgent
    adk_module.AgentConfig = MockAgentConfig
    
    adk_models_module = types.ModuleType('google.adk.models')
    adk_models_module.ModelConfig = MockModelConfig
    
    # Register modules
    sys.modules['google.adk'] = adk_module
    sys.modules['google.adk.models'] = adk_models_module
    
    return adk_module, adk_models_module


def teardown_adk_mocks():
    """Remove mock ADK modules from sys.modules."""
    modules_to_remove = ['google.adk', 'google.adk.models']
    for module in modules_to_remove:
        if module in sys.modules:
            del sys.modules[module]
