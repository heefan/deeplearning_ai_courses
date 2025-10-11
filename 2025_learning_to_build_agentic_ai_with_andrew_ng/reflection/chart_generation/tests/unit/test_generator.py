"""
Unit tests for the Generator Agent.

These tests use mocked ADK responses to verify the generator agent
functionality without requiring real LMStudio connections.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from google.adk.models import ModelConfig

from src.agents.generator import GeneratorAgent, GeneratorResponse
from src.utils.data_schema import DataSchema


class TestGeneratorAgent:
    """Test cases for the Generator Agent."""
    
    @pytest.fixture
    def mock_model_config(self):
        """Mock ModelConfig for testing."""
        return ModelConfig(
            model_name="test-model",
            endpoint="http://localhost:1234/v1"
        )
    
    @pytest.fixture
    def mock_data_schema(self):
        """Mock DataSchema for testing."""
        schema = Mock(spec=DataSchema)
        schema.get_description.return_value = "Test dataset description"
        schema.columns = ["date", "coffee_name", "price"]
        schema.get_sample_data.return_value = "Sample data here"
        return schema
    
    @pytest.fixture
    def generator_agent(self, mock_model_config, mock_data_schema):
        """Create GeneratorAgent instance for testing."""
        return GeneratorAgent(
            model_config=mock_model_config,
            data_schema=mock_data_schema,
            max_retries=2
        )
    
    @pytest.mark.asyncio
    async def test_initialization(self, generator_agent):
        """Test agent initialization."""
        assert generator_agent.model_config is not None
        assert generator_agent.data_schema is not None
        assert generator_agent.max_retries == 2
        assert generator_agent._agent is None
    
    @pytest.mark.asyncio
    async def test_agent_initialization_lazy(self, generator_agent):
        """Test that agent is initialized lazily."""
        assert generator_agent._agent is None
        
        # Mock the agent creation
        with patch('src.agents.generator.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            await generator_agent._initialize_agent()
            
            assert generator_agent._agent is not None
            mock_agent_class.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_code_success(self, generator_agent):
        """Test successful code generation."""
        # Mock agent response
        mock_response = {
            "code": "import matplotlib.pyplot as plt\nplt.plot([1,2,3])\nplt.show()",
            "explanation": "Creates a simple line plot",
            "confidence": 0.95
        }
        
        with patch('src.agents.generator.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.return_value = mock_response
            mock_agent_class.return_value = mock_agent
            
            result = await generator_agent.generate_code("Create a line plot")
            
            assert isinstance(result, GeneratorResponse)
            assert result.code.startswith("<execute_python>")
            assert result.code.endswith("</execute_python>")
            assert result.explanation == "Creates a simple line plot"
            assert result.confidence == 0.95
    
    @pytest.mark.asyncio
    async def test_generate_code_with_context(self, generator_agent):
        """Test code generation with context."""
        context = {
            "previous_attempts": [
                {"code": "old code", "feedback": "needs improvement"}
            ]
        }
        
        mock_response = {
            "code": "improved code",
            "explanation": "Better code",
            "confidence": 0.9
        }
        
        with patch('src.agents.generator.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.return_value = mock_response
            mock_agent_class.return_value = mock_agent
            
            result = await generator_agent.generate_code("Create a chart", context)
            
            # Verify context was included in prompt
            call_args = mock_agent.generate.call_args
            prompt = call_args[1]['prompt']
            assert "Previous attempts" in prompt
            assert "old code" in prompt
    
    @pytest.mark.asyncio
    async def test_generate_code_retry_on_failure(self, generator_agent):
        """Test retry logic on agent failures."""
        with patch('src.agents.generator.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.side_effect = [Exception("Network error"), {
                "code": "success code",
                "explanation": "Success",
                "confidence": 0.8
            }]
            mock_agent_class.return_value = mock_agent
            
            result = await generator_agent.generate_code("Create a chart")
            
            assert result.code == "<execute_python>\nsuccess code\n</execute_python>"
            assert mock_agent.generate.call_count == 2
    
    @pytest.mark.asyncio
    async def test_generate_code_max_retries_exceeded(self, generator_agent):
        """Test behavior when max retries are exceeded."""
        with patch('src.agents.generator.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.side_effect = Exception("Persistent error")
            mock_agent_class.return_value = mock_agent
            
            with pytest.raises(RuntimeError, match="Generator agent failed after 2 attempts"):
                await generator_agent.generate_code("Create a chart")
    
    def test_build_system_prompt(self, generator_agent):
        """Test system prompt construction."""
        prompt = generator_agent._build_system_prompt()
        
        assert "Test dataset description" in prompt
        assert "date, coffee_name, price" in prompt
        assert "Sample data here" in prompt
        assert "<execute_python>" in prompt
    
    def test_build_user_prompt(self, generator_agent):
        """Test user prompt construction."""
        query = "Create a bar chart"
        context = {"previous_attempts": [{"code": "old", "feedback": "bad"}]}
        
        prompt = generator_agent._build_user_prompt(query, context)
        
        assert "Create a bar chart" in prompt
        assert "Previous attempts" in prompt
        assert "old" in prompt
        assert "bad" in prompt
    
    def test_parse_response_success(self, generator_agent):
        """Test successful response parsing."""
        response = {
            "code": "test code",
            "explanation": "test explanation",
            "confidence": 0.8
        }
        
        result = generator_agent._parse_response(response)
        
        assert result.code == "<execute_python>\ntest code\n</execute_python>"
        assert result.explanation == "test explanation"
        assert result.confidence == 0.8
    
    def test_parse_response_missing_fields(self, generator_agent):
        """Test response parsing with missing fields."""
        response = {"code": "test code"}
        
        result = generator_agent._parse_response(response)
        
        assert result.code == "<execute_python>\ntest code\n</execute_python>"
        assert result.explanation == ""
        assert result.confidence == 0.0
    
    def test_parse_response_invalid_confidence(self, generator_agent):
        """Test response parsing with invalid confidence."""
        response = {
            "code": "test code",
            "confidence": "invalid"
        }
        
        with pytest.raises(RuntimeError, match="Failed to parse generator response"):
            generator_agent._parse_response(response)
    
    @pytest.mark.asyncio
    async def test_close(self, generator_agent):
        """Test agent cleanup."""
        with patch('src.agents.generator.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            await generator_agent._initialize_agent()
            await generator_agent.close()
            
            mock_agent.close.assert_called_once()
            assert generator_agent._agent is None
