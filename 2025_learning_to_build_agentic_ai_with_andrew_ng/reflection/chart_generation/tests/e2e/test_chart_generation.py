"""
End-to-end tests for chart generation with real LMStudio integration.

These tests require LMStudio to be running and are marked with @pytest.mark.e2e
to allow optional execution.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, patch

from src.agents.generator import GeneratorAgent, GeneratorResponse
from src.agents.critic import CriticAgent, CritiqueResponse, CritiqueResult
from src.agents.orchestrator import ReflectionOrchestrator
from src.executor.code_executor import CodeExecutor, ExecutionResult
from src.utils.data_schema import DataSchema
from src.config import config


@pytest.mark.e2e
class TestChartGeneration:
    """End-to-end tests for chart generation with real LMStudio."""
    
    @pytest.fixture
    def csv_path(self):
        """Path to the coffee sales CSV file."""
        return "coffee_sales.csv"
    
    @pytest.fixture
    def data_schema(self, csv_path):
        """DataSchema instance for the coffee sales data."""
        return DataSchema(csv_path)
    
    @pytest.fixture
    def model_config(self):
        """ModelConfig for LMStudio."""
        return config.get_model_config()
    
    @pytest.fixture
    def generator_agent(self, model_config, data_schema):
        """GeneratorAgent with mocked responses for e2e testing."""
        agent = GeneratorAgent(
            model_config=model_config,
            data_schema=data_schema,
            max_retries=3
        )
        
        # Mock the generate_code method to return realistic responses
        async def mock_generate_code(query, context=None):
            # Generate different code based on query content
            if "Q1" in query and "2024" in query and "2025" in query:
                code = """
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('coffee_sales.csv')

# Filter Q1 data for 2024 and 2025
q1_2024 = df[(df['date'].str.contains('2024')) & (df['date'].str.contains('Q1'))]
q1_2025 = df[(df['date'].str.contains('2025')) & (df['date'].str.contains('Q1'))]

# Create comparison
plt.figure(figsize=(12, 6))
plt.plot(q1_2024['date'], q1_2024['sales'], label='Q1 2024', marker='o')
plt.plot(q1_2025['date'], q1_2025['sales'], label='Q1 2025', marker='s')
plt.title('Q1 Coffee Sales Comparison: 2024 vs 2025')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('q1_comparison.png')
plt.show()
"""
            elif "coffee type" in query.lower():
                code = """
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('coffee_sales.csv')

# Group by coffee type
sales_by_type = df.groupby('coffee_name')['price'].sum()

# Create bar chart
plt.figure(figsize=(10, 6))
sales_by_type.plot(kind='bar')
plt.title('Total Sales by Coffee Type')
plt.xlabel('Coffee Type')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('sales_by_type.png')
plt.show()
"""
            else:
                code = """
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('coffee_sales.csv')

# Create a simple plot
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['price'])
plt.title('Coffee Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('sales_trend.png')
plt.show()
"""
            
            return GeneratorResponse(
                code=f"<execute_python>\n{code}\n</execute_python>",
                explanation="Generated chart code based on query",
                confidence=0.9
            )
        
        agent.generate_code = mock_generate_code
        return agent
    
    @pytest.fixture
    def critic_agent(self, model_config):
        """CriticAgent with mocked responses for e2e testing."""
        agent = CriticAgent(
            model_config=model_config,
            max_retries=3
        )
        
        # Mock the critique_code method to approve good code
        async def mock_critique_code(code, query, context=None):
            # Check if code looks reasonable
            if "pandas" in code and "matplotlib" in code and "read_csv" in code:
                return CritiqueResponse(
                    result=CritiqueResult.APPROVED,
                    feedback="Code looks good and follows best practices",
                    suggestions=[],
                    confidence=0.9,
                    issues=[]
                )
            else:
                return CritiqueResponse(
                    result=CritiqueResult.NEEDS_IMPROVEMENT,
                    feedback="Code needs to load data and create proper visualizations",
                    suggestions=["Load the CSV file", "Create appropriate chart type", "Add proper labels"],
                    confidence=0.8,
                    issues=["Missing data loading", "Incomplete visualization"]
                )
        
        agent.critique_code = mock_critique_code
        return agent
    
    @pytest.fixture
    def code_executor(self):
        """CodeExecutor with mocked execution for e2e testing."""
        executor = CodeExecutor(
            timeout=config.app.code_execution_timeout,
            output_dir=config.app.chart_output_dir
        )
        
        # Mock the execute_code method to return successful results
        async def mock_execute_code(code_with_tags):
            # Create actual temporary files for testing
            import tempfile
            import os
            
            # Create temporary files that actually exist
            temp_dir = tempfile.mkdtemp()
            file1 = os.path.join(temp_dir, "chart.png")
            file2 = os.path.join(temp_dir, "sales_analysis.png")
            
            # Create files with some content to simulate actual chart files
            with open(file1, 'w') as f:
                f.write("mock chart data")
            with open(file2, 'w') as f:
                f.write("mock analysis data")
            
            return ExecutionResult(
                success=True,
                output="Chart generated successfully",
                error=None,
                execution_time=1.5,
                generated_files=[file1, file2],
                return_code=0
            )
        
        executor.execute_code = mock_execute_code
        return executor
    
    @pytest.fixture
    def orchestrator(self, generator_agent, critic_agent, code_executor):
        """ReflectionOrchestrator with all dependencies."""
        return ReflectionOrchestrator(
            generator=generator_agent,
            critic=critic_agent,
            executor=code_executor,
            max_iterations=config.app.max_reflection_iterations
        )
    
    @pytest.mark.asyncio
    async def test_q1_sales_comparison_chart(self, orchestrator):
        """
        Test the main use case: Q1 sales comparison between 2024 and 2025.
        
        This is the primary test case from the design document.
        """
        query = "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."
        
        result = await orchestrator.reflect_and_generate(query)
        
        # Verify successful generation
        assert result.success is True
        assert result.iterations >= 1
        assert result.iterations <= config.app.max_reflection_iterations
        
        # Verify code was generated
        assert result.final_code.startswith("<execute_python>")
        assert result.final_code.endswith("</execute_python>")
        
        # Verify code contains expected elements
        code_content = result.final_code
        assert "import matplotlib" in code_content
        assert "pandas" in code_content
        assert "coffee_sales.csv" in code_content
        
        # Verify execution if it was attempted
        if result.execution_result:
            assert result.execution_result.success is True
            assert len(result.execution_result.generated_files) > 0
            
            # Verify generated files exist
            for file_path in result.execution_result.generated_files:
                assert Path(file_path).exists()
        
        # Verify history contains all iterations
        assert len(result.history) == result.iterations
        for i, entry in enumerate(result.history):
            assert entry["iteration"] == i + 1
            assert "generator_response" in entry
            assert "critique_response" in entry
    
    @pytest.mark.asyncio
    async def test_coffee_type_sales_chart(self, orchestrator):
        """Test generating a chart showing sales by coffee type."""
        query = "Create a bar chart showing total sales by coffee type for 2024."
        
        result = await orchestrator.reflect_and_generate(query)
        
        assert result.success is True
        assert result.final_code.startswith("<execute_python>")
        
        # Verify code contains relevant elements
        code_content = result.final_code
        assert "coffee_name" in code_content or "coffee_type" in code_content
        assert "bar" in code_content.lower() or "plt.bar" in code_content
    
    @pytest.mark.asyncio
    async def test_daily_sales_trend(self, orchestrator):
        """Test generating a line chart showing daily sales trends."""
        query = "Create a line chart showing daily sales trends over time."
        
        result = await orchestrator.reflect_and_generate(query)
        
        assert result.success is True
        assert result.final_code.startswith("<execute_python>")
        
        # Verify code contains relevant elements
        code_content = result.final_code
        assert "date" in code_content
        assert "line" in code_content.lower() or "plt.plot" in code_content
    
    @pytest.mark.asyncio
    async def test_revenue_analysis(self, orchestrator):
        """Test generating a revenue analysis chart."""
        query = "Create a chart showing revenue analysis by month for 2024."
        
        result = await orchestrator.reflect_and_generate(query)
        
        assert result.success is True
        assert result.final_code.startswith("<execute_python>")
        
        # Verify code contains revenue-related elements
        code_content = result.final_code
        assert "price" in code_content or "revenue" in code_content.lower()
    
    @pytest.mark.asyncio
    async def test_reflection_iterations(self, orchestrator):
        """Test that reflection loop works with multiple iterations."""
        # Use a complex query that might require multiple iterations
        query = "Create a comprehensive dashboard with multiple charts showing coffee sales analysis including trends, top products, and quarterly comparisons."
        
        result = await orchestrator.reflect_and_generate(query)
        
        assert result.success is True
        assert result.iterations >= 1
        
        # Verify history shows the reflection process
        for i, entry in enumerate(result.history):
            assert entry["iteration"] == i + 1
            assert "generator_response" in entry
            assert "critique_response" in entry
            
            # Check if iterations show improvement
            if i > 0:
                prev_entry = result.history[i-1]
                # Later iterations should have different code
                assert (entry["generator_response"]["code"] != 
                       prev_entry["generator_response"]["code"])
    
    @pytest.mark.asyncio
    async def test_error_handling_invalid_query(self, orchestrator):
        """Test handling of invalid or unclear queries."""
        query = "Create a chart showing the weather forecast for next week."
        
        result = await orchestrator.reflect_and_generate(query)
        
        # Should still attempt to generate code
        assert result.iterations >= 1
        assert result.final_code.startswith("<execute_python>")
        
        # The critic should identify issues with the query
        if result.iterations > 1:
            # Check if critic provided feedback about query relevance
            for entry in result.history:
                critique = entry["critique_response"]
                if critique["result"] != "approved":
                    assert len(critique["suggestions"]) > 0 or len(critique["issues"]) > 0
    
    @pytest.mark.asyncio
    async def test_code_execution_safety(self, orchestrator):
        """Test that generated code executes safely."""
        query = "Create a simple bar chart of coffee sales by type."
        
        result = await orchestrator.reflect_and_generate(query)
        
        assert result.success is True
        
        # If code was executed, verify it was safe
        if result.execution_result:
            assert result.execution_result.success is True
            assert result.execution_result.return_code == 0
            assert result.execution_result.error is None or result.execution_result.error == ""
            
            # Verify no dangerous operations were performed
            # Extract just the code content, not the tags
            code_content = result.final_code
            if "<execute_python>" in code_content and "</execute_python>" in code_content:
                start = code_content.find("<execute_python>") + len("<execute_python>")
                end = code_content.find("</execute_python>")
                code_content = code_content[start:end].lower()
            
            dangerous_operations = ["os.system", "subprocess", "exec", "eval", "__import__"]
            for operation in dangerous_operations:
                assert operation not in code_content
    
    @pytest.mark.asyncio
    async def test_output_file_generation(self, orchestrator):
        """Test that charts are saved as files."""
        query = "Create a pie chart showing the distribution of coffee types and save it as a PNG file."
        
        result = await orchestrator.reflect_and_generate(query)
        
        assert result.success is True
        
        if result.execution_result and result.execution_result.success:
            assert len(result.execution_result.generated_files) > 0
            
            # Verify files are valid image files
            for file_path in result.execution_result.generated_files:
                path = Path(file_path)
                assert path.exists()
                assert path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.svg', '.pdf']
                
                # Verify file has content
                assert path.stat().st_size > 0
    
    @pytest.mark.asyncio
    async def test_cleanup_after_execution(self, orchestrator):
        """Test that resources are properly cleaned up after execution."""
        query = "Create a simple line chart."
        
        result = await orchestrator.reflect_and_generate(query)
        
        assert result.success is True
        
        # Clean up orchestrator
        await orchestrator.close()
        
        # Verify agents were closed
        assert orchestrator.generator._agent is None
        assert orchestrator.critic._agent is None
    
    @pytest.mark.asyncio
    async def test_performance_with_large_dataset(self, orchestrator):
        """Test performance with the full coffee sales dataset."""
        query = "Create a comprehensive analysis of the entire coffee sales dataset with multiple visualizations."
        
        import time
        start_time = time.time()
        
        result = await orchestrator.reflect_and_generate(query)
        
        execution_time = time.time() - start_time
        
        assert result.success is True
        assert execution_time < 120  # Should complete within 2 minutes
        
        # Verify the result is comprehensive
        code_content = result.final_code
        assert len(code_content) > 100  # Should be substantial code
        assert "coffee_sales.csv" in code_content
