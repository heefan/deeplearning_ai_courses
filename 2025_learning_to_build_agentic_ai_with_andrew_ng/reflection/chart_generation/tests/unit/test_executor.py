"""
Unit tests for the Code Executor.

These tests verify the safe execution of Python code with proper
sandboxing and error handling.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, AsyncMock

from src.executor.code_executor import CodeExecutor, ExecutionResult


class TestCodeExecutor:
    """Test cases for the Code Executor."""
    
    @pytest.fixture
    def executor(self):
        """Create CodeExecutor instance for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield CodeExecutor(
                timeout=5,
                output_dir=temp_dir,
                allowed_imports=["matplotlib", "pandas", "numpy"]
            )
    
    def test_initialization(self, executor):
        """Test executor initialization."""
        assert executor.timeout == 5
        assert executor.allowed_imports == ["matplotlib", "pandas", "numpy"]
        assert executor.output_dir.exists()
    
    def test_extract_code_success(self, executor):
        """Test successful code extraction."""
        code_with_tags = """
        <execute_python>
        import matplotlib.pyplot as plt
        plt.plot([1, 2, 3])
        plt.show()
        </execute_python>
        """
        
        extracted = executor.extract_code(code_with_tags)
        
        assert "import matplotlib.pyplot as plt" in extracted
        assert "plt.plot([1, 2, 3])" in extracted
        assert extracted.strip().startswith("import")
    
    def test_extract_code_no_tags(self, executor):
        """Test code extraction with no tags."""
        code_without_tags = "import matplotlib.pyplot as plt"
        
        with pytest.raises(ValueError, match="No <execute_python> tags found"):
            executor.extract_code(code_without_tags)
    
    def test_extract_code_multiple_tags(self, executor):
        """Test code extraction with multiple tags."""
        code_with_multiple_tags = """
        <execute_python>code1</execute_python>
        <execute_python>code2</execute_python>
        """
        
        with pytest.raises(ValueError, match="Multiple <execute_python> tags found"):
            executor.extract_code(code_with_multiple_tags)
    
    def test_validate_imports_allowed(self, executor):
        """Test validation of allowed imports."""
        code = """
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        """
        
        # Should not raise exception
        executor._validate_imports(code)
    
    def test_validate_imports_disallowed(self, executor):
        """Test validation of disallowed imports."""
        code = """
        import os
        import sys
        """
        
        with pytest.raises(ValueError, match="Import 'os' not allowed"):
            executor._validate_imports(code)
    
    def test_validate_imports_from_import(self, executor):
        """Test validation of from imports."""
        code = """
        from matplotlib import pyplot
        from pandas import DataFrame
        """
        
        # Should not raise exception
        executor._validate_imports(code)
    
    def test_validate_imports_disallowed_from(self, executor):
        """Test validation of disallowed from imports."""
        code = """
        from os import path
        """
        
        with pytest.raises(ValueError, match="Import 'os' not allowed"):
            executor._validate_imports(code)
    
    @pytest.mark.asyncio
    async def test_execute_code_success(self, executor):
        """Test successful code execution."""
        code_with_tags = """
<execute_python>
import matplotlib.pyplot as plt
import numpy as np

# Create a simple plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title('Simple Sine Wave')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig('test_plot.png')
plt.close()
</execute_python>
"""
        
        result = await executor.execute_code(code_with_tags)
        
        assert isinstance(result, ExecutionResult)
        assert result.success is True
        assert result.return_code == 0
        assert result.error is None
        assert result.execution_time > 0
        assert len(result.generated_files) > 0
    
    @pytest.mark.asyncio
    async def test_execute_code_syntax_error(self, executor):
        """Test code execution with syntax error."""
        code_with_tags = """
<execute_python>
import matplotlib.pyplot as plt
plt.plot([1, 2, 3]  # Missing closing parenthesis
</execute_python>
"""
        
        result = await executor.execute_code(code_with_tags)
        
        assert result.success is False
        assert result.return_code != 0
        assert result.error is not None
        assert "SyntaxError" in result.error or "syntax" in result.error.lower()
    
    @pytest.mark.asyncio
    async def test_execute_code_runtime_error(self, executor):
        """Test code execution with runtime error."""
        code_with_tags = """
        <execute_python>
        import matplotlib.pyplot as plt
        # Try to access undefined variable
        plt.plot(undefined_variable)
        </execute_python>
        """
        
        result = await executor.execute_code(code_with_tags)
        
        assert result.success is False
        assert result.return_code != 0
        assert result.error is not None
        assert "NameError" in result.error or "undefined" in result.error.lower()
    
    @pytest.mark.asyncio
    async def test_execute_code_timeout(self, executor):
        """Test code execution timeout."""
        # Create executor with very short timeout
        short_executor = CodeExecutor(timeout=1, output_dir=executor.output_dir)
        
        code_with_tags = """
<execute_python>
import matplotlib.pyplot as plt
import numpy as np

# Create a very large dataset that will take time to process
x = np.linspace(0, 100000, 1000000)
y = np.sin(x)

# This should take longer than 1 second
for i in range(100000):
    y = y + np.sin(x * i / 1000)

plt.plot(x, y)
plt.savefig('large_plot.png')
</execute_python>
"""
        
        result = await short_executor.execute_code(code_with_tags)
        
        assert result.success is False
        assert "timed out" in result.error.lower()
        assert result.return_code == -1
    
    @pytest.mark.asyncio
    async def test_execute_code_disallowed_import(self, executor):
        """Test code execution with disallowed import."""
        code_with_tags = """
        <execute_python>
        import os  # This should be disallowed
        print("Hello")
        </execute_python>
        """
        
        result = await executor.execute_code(code_with_tags)
        
        assert result.success is False
        assert "not allowed" in result.error
    
    def test_find_generated_files(self, executor):
        """Test finding generated files."""
        # Create some test files
        test_files = ["plot1.png", "chart2.svg", "graph3.pdf"]
        for filename in test_files:
            (executor.output_dir / filename).touch()
        
        # Create a non-chart file
        (executor.output_dir / "data.txt").touch()
        
        generated_files = executor._find_generated_files()
        
        # Should find chart files but not text files
        assert len(generated_files) == 3
        for filename in test_files:
            assert any(filename in file for file in generated_files)
    
    @pytest.mark.asyncio
    async def test_execute_code_no_output(self, executor):
        """Test code execution that produces no output files."""
        code_with_tags = """
<execute_python>
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
# Don't save the plot
</execute_python>
"""
        
        result = await executor.execute_code(code_with_tags)
        
        assert result.success is True
        assert result.generated_files == []
    
    def test_extract_code_whitespace_handling(self, executor):
        """Test code extraction with various whitespace scenarios."""
        # Test with extra whitespace
        code_with_whitespace = """
<execute_python>
    
import matplotlib.pyplot as plt
    
plt.plot([1, 2, 3])
    
</execute_python>
"""
        
        extracted = executor.extract_code(code_with_whitespace)
        # The extracted code should contain the essential content
        assert "import matplotlib.pyplot as plt" in extracted
        assert "plt.plot([1, 2, 3])" in extracted
    
    def test_validate_imports_comments(self, executor):
        """Test import validation with comments."""
        code = """
        # This is a comment
        import matplotlib.pyplot as plt  # Another comment
        import pandas as pd
        """
        
        # Should not raise exception
        executor._validate_imports(code)
    
    def test_validate_imports_multiline(self, executor):
        """Test import validation with multiline imports."""
        code = """
        from matplotlib import (
            pyplot as plt,
            patches
        )
        """
        
        # Should not raise exception
        executor._validate_imports(code)
