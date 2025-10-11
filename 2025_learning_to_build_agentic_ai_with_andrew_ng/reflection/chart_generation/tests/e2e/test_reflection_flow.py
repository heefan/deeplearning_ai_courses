"""
End-to-end tests for the reflection workflow.

These tests verify the complete reflection loop between generator and critic agents
using mocked LLM responses to simulate real-world scenarios.
"""

import pytest
from unittest.mock import AsyncMock, patch
from google.adk.models import ModelConfig

from src.agents.generator import GeneratorAgent
from src.agents.critic import CriticAgent
from src.agents.orchestrator import ReflectionOrchestrator
from src.executor.code_executor import CodeExecutor
from src.utils.data_schema import DataSchema


class TestReflectionFlow:
    """Test cases for the complete reflection workflow."""
    
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
        schema.get_description.return_value = "Test dataset with coffee sales data"
        schema.columns = ["date", "coffee_name", "price"]
        schema.get_sample_data.return_value = "Sample data"
        return schema
    
    @pytest.fixture
    def mock_executor(self):
        """Mock CodeExecutor for testing."""
        executor = Mock(spec=CodeExecutor)
        executor.execute_code = AsyncMock()
        return executor
    
    @pytest.fixture
    def generator_agent(self, mock_model_config, mock_data_schema):
        """Create GeneratorAgent with mocked dependencies."""
        return GeneratorAgent(
            model_config=mock_model_config,
            data_schema=mock_data_schema,
            max_retries=2
        )
    
    @pytest.fixture
    def critic_agent(self, mock_model_config):
        """Create CriticAgent with mocked dependencies."""
        return CriticAgent(
            model_config=mock_model_config,
            max_retries=2
        )
    
    @pytest.fixture
    def orchestrator(self, generator_agent, critic_agent, mock_executor):
        """Create ReflectionOrchestrator with all dependencies."""
        return ReflectionOrchestrator(
            generator=generator_agent,
            critic=critic_agent,
            executor=mock_executor,
            max_iterations=3
        )
    
    @pytest.mark.asyncio
    async def test_reflection_flow_immediate_approval(self, orchestrator):
        """Test reflection flow with immediate approval."""
        # Mock generator response
        generator_response = {
            "code": "import matplotlib.pyplot as plt\nplt.plot([1,2,3])\nplt.show()",
            "explanation": "Creates a simple line plot",
            "confidence": 0.95
        }
        
        # Mock critic response (approval)
        critic_response = {
            "result": "approved",
            "feedback": "Code looks good",
            "suggestions": [],
            "confidence": 0.9,
            "issues": []
        }
        
        # Mock execution result
        execution_result = Mock()
        execution_result.success = True
        execution_result.generated_files = ["plot.png"]
        
        with patch('src.agents.generator.Agent') as mock_gen_agent, \
             patch('src.agents.critic.Agent') as mock_crit_agent:
            
            # Setup generator mock
            gen_agent = AsyncMock()
            gen_agent.generate.return_value = generator_response
            mock_gen_agent.return_value = gen_agent
            
            # Setup critic mock
            crit_agent = AsyncMock()
            crit_agent.generate.return_value = critic_response
            mock_crit_agent.return_value = crit_agent
            
            # Setup executor mock
            orchestrator.executor.execute_code.return_value = execution_result
            
            result = await orchestrator.reflect_and_generate("Create a line plot")
            
            # Verify result
            assert result.success is True
            assert result.iterations == 1
            assert result.final_code.startswith("<execute_python>")
            assert result.execution_result is not None
            assert len(result.history) == 1
            
            # Verify history
            history_entry = result.history[0]
            assert history_entry["iteration"] == 1
            assert "generator_response" in history_entry
            assert "critique_response" in history_entry
    
    @pytest.mark.asyncio
    async def test_reflection_flow_with_improvement(self, orchestrator):
        """Test reflection flow requiring improvement iterations."""
        # First iteration - needs improvement
        generator_response_1 = {
            "code": "bad code",
            "explanation": "First attempt",
            "confidence": 0.6
        }
        
        critic_response_1 = {
            "result": "needs_improvement",
            "feedback": "Code needs better error handling",
            "suggestions": ["Add try-catch blocks", "Improve variable names"],
            "confidence": 0.8,
            "issues": ["Missing error handling"]
        }
        
        # Second iteration - approved
        generator_response_2 = {
            "code": "improved code",
            "explanation": "Better code with error handling",
            "confidence": 0.9
        }
        
        critic_response_2 = {
            "result": "approved",
            "feedback": "Much better now",
            "suggestions": [],
            "confidence": 0.95,
            "issues": []
        }
        
        execution_result = Mock()
        execution_result.success = True
        execution_result.generated_files = ["improved_plot.png"]
        
        with patch('src.agents.generator.Agent') as mock_gen_agent, \
             patch('src.agents.critic.Agent') as mock_crit_agent:
            
            # Setup generator mock with side effects
            gen_agent = AsyncMock()
            gen_agent.generate.side_effect = [generator_response_1, generator_response_2]
            mock_gen_agent.return_value = gen_agent
            
            # Setup critic mock with side effects
            crit_agent = AsyncMock()
            crit_agent.generate.side_effect = [critic_response_1, critic_response_2]
            mock_crit_agent.return_value = crit_agent
            
            # Setup executor mock
            orchestrator.executor.execute_code.return_value = execution_result
            
            result = await orchestrator.reflect_and_generate("Create a chart")
            
            # Verify result
            assert result.success is True
            assert result.iterations == 2
            assert result.final_code == "<execute_python>\nimproved code\n</execute_python>"
            assert len(result.history) == 2
            
            # Verify history contains both iterations
            assert result.history[0]["iteration"] == 1
            assert result.history[1]["iteration"] == 2
            assert result.history[0]["critique_response"]["result"] == "needs_improvement"
            assert result.history[1]["critique_response"]["result"] == "approved"
    
    @pytest.mark.asyncio
    async def test_reflection_flow_max_iterations(self, orchestrator):
        """Test reflection flow reaching max iterations without approval."""
        # All iterations need improvement
        generator_responses = [
            {"code": f"code_{i}", "explanation": f"Attempt {i}", "confidence": 0.5}
            for i in range(3)
        ]
        
        critic_responses = [
            {
                "result": "needs_improvement",
                "feedback": f"Attempt {i} needs work",
                "suggestions": ["Improve code"],
                "confidence": 0.7,
                "issues": ["Not good enough"]
            }
            for i in range(3)
        ]
        
        with patch('src.agents.generator.Agent') as mock_gen_agent, \
             patch('src.agents.critic.Agent') as mock_crit_agent:
            
            # Setup mocks
            gen_agent = AsyncMock()
            gen_agent.generate.side_effect = generator_responses
            mock_gen_agent.return_value = gen_agent
            
            crit_agent = AsyncMock()
            crit_agent.generate.side_effect = critic_responses
            mock_crit_agent.return_value = crit_agent
            
            result = await orchestrator.reflect_and_generate("Create a chart")
            
            # Verify result
            assert result.success is False
            assert result.iterations == 3
            assert "Maximum iterations reached" in result.error_message
            assert len(result.history) == 3
    
    @pytest.mark.asyncio
    async def test_reflection_flow_execution_failure(self, orchestrator):
        """Test reflection flow with execution failure."""
        generator_response = {
            "code": "import matplotlib.pyplot as plt\nplt.plot([1,2,3])",
            "explanation": "Simple plot",
            "confidence": 0.9
        }
        
        critic_response = {
            "result": "approved",
            "feedback": "Code looks good",
            "suggestions": [],
            "confidence": 0.9,
            "issues": []
        }
        
        # Mock execution failure
        orchestrator.executor.execute_code.side_effect = Exception("Execution failed")
        
        with patch('src.agents.generator.Agent') as mock_gen_agent, \
             patch('src.agents.critic.Agent') as mock_crit_agent:
            
            gen_agent = AsyncMock()
            gen_agent.generate.return_value = generator_response
            mock_gen_agent.return_value = gen_agent
            
            crit_agent = AsyncMock()
            crit_agent.generate.return_value = critic_response
            mock_crit_agent.return_value = crit_agent
            
            result = await orchestrator.reflect_and_generate("Create a chart")
            
            # Should still succeed even if execution fails
            assert result.success is True
            assert result.iterations == 1
            assert result.execution_result is None
            assert "execution_error" in result.history[0]
    
    @pytest.mark.asyncio
    async def test_reflection_flow_without_execution(self, orchestrator):
        """Test reflection flow without code execution."""
        generator_response = {
            "code": "import matplotlib.pyplot as plt\nplt.plot([1,2,3])",
            "explanation": "Simple plot",
            "confidence": 0.9
        }
        
        critic_response = {
            "result": "approved",
            "feedback": "Code looks good",
            "suggestions": [],
            "confidence": 0.9,
            "issues": []
        }
        
        with patch('src.agents.generator.Agent') as mock_gen_agent, \
             patch('src.agents.critic.Agent') as mock_crit_agent:
            
            gen_agent = AsyncMock()
            gen_agent.generate.return_value = generator_response
            mock_gen_agent.return_value = gen_agent
            
            crit_agent = AsyncMock()
            crit_agent.generate.return_value = critic_response
            mock_crit_agent.return_value = crit_agent
            
            result = await orchestrator.reflect_and_generate("Create a chart", execute_code=False)
            
            # Should succeed without execution
            assert result.success is True
            assert result.iterations == 1
            assert result.execution_result is None
            assert orchestrator.executor.execute_code.call_count == 0
    
    @pytest.mark.asyncio
    async def test_reflection_flow_generator_failure(self, orchestrator):
        """Test reflection flow with generator failure."""
        with patch('src.agents.generator.Agent') as mock_gen_agent, \
             patch('src.agents.critic.Agent') as mock_crit_agent:
            
            gen_agent = AsyncMock()
            gen_agent.generate.side_effect = Exception("Generator failed")
            mock_gen_agent.return_value = gen_agent
            
            crit_agent = AsyncMock()
            mock_crit_agent.return_value = crit_agent
            
            result = await orchestrator.reflect_and_generate("Create a chart")
            
            # Should fail gracefully
            assert result.success is False
            assert "Reflection process failed" in result.error_message
            assert result.iterations == 0
    
    @pytest.mark.asyncio
    async def test_orchestrator_close(self, orchestrator):
        """Test orchestrator cleanup."""
        with patch('src.agents.generator.Agent') as mock_gen_agent, \
             patch('src.agents.critic.Agent') as mock_crit_agent:
            
            gen_agent = AsyncMock()
            crit_agent = AsyncMock()
            mock_gen_agent.return_value = gen_agent
            mock_crit_agent.return_value = crit_agent
            
            # Initialize agents
            await orchestrator.generator._initialize_agent()
            await orchestrator.critic._initialize_agent()
            
            # Close orchestrator
            await orchestrator.close()
            
            # Verify agents were closed
            gen_agent.close.assert_called_once()
            crit_agent.close.assert_called_once()
