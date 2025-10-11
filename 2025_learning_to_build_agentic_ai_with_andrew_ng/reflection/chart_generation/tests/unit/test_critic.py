"""
Unit tests for the Critic Agent.

These tests use mocked ADK responses to verify the critic agent
functionality without requiring real LMStudio connections.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from google.adk.models import ModelConfig

from src.agents.critic import CriticAgent, CritiqueResponse, CritiqueResult


class TestCriticAgent:
    """Test cases for the Critic Agent."""
    
    @pytest.fixture
    def mock_model_config(self):
        """Mock ModelConfig for testing."""
        return ModelConfig(
            model_name="test-model",
            endpoint="http://localhost:1234/v1"
        )
    
    @pytest.fixture
    def critic_agent(self, mock_model_config):
        """Create CriticAgent instance for testing."""
        return CriticAgent(
            model_config=mock_model_config,
            max_retries=2
        )
    
    @pytest.mark.asyncio
    async def test_initialization(self, critic_agent):
        """Test agent initialization."""
        assert critic_agent.model_config is not None
        assert critic_agent.max_retries == 2
        assert critic_agent._agent is None
    
    @pytest.mark.asyncio
    async def test_agent_initialization_lazy(self, critic_agent):
        """Test that agent is initialized lazily."""
        assert critic_agent._agent is None
        
        with patch('src.agents.critic.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            await critic_agent._initialize_agent()
            
            assert critic_agent._agent is not None
            mock_agent_class.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_critique_code_approved(self, critic_agent):
        """Test code critique with approval."""
        mock_response = {
            "result": "approved",
            "feedback": "Code looks good",
            "suggestions": [],
            "confidence": 0.95,
            "issues": []
        }
        
        with patch('src.agents.critic.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.return_value = mock_response
            mock_agent_class.return_value = mock_agent
            
            result = await critic_agent.critique_code("test code", "Create a chart")
            
            assert isinstance(result, CritiqueResponse)
            assert result.result == CritiqueResult.APPROVED
            assert result.feedback == "Code looks good"
            assert result.confidence == 0.95
            assert result.suggestions == []
            assert result.issues == []
    
    @pytest.mark.asyncio
    async def test_critique_code_needs_improvement(self, critic_agent):
        """Test code critique with improvement needed."""
        mock_response = {
            "result": "needs_improvement",
            "feedback": "Code needs better error handling",
            "suggestions": ["Add try-catch blocks", "Improve error messages"],
            "confidence": 0.8,
            "issues": ["Missing error handling", "Poor variable names"]
        }
        
        with patch('src.agents.critic.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.return_value = mock_response
            mock_agent_class.return_value = mock_agent
            
            result = await critic_agent.critique_code("test code", "Create a chart")
            
            assert result.result == CritiqueResult.NEEDS_IMPROVEMENT
            assert result.feedback == "Code needs better error handling"
            assert len(result.suggestions) == 2
            assert len(result.issues) == 2
    
    @pytest.mark.asyncio
    async def test_critique_code_rejected(self, critic_agent):
        """Test code critique with rejection."""
        mock_response = {
            "result": "rejected",
            "feedback": "Code has serious issues",
            "suggestions": ["Rewrite completely"],
            "confidence": 0.9,
            "issues": ["Syntax errors", "Logic errors"]
        }
        
        with patch('src.agents.critic.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.return_value = mock_response
            mock_agent_class.return_value = mock_agent
            
            result = await critic_agent.critique_code("test code", "Create a chart")
            
            assert result.result == CritiqueResult.REJECTED
            assert result.feedback == "Code has serious issues"
    
    @pytest.mark.asyncio
    async def test_critique_code_with_context(self, critic_agent):
        """Test code critique with context."""
        context = {
            "previous_critiques": [
                {"feedback": "Previous feedback", "suggestions": ["old suggestion"]}
            ]
        }
        
        mock_response = {
            "result": "approved",
            "feedback": "Good now",
            "suggestions": [],
            "confidence": 0.9,
            "issues": []
        }
        
        with patch('src.agents.critic.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.return_value = mock_response
            mock_agent_class.return_value = mock_agent
            
            result = await critic_agent.critique_code("test code", "Create a chart", context)
            
            # Verify context was included in prompt
            call_args = mock_agent.generate.call_args
            prompt = call_args[1]['prompt']
            assert "Previous critiques" in prompt
            assert "Previous feedback" in prompt
    
    @pytest.mark.asyncio
    async def test_critique_code_retry_on_failure(self, critic_agent):
        """Test retry logic on agent failures."""
        with patch('src.agents.critic.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.side_effect = [
                Exception("Network error"),
                {
                    "result": "approved",
                    "feedback": "Success",
                    "suggestions": [],
                    "confidence": 0.8,
                    "issues": []
                }
            ]
            mock_agent_class.return_value = mock_agent
            
            result = await critic_agent.critique_code("test code", "Create a chart")
            
            assert result.result == CritiqueResult.APPROVED
            assert mock_agent.generate.call_count == 2
    
    @pytest.mark.asyncio
    async def test_critique_code_max_retries_exceeded(self, critic_agent):
        """Test behavior when max retries are exceeded."""
        with patch('src.agents.critic.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.generate.side_effect = Exception("Persistent error")
            mock_agent_class.return_value = mock_agent
            
            with pytest.raises(RuntimeError, match="Critic agent failed after 2 attempts"):
                await critic_agent.critique_code("test code", "Create a chart")
    
    def test_build_critique_prompt(self, critic_agent):
        """Test critique prompt construction."""
        code = "import matplotlib.pyplot as plt\nplt.plot([1,2,3])"
        query = "Create a line plot"
        context = {"previous_critiques": [{"feedback": "old feedback"}]}
        
        prompt = critic_agent._build_critique_prompt(code, query, context)
        
        assert "Create a line plot" in prompt
        assert "import matplotlib.pyplot as plt" in prompt
        assert "Previous critiques" in prompt
        assert "old feedback" in prompt
    
    def test_parse_response_success(self, critic_agent):
        """Test successful response parsing."""
        response = {
            "result": "needs_improvement",
            "feedback": "test feedback",
            "suggestions": ["suggestion1", "suggestion2"],
            "confidence": 0.8,
            "issues": ["issue1", "issue2"]
        }
        
        result = critic_agent._parse_response(response)
        
        assert result.result == CritiqueResult.NEEDS_IMPROVEMENT
        assert result.feedback == "test feedback"
        assert result.suggestions == ["suggestion1", "suggestion2"]
        assert result.confidence == 0.8
        assert result.issues == ["issue1", "issue2"]
    
    def test_parse_response_missing_fields(self, critic_agent):
        """Test response parsing with missing fields."""
        response = {"result": "approved"}
        
        result = critic_agent._parse_response(response)
        
        assert result.result == CritiqueResult.APPROVED
        assert result.feedback == ""
        assert result.suggestions == []
        assert result.confidence == 0.0
        assert result.issues == []
    
    def test_parse_response_invalid_result(self, critic_agent):
        """Test response parsing with invalid result."""
        response = {
            "result": "invalid_result",
            "feedback": "test",
            "suggestions": [],
            "confidence": 0.8,
            "issues": []
        }
        
        result = critic_agent._parse_response(response)
        
        # Should default to NEEDS_IMPROVEMENT for invalid results
        assert result.result == CritiqueResult.NEEDS_IMPROVEMENT
    
    def test_parse_response_non_list_suggestions(self, critic_agent):
        """Test response parsing with non-list suggestions."""
        response = {
            "result": "approved",
            "suggestions": "single suggestion",
            "issues": "single issue"
        }
        
        result = critic_agent._parse_response(response)
        
        assert result.suggestions == ["single suggestion"]
        assert result.issues == ["single issue"]
    
    def test_parse_response_invalid_confidence(self, critic_agent):
        """Test response parsing with invalid confidence."""
        response = {
            "result": "approved",
            "confidence": "invalid"
        }
        
        with pytest.raises(RuntimeError, match="Failed to parse critic response"):
            critic_agent._parse_response(response)
    
    @pytest.mark.asyncio
    async def test_close(self, critic_agent):
        """Test agent cleanup."""
        with patch('src.agents.critic.Agent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent_class.return_value = mock_agent
            
            await critic_agent._initialize_agent()
            await critic_agent.close()
            
            mock_agent.close.assert_called_once()
            assert critic_agent._agent is None
