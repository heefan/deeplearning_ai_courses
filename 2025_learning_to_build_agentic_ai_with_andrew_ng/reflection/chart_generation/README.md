# Chart Generation Agent with Reflection Pattern

A Google Agent ADK CLI application that generates Python matplotlib code to visualize coffee sales data using the reflection AI design pattern. Provides both command-line interface and programmatic API.

## Overview

This project implements a sophisticated agent system that uses the reflection pattern to generate high-quality Python code for data visualization. The system consists of:

- **Generator Agent**: Creates initial Python chart code based on user queries
- **Critic Agent**: Reviews and provides feedback on generated code
- **Orchestrator**: Manages the iterative reflection loop
- **Code Executor**: Safely executes the generated Python code

## Features

- 🤖 **Reflection AI Pattern**: Generator-Critic iterative improvement loop
- 🔒 **Safe Code Execution**: Restricted environment with timeout protection
- 📊 **Data Schema Awareness**: Automatic CSV schema parsing and validation
- 🧪 **Comprehensive Testing**: Unit tests with mocks + E2E tests with real LMStudio
- ⚡ **Local Model Support**: LMStudio integration with gpt-oss-20b
- 🛠️ **Modern Tooling**: uv for dependency management, pytest for testing
- 💻 **CLI Interface**: Beautiful command-line interface with Rich terminal output

## Quick Start

### Prerequisites

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) for dependency management
- [LMStudio](https://lmstudio.ai/) with gpt-oss-20b model running locally

### Installation

1. **Clone and setup the project:**
   ```bash
   git clone <repository-url>
   cd chart_generation
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your LMStudio settings
   ```

3. **Start LMStudio:**
   - Launch LMStudio
   - Load the gpt-oss-20b model
   - Start the local server (default: http://localhost:1234)

### Usage

#### CLI Interface (Recommended)

```bash
# Generate a chart with a simple query
chart-gen generate "Create a plot comparing Q1 coffee sales in 2024 and 2025"

# Use custom CSV file and output directory
chart-gen generate "Create a bar chart of sales by coffee type" \
  --csv-file my_data.csv \
  --output-dir ./charts

# Analyze your dataset
chart-gen analyze coffee_sales.csv

# Show configuration
chart-gen config-info

# Show example queries
chart-gen examples

# Verbose output for debugging
chart-gen generate "Create a comprehensive sales analysis" --verbose
```

#### Programmatic Usage

```python
from src.agents.orchestrator import ReflectionOrchestrator
from src.agents.generator import GeneratorAgent
from src.agents.critic import CriticAgent
from src.executor.code_executor import CodeExecutor
from src.utils.data_schema import DataSchema
from src.config import config

# Initialize components
data_schema = DataSchema("coffee_sales.csv")
model_config = config.get_model_config()

generator = GeneratorAgent(model_config, data_schema)
critic = CriticAgent(model_config)
executor = CodeExecutor()
orchestrator = ReflectionOrchestrator(generator, critic, executor)

# Generate chart code
result = await orchestrator.reflect_and_generate(
    "Create a plot comparing Q1 coffee sales in 2024 and 2025"
)

if result.success:
    print(f"Generated code after {result.iterations} iterations:")
    print(result.final_code)
    
    if result.execution_result:
        print(f"Generated files: {result.execution_result.generated_files}")
```

## Project Structure

```
chart_generation/
├── src/                          # Source code
│   ├── agents/                   # ADK agents
│   │   ├── generator.py         # Code generation agent
│   │   ├── critic.py            # Code critique agent
│   │   └── orchestrator.py     # Reflection loop manager
│   ├── cli/                     # CLI interface
│   │   └── main.py             # Command-line interface
│   ├── executor/                # Code execution
│   │   └── code_executor.py    # Safe Python execution
│   ├── utils/                   # Utilities
│   │   ├── data_schema.py      # CSV schema parser
│   │   └── prompt_templates.py # Agent prompts
│   └── config.py               # Configuration
├── tests/                       # Test suite
│   ├── unit/                   # Unit tests (mocked)
│   └── e2e/                    # E2E tests (real LMStudio)
├── coffee_sales.csv            # Sample dataset
├── pyproject.toml             # Project configuration
├── .cursorrules               # Cursor IDE rules
└── README.md                  # This file
```

## Testing

### Unit Tests (Fast, Mocked)
```bash
# Run all unit tests
uv run pytest tests/unit/

# Run with coverage
uv run pytest tests/unit/ --cov=src --cov-report=html
```

### E2E Tests (Requires LMStudio)
```bash
# Run E2E tests (requires LMStudio running)
uv run pytest tests/e2e/ -m e2e

# Skip E2E tests
uv run pytest -m "not e2e"
```

### All Tests
```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src --cov-report=term-missing --cov-report=html
```

## Configuration

### Environment Variables

Create a `.env` file with the following settings:

```env
# LMStudio Configuration
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL=gpt-oss-20b
LMSTUDIO_API_KEY=your-api-key-here

# ADK Configuration
ADK_PROJECT_ID=your-project-id
ADK_LOCATION=us-central1

# Application Settings
MAX_REFLECTION_ITERATIONS=3
CODE_EXECUTION_TIMEOUT=30
CHART_OUTPUT_DIR=./outputs

# Development Settings
DEBUG=false
LOG_LEVEL=INFO
```

### LMStudio Setup

1. Download and install [LMStudio](https://lmstudio.ai/)
2. Download the gpt-oss-20b model
3. Start the local server:
   - Model: gpt-oss-20b
   - Server URL: http://localhost:1234
   - API format: OpenAI compatible

## Development

### Code Style

This project uses modern Python tooling:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast linting
- **MyPy**: Type checking

```bash
# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

### Adding New Features

1. **Agents**: Add new agent types in `src/agents/`
2. **Executors**: Extend execution capabilities in `src/executor/`
3. **Utils**: Add utilities in `src/utils/`
4. **Tests**: Add corresponding tests in `tests/`

### Testing Guidelines

- **Unit Tests**: Mock all external dependencies (ADK, LMStudio)
- **E2E Tests**: Use real LMStudio for integration testing
- **Coverage**: Maintain >80% code coverage
- **Performance**: E2E tests should complete within reasonable time

## Architecture

### Reflection Pattern

The system implements the reflection AI design pattern:

1. **Generate**: Generator agent creates initial code
2. **Critique**: Critic agent reviews the code
3. **Reflect**: If not approved, regenerate with feedback
4. **Iterate**: Repeat up to max iterations
5. **Execute**: Run the final approved code

### Safety Features

- **Code Extraction**: Safely extract code from `<execute_python>` tags
- **Import Validation**: Only allow safe imports (matplotlib, pandas, numpy)
- **Timeout Protection**: Prevent infinite loops
- **Sandboxed Execution**: Run code in restricted environment
- **Error Handling**: Graceful failure with detailed error messages

## Example Use Cases

### CLI Examples

```bash
# Q1 Sales Comparison
chart-gen generate "Create a plot comparing Q1 coffee sales in 2024 and 2025"

# Coffee Type Analysis
chart-gen generate "Create a bar chart showing sales by coffee type"

# Revenue Trends
chart-gen generate "Create a line chart showing daily revenue trends"

# Comprehensive Analysis
chart-gen generate "Create a comprehensive dashboard with multiple charts showing coffee sales analysis" --verbose

# Custom Dataset
chart-gen generate "Create a pie chart of sales distribution" --csv-file my_data.csv --output-dir ./results
```

### Programmatic Examples

```python
# Q1 Sales Comparison
query = "Create a plot comparing Q1 coffee sales in 2024 and 2025"
result = await orchestrator.reflect_and_generate(query)

# Coffee Type Analysis
query = "Create a bar chart showing sales by coffee type"
result = await orchestrator.reflect_and_generate(query)

# Revenue Trends
query = "Create a line chart showing daily revenue trends"
result = await orchestrator.reflect_and_generate(query)
```

## Troubleshooting

### Common Issues

1. **LMStudio Connection Failed**
   - Ensure LMStudio is running
   - Check the base URL in configuration
   - Verify the model is loaded

2. **Code Execution Timeout**
   - Increase `CODE_EXECUTION_TIMEOUT` in configuration
   - Check for infinite loops in generated code

3. **Import Errors**
   - Ensure all dependencies are installed: `uv sync`
   - Check allowed imports in executor configuration

4. **Test Failures**
   - Unit tests should pass without LMStudio
   - E2E tests require LMStudio running
   - Check test markers: `pytest -m "not e2e"`

### Debug Mode

Enable debug logging:

```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Agent ADK for the agent framework
- LMStudio for local model hosting
- The reflection AI pattern for iterative improvement
- The coffee sales dataset for testing scenarios
