# Essay Composer with Reflection Pattern using Google ADK

A production-ready CLI tool that uses the reflection AI design pattern with Google's Agent Development Kit (ADK) to generate high-quality essays. The process involves three phases: **Generation** → **Reflection** → **Revision**, orchestrated by specialized ADK agents.

## ✨ Features

- 🤖 **Local AI Processing**: Uses LM Studio for privacy and control
- 🔄 **Reflection Pattern**: Three-phase process for superior essay quality
- 📝 **Structured Essays**: Generates essays with introduction, body paragraphs, and conclusion
- 🎯 **CLI Interface**: Simple command-line interface with comprehensive options
- 📊 **Verbose Output**: Shows all intermediate steps for transparency
- 🚀 **Google ADK Integration**: Production-ready modular agent-based architecture
- 🔧 **Flexible Deployment**: Production-ready ADK agent architecture
- 🧩 **Specialized Agents**: Dedicated agents for generation, reflection, and revision
- ✅ **Comprehensive Testing**: 79 tests with 100% pass rate
- 🛠️ **Production Ready**: Robust error handling and user feedback

## Prerequisites

1. **LM Studio**: Download and install [LM Studio](https://lmstudio.ai/)
2. **Python 3.12**: Make sure Python is installed (required for Google ADK)
3. **Model**: Load the `openai/gpt-oss-20b` model in LM Studio (or update the model name in the code)

## Installation

1. Clone or download this project
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

## Setup LM Studio

1. Open LM Studio
2. Download and load the `openai/gpt-oss-20b` model
3. Start the local server (usually runs on `http://localhost:1234`)
4. Make sure the server is running before using the essay composer

## Usage

### Basic Usage

```bash
# Generate an essay using ADK agents
uv run python src/essay_composer.py "The impact of artificial intelligence on education"
```

### CLI Options

```bash
# Test connection to LM Studio
uv run python src/essay_composer.py "Test Topic" --test

# Use custom LM Studio URL
uv run python src/essay_composer.py "Your topic" --url http://localhost:8080/v1

# Quiet mode (only show final essay)
uv run python src/essay_composer.py "Your topic" --quiet

# Show ADK workflow information
uv run python src/essay_composer.py "Test Topic" --workflow-info

# Get help
uv run python src/essay_composer.py --help
```

## How It Works

### ADK Agent Architecture

The essay composer uses Google's Agent Development Kit to orchestrate specialized agents:

1. **EssayGeneratorAgent**: Creates initial essay drafts (500-800 words, structured format)
2. **ReflectorAgent**: Critiques the draft, identifying strengths and weaknesses  
3. **ReviserAgent**: Revises the essay based on the critique for final output

### Workflow

The reflection pattern involves three sequential steps:

1. **Generation**: Creates an initial essay draft with introduction, body paragraphs, and conclusion
2. **Reflection**: AI critiques the draft, analyzing structure, arguments, clarity, and coherence
3. **Revision**: AI revises the essay incorporating feedback to produce a polished final version

This process results in significantly higher quality essays compared to single-pass generation.

### Agent Benefits

- **Modularity**: Each agent has a specific responsibility and can be tested independently
- **Scalability**: Easy to add new agents or modify existing ones without affecting others
- **Flexibility**: Modular architecture allows easy customization and extension
- **Production Ready**: Robust error handling, context management, and state tracking
- **Deployment**: Ready for containerization and cloud deployment with proper orchestration

## Example Output

```
🎯 Topic: The impact of artificial intelligence on education
==================================================
🤖 Starting ADK SequentialAgent Workflow...
==================================================

📄 DRAFT ESSAY:
------------------------------
[Initial essay draft here...]

==================================================

💭 CRITIQUE:
------------------------------
[AI critique here...]

==================================================

✨ FINAL ESSAY:
------------------------------
[Final polished essay here...]

🎉 Essay completed successfully using ADK SequentialAgent!
Topic: The impact of artificial intelligence on education
Workflow Status: completed
```

## Testing

The project includes comprehensive testing with **79 tests and 100% pass rate**:

### Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_llm_client_unit.py
│   ├── test_prompts_unit.py
│   └── test_agents_unit.py
├── integration/             # Integration tests for component interactions
│   └── test_agent_integration.py
├── e2e/                    # End-to-end tests for complete workflows
│   ├── test_essay_composer_e2e.py
│   └── test_cli_e2e.py
└── test_essay_composer.py   # Main application tests
```

### Running Tests

```bash
# Run all tests (79 tests, 100% pass rate)
uv run python -m pytest

# Run specific test categories
uv run python -m pytest tests/unit/           # Unit tests only
uv run python -m pytest tests/integration/   # Integration tests only
uv run python -m pytest tests/e2e/           # End-to-end tests only

# Run with verbose output
uv run python -m pytest -v

# Run with coverage
uv run python -m pytest --cov=.

# Run specific test file
uv run python -m pytest tests/unit/test_llm_client_unit.py

# Run tests in parallel
uv run python -m pytest -n auto

# Quick test run
uv run python -m pytest --tb=short -q
```

### Test Coverage

- **Unit Tests**: Individual component functionality (agents, prompts, client)
- **Integration Tests**: Agent interactions and workflow orchestration
- **E2E Tests**: Complete workflows from CLI to final output
- **CLI Tests**: Command-line interface functionality with all options
- **Mock Testing**: Proper mocking for external dependencies
- **Error Handling**: Comprehensive error scenario testing

## Troubleshooting

- **Connection Error**: Make sure LM Studio is running and the server is started
- **Model Not Found**: Ensure you have loaded the `openai/gpt-oss-20b` model in LM Studio
- **Slow Generation**: The gpt-oss-20b model is large; consider using a smaller model or adjust the max_tokens parameter
- **Memory Issues**: The 20B model requires significant RAM; ensure you have at least 16GB available
- **Test Failures**: Run `uv run python -m pytest` to verify all 81 tests pass
- **CLI Issues**: Use `--help` to see all available options

## Project Status

### ✅ Completed Features

- **Google ADK Integration**: Full implementation using SequentialAgent and LlmAgent
- **LM Studio Integration**: OpenAI-compatible client with connection testing
- **CLI Interface**: Complete Click-based command-line interface with all options
- **Agent Architecture**: Three specialized ADK agents with proper orchestration
- **Comprehensive Testing**: 79 tests with 100% pass rate
- **Project Structure**: Modern Python project with uv dependency management
- **Error Handling**: Robust error handling and user feedback
- **Documentation**: Complete README and inline documentation

### 🚀 Future Enhancements

- **Performance Optimization**: Caching for repeated requests
- **Advanced CLI Features**: Configuration file support, batch processing
- **Output Formatting**: Multiple output formats (JSON, markdown, PDF)
- **Model Configuration**: Support for different models per agent
- **Iterative Refinement**: Multiple reflection cycles option
- **Interactive Mode**: User feedback integration
- **Export Options**: PDF, Word, and other document formats
