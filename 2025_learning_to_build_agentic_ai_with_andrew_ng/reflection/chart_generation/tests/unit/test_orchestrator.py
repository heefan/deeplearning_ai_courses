"""
Unit tests for the Reflection Orchestrator.

These tests verify the orchestrator's ability to coordinate the generator-critic
reflection loop for iterative code improvement, specifically testing the case
where the orchestrator calls the generator agent for Q1 coffee sales comparison.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime

from src.agents.orchestrator import ReflectionOrchestrator, ReflectionResult
from src.agents.generator import GeneratorAgent, GeneratorResponse
from src.agents.critic import CriticAgent, CritiqueResponse, CritiqueResult
from src.executor.code_executor import CodeExecutor, ExecutionResult


class TestReflectionOrchestrator:
    """Test cases for the Reflection Orchestrator."""
    
    @pytest.fixture
    def mock_generator(self):
        """Mock GeneratorAgent for testing."""
        generator = Mock(spec=GeneratorAgent)
        generator.close = AsyncMock()
        return generator
    
    @pytest.fixture
    def mock_critic(self):
        """Mock CriticAgent for testing."""
        critic = Mock(spec=CriticAgent)
        critic.close = AsyncMock()
        return critic
    
    @pytest.fixture
    def mock_executor(self):
        """Mock CodeExecutor for testing."""
        executor = Mock(spec=CodeExecutor)
        return executor
    
    @pytest.fixture
    def orchestrator(self, mock_generator, mock_critic, mock_executor):
        """Create ReflectionOrchestrator instance for testing."""
        return ReflectionOrchestrator(
            generator=mock_generator,
            critic=mock_critic,
            executor=mock_executor,
            max_iterations=3
        )
    
    @pytest.mark.asyncio
    async def test_initialization(self, orchestrator, mock_generator, mock_critic, mock_executor):
        """Test orchestrator initialization."""
        assert orchestrator.generator == mock_generator
        assert orchestrator.critic == mock_critic
        assert orchestrator.executor == mock_executor
        assert orchestrator.max_iterations == 3
    
    @pytest.mark.asyncio
    async def test_q1_coffee_sales_comparison_success_first_iteration(self, orchestrator):
        """Test Case 1: Orchestrator calls generator for Q1 coffee sales comparison and succeeds immediately."""
        # Mock generator response for Q1 coffee sales comparison
        generator_response = GeneratorResponse(
            code="<execute_python>\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n# Load data\ndf = pd.read_csv('coffee_sales.csv')\n\n# Filter Q1 data for 2024 and 2025\nq1_2024 = df[(df['date'].str.contains('2024')) & (df['date'].str.contains('Q1'))]\nq1_2025 = df[(df['date'].str.contains('2025')) & (df['date'].str.contains('Q1'))]\n\n# Create comparison\nplt.figure(figsize=(12, 6))\nplt.plot(q1_2024['date'], q1_2024['sales'], label='Q1 2024', marker='o')\nplt.plot(q1_2025['date'], q1_2025['sales'], label='Q1 2025', marker='s')\nplt.title('Q1 Coffee Sales Comparison: 2024 vs 2025')\nplt.xlabel('Date')\nplt.ylabel('Sales')\nplt.legend()\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.show()\n</execute_python>",
            explanation="Creates a line plot comparing Q1 coffee sales between 2024 and 2025, filtering the data by quarter and year.",
            confidence=0.95
        )
        
        # Mock critic response - approves the code
        critique_response = CritiqueResponse(
            result=CritiqueResult.APPROVED,
            feedback="The code correctly filters Q1 data for both years and creates an appropriate comparison chart.",
            suggestions=[],
            confidence=0.9,
            issues=[]
        )
        
        # Mock execution result
        execution_result = ExecutionResult(
            success=True,
            output="Chart generated successfully",
            error=None,
            execution_time=1.5,
            generated_files=["chart.png"],
            return_code=0
        )
        
        # Configure mocks
        orchestrator.generator.generate_code = AsyncMock(return_value=generator_response)
        orchestrator.critic.critique_code = AsyncMock(return_value=critique_response)
        orchestrator.executor.execute_code = AsyncMock(return_value=execution_result)
        
        # Execute the reflection process
        user_query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        result = await orchestrator.reflect_and_generate(user_query, execute_code=True)
        
        # Verify the result
        assert isinstance(result, ReflectionResult)
        assert result.success is True
        assert result.iterations == 1
        assert result.final_code == generator_response.code
        assert result.execution_result == execution_result
        assert result.error_message is None
        assert len(result.history) == 1
        
        # Verify history record
        history_record = result.history[0]
        assert history_record["iteration"] == 1
        assert history_record["generator_response"]["code"] == generator_response.code
        assert history_record["generator_response"]["explanation"] == generator_response.explanation
        assert history_record["generator_response"]["confidence"] == 0.95
        assert history_record["critique_response"]["result"] == "approved"
        assert history_record["critique_response"]["feedback"] == critique_response.feedback
        
        # Verify agent calls
        orchestrator.generator.generate_code.assert_called_once_with(user_query, {})
        orchestrator.critic.critique_code.assert_called_once_with(
            generator_response.code, user_query, {}
        )
        orchestrator.executor.execute_code.assert_called_once_with(generator_response.code)
    
    @pytest.mark.asyncio
    async def test_q1_coffee_sales_comparison_with_reflection_loop(self, orchestrator):
        """Test Case 1 with reflection loop: Generator creates code, critic suggests improvements, then approves."""
        # First iteration - generator creates initial code
        initial_generator_response = GeneratorResponse(
            code="<execute_python>\n# Basic plot without proper Q1 filtering\nimport matplotlib.pyplot as plt\nplt.plot([1,2,3], [4,5,6])\nplt.show()\n</execute_python>",
            explanation="Creates a basic plot",
            confidence=0.7
        )
        
        # First critique - needs improvement
        initial_critique_response = CritiqueResponse(
            result=CritiqueResult.NEEDS_IMPROVEMENT,
            feedback="The code doesn't properly filter for Q1 data or compare 2024 vs 2025. Need to load the CSV and filter by quarter and year.",
            suggestions=["Load the coffee_sales.csv file", "Filter data by Q1 for both years", "Create a proper comparison chart"],
            confidence=0.8,
            issues=["Missing data loading", "No Q1 filtering", "No year comparison"]
        )
        
        # Second iteration - improved code
        improved_generator_response = GeneratorResponse(
            code="<execute_python>\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n# Load and filter Q1 data for 2024 and 2025\ndf = pd.read_csv('coffee_sales.csv')\nq1_2024 = df[(df['date'].str.contains('2024')) & (df['date'].str.contains('Q1'))]\nq1_2025 = df[(df['date'].str.contains('2025')) & (df['date'].str.contains('Q1'))]\n\nplt.figure(figsize=(12, 6))\nplt.plot(q1_2024['date'], q1_2024['sales'], label='Q1 2024', marker='o')\nplt.plot(q1_2025['date'], q1_2025['sales'], label='Q1 2025', marker='s')\nplt.title('Q1 Coffee Sales Comparison: 2024 vs 2025')\nplt.xlabel('Date')\nplt.ylabel('Sales')\nplt.legend()\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.show()\n</execute_python>",
            explanation="Now properly loads the CSV, filters for Q1 data in both 2024 and 2025, and creates a comparison chart.",
            confidence=0.9
        )
        
        # Second critique - approves
        final_critique_response = CritiqueResponse(
            result=CritiqueResult.APPROVED,
            feedback="Excellent! The code now properly loads the data, filters for Q1 in both years, and creates an appropriate comparison chart.",
            suggestions=[],
            confidence=0.95,
            issues=[]
        )
        
        # Mock execution result
        execution_result = ExecutionResult(
            success=True,
            output="Q1 comparison chart generated successfully",
            error=None,
            execution_time=2.0,
            generated_files=["q1_comparison.png"],
            return_code=0
        )
        
        # Configure mocks with side effects for multiple calls
        orchestrator.generator.generate_code = AsyncMock(side_effect=[
            initial_generator_response,
            improved_generator_response
        ])
        orchestrator.critic.critique_code = AsyncMock(side_effect=[
            initial_critique_response,
            final_critique_response
        ])
        orchestrator.executor.execute_code = AsyncMock(return_value=execution_result)
        
        # Execute the reflection process
        user_query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        result = await orchestrator.reflect_and_generate(user_query, execute_code=True)
        
        # Verify the result
        assert isinstance(result, ReflectionResult)
        assert result.success is True
        assert result.iterations == 2
        assert result.final_code == improved_generator_response.code
        assert result.execution_result == execution_result
        assert result.error_message is None
        assert len(result.history) == 2
        
        # Verify first iteration history
        first_iteration = result.history[0]
        assert first_iteration["iteration"] == 1
        assert first_iteration["critique_response"]["result"] == "needs_improvement"
        assert "Q1 data" in first_iteration["critique_response"]["feedback"]
        
        # Verify second iteration history
        second_iteration = result.history[1]
        assert second_iteration["iteration"] == 2
        assert second_iteration["critique_response"]["result"] == "approved"
        
        # Verify context was passed to second generation
        second_call_args = orchestrator.generator.generate_code.call_args_list[1]
        context = second_call_args[0][1]  # Second positional argument
        assert "previous_attempts" in context
        assert len(context["previous_attempts"]) == 1
        assert context["previous_attempts"][0]["code"] == initial_generator_response.code
        assert context["previous_attempts"][0]["feedback"] == initial_critique_response.feedback
        
        # Verify agent calls
        assert orchestrator.generator.generate_code.call_count == 2
        assert orchestrator.critic.critique_code.call_count == 2
        orchestrator.executor.execute_code.assert_called_once_with(improved_generator_response.code)
    
    @pytest.mark.asyncio
    async def test_max_iterations_reached_without_approval(self, orchestrator):
        """Test behavior when max iterations are reached without approval."""
        # Mock responses that never get approved
        generator_response = GeneratorResponse(
            code="<execute_python>\n# Code that never gets approved\nprint('test')\n</execute_python>",
            explanation="Test code",
            confidence=0.5
        )
        
        critique_response = CritiqueResponse(
            result=CritiqueResult.NEEDS_IMPROVEMENT,
            feedback="Code needs improvement",
            suggestions=["Improve the code"],
            confidence=0.6,
            issues=["Not good enough"]
        )
        
        # Configure mocks to always return the same responses
        orchestrator.generator.generate_code = AsyncMock(return_value=generator_response)
        orchestrator.critic.critique_code = AsyncMock(return_value=critique_response)
        
        # Execute the reflection process
        user_query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        result = await orchestrator.reflect_and_generate(user_query, execute_code=False)
        
        # Verify the result
        assert isinstance(result, ReflectionResult)
        assert result.success is False
        assert result.iterations == 3  # Max iterations reached
        assert result.final_code == generator_response.code
        assert result.execution_result is None
        assert result.error_message == "Maximum iterations reached without approval"
        assert len(result.history) == 3
        
        # Verify all iterations were recorded
        for i, record in enumerate(result.history):
            assert record["iteration"] == i + 1
            assert record["critique_response"]["result"] == "needs_improvement"
        
        # Verify agent calls
        assert orchestrator.generator.generate_code.call_count == 3
        assert orchestrator.critic.critique_code.call_count == 3
        orchestrator.executor.execute_code.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execution_failure_after_approval(self, orchestrator):
        """Test behavior when code is approved but execution fails."""
        generator_response = GeneratorResponse(
            code="<execute_python>\n# Code that gets approved but fails execution\ninvalid_syntax_here\n</execute_python>",
            explanation="Code that will fail execution",
            confidence=0.8
        )
        
        critique_response = CritiqueResponse(
            result=CritiqueResult.APPROVED,
            feedback="Code looks good",
            suggestions=[],
            confidence=0.9,
            issues=[]
        )
        
        # Configure mocks
        orchestrator.generator.generate_code = AsyncMock(return_value=generator_response)
        orchestrator.critic.critique_code = AsyncMock(return_value=critique_response)
        orchestrator.executor.execute_code = AsyncMock(side_effect=Exception("Syntax error"))
        
        # Execute the reflection process
        user_query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        result = await orchestrator.reflect_and_generate(user_query, execute_code=True)
        
        # Verify the result
        assert isinstance(result, ReflectionResult)
        assert result.success is True  # Still successful because code was approved
        assert result.iterations == 1
        assert result.final_code == generator_response.code
        assert result.execution_result is None
        assert result.error_message is None
        
        # Verify execution error was recorded in history
        history_record = result.history[0]
        assert "execution_error" in history_record
        assert "Syntax error" in history_record["execution_error"]
    
    @pytest.mark.asyncio
    async def test_generator_failure_handling(self, orchestrator):
        """Test handling of generator agent failures."""
        # Configure generator to fail
        orchestrator.generator.generate_code = AsyncMock(side_effect=Exception("Generator failed"))
        orchestrator.critic.critique_code = AsyncMock()
        orchestrator.executor.execute_code = AsyncMock()
        
        # Execute the reflection process
        user_query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        result = await orchestrator.reflect_and_generate(user_query, execute_code=True)
        
        # Verify the result
        assert isinstance(result, ReflectionResult)
        assert result.success is False
        assert result.iterations == 0
        assert result.final_code == ""
        assert result.execution_result is None
        assert "Reflection process failed: Generator failed" in result.error_message
        assert len(result.history) == 0
        
        # Verify no other agents were called
        orchestrator.critic.critique_code.assert_not_called()
        orchestrator.executor.execute_code.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_critic_failure_handling(self, orchestrator):
        """Test handling of critic agent failures."""
        generator_response = GeneratorResponse(
            code="<execute_python>\nprint('test')\n</execute_python>",
            explanation="Test code",
            confidence=0.8
        )
        
        # Configure critic to fail
        orchestrator.generator.generate_code = AsyncMock(return_value=generator_response)
        orchestrator.critic.critique_code = AsyncMock(side_effect=Exception("Critic failed"))
        orchestrator.executor.execute_code = AsyncMock()
        
        # Execute the reflection process
        user_query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        result = await orchestrator.reflect_and_generate(user_query, execute_code=True)
        
        # Verify the result
        assert isinstance(result, ReflectionResult)
        assert result.success is False
        assert result.iterations == 0
        assert result.final_code == ""
        assert result.execution_result is None
        assert "Reflection process failed: Critic failed" in result.error_message
        assert len(result.history) == 0
        
        # Verify generator was called but executor was not
        orchestrator.generator.generate_code.assert_called_once()
        orchestrator.executor.execute_code.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_context_accumulation_across_iterations(self, orchestrator):
        """Test that context accumulates properly across multiple iterations."""
        # Mock responses for 3 iterations
        generator_responses = [
            GeneratorResponse(code="code1", explanation="explanation1", confidence=0.6),
            GeneratorResponse(code="code2", explanation="explanation2", confidence=0.7),
            GeneratorResponse(code="code3", explanation="explanation3", confidence=0.8)
        ]
        
        critique_responses = [
            CritiqueResponse(
                result=CritiqueResult.NEEDS_IMPROVEMENT,
                feedback="feedback1",
                suggestions=["suggestion1"],
                confidence=0.7,
                issues=["issue1"]
            ),
            CritiqueResponse(
                result=CritiqueResult.NEEDS_IMPROVEMENT,
                feedback="feedback2",
                suggestions=["suggestion2"],
                confidence=0.8,
                issues=["issue2"]
            ),
            CritiqueResponse(
                result=CritiqueResult.APPROVED,
                feedback="feedback3",
                suggestions=[],
                confidence=0.9,
                issues=[]
            )
        ]
        
        # Configure mocks
        orchestrator.generator.generate_code = AsyncMock(side_effect=generator_responses)
        orchestrator.critic.critique_code = AsyncMock(side_effect=critique_responses)
        orchestrator.executor.execute_code = AsyncMock(return_value=ExecutionResult(
            success=True, output="Success", error=None, execution_time=1.0, generated_files=["test.png"], return_code=0
        ))
        
        # Execute the reflection process
        user_query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        result = await orchestrator.reflect_and_generate(user_query, execute_code=True)
        
        # Verify the result
        assert result.success is True
        assert result.iterations == 3
        
        # Verify context accumulation in generator calls
        generator_calls = orchestrator.generator.generate_code.call_args_list
        
        # Verify that context was passed to each call (context is modified in place)
        assert len(generator_calls) == 3
        
        # Check that the final context contains accumulated data
        # Note: context is modified in place, so we check the final state
        final_context = generator_calls[2][0][1]
        assert "previous_attempts" in final_context
        assert len(final_context["previous_attempts"]) == 2
        assert final_context["previous_attempts"][0]["code"] == "code1"
        assert final_context["previous_attempts"][1]["code"] == "code2"
        
        # Verify previous critiques accumulation
        assert "previous_critiques" in final_context
        assert len(final_context["previous_critiques"]) == 2
    
    @pytest.mark.asyncio
    async def test_close_cleanup(self, orchestrator):
        """Test orchestrator cleanup."""
        await orchestrator.close()
        
        # Verify all agents were closed
        orchestrator.generator.close.assert_called_once()
        orchestrator.critic.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_reflect_and_generate_without_execution(self, orchestrator):
        """Test reflection process without code execution."""
        generator_response = GeneratorResponse(
            code="<execute_python>\nprint('test')\n</execute_python>",
            explanation="Test code",
            confidence=0.8
        )
        
        critique_response = CritiqueResponse(
            result=CritiqueResult.APPROVED,
            feedback="Code looks good",
            suggestions=[],
            confidence=0.9,
            issues=[]
        )
        
        # Configure mocks
        orchestrator.generator.generate_code = AsyncMock(return_value=generator_response)
        orchestrator.critic.critique_code = AsyncMock(return_value=critique_response)
        
        # Execute without code execution
        user_query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        result = await orchestrator.reflect_and_generate(user_query, execute_code=False)
        
        # Verify the result
        assert result.success is True
        assert result.iterations == 1
        assert result.final_code == generator_response.code
        assert result.execution_result is None
        
        # Verify executor was not called
        orchestrator.executor.execute_code.assert_not_called()
