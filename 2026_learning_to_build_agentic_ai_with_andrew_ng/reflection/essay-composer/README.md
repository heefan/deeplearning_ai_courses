# Essay Composer with Reflection Pattern using Google ADK

A CLI tool that uses the reflection AI design pattern with Google's Agent Development Kit (ADK) to generate high-quality essays. The process involves three phases: **Generation** → **Reflection** → **Revision**, orchestrated by specialized ADK agents.

## Features

- 🤖 Uses local LM Studio for AI processing
- 🔄 Implements reflection pattern for improved essay quality
- 📝 Generates structured essays (introduction, body, conclusion)
- 🎯 Simple CLI interface
- 📊 Verbose output showing all intermediate steps
- 🚀 **Google ADK Integration**: Modular agent-based architecture
- 🔧 **Flexible Deployment**: Support for both ADK and legacy modes
- 🧩 **Specialized Agents**: Dedicated agents for generation, reflection, and revision

## Prerequisites

1. **LM Studio**: Download and install [LM Studio](https://lmstudio.ai/)
2. **Python 3.9+**: Make sure Python is installed (required for Google ADK)
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
# Using ADK agents (default)
uv run essay_composer.py "The impact of artificial intelligence on education"

# Using legacy mode (without ADK)
uv run essay_composer.py "Your topic" --legacy
```

### Options

```bash
# Test connection to LM Studio
uv run essay_composer.py --test

# Use custom LM Studio URL
uv run essay_composer.py "Your topic" --url http://localhost:8080/v1

# Quiet mode (only show final essay)
uv run essay_composer.py "Your topic" --quiet

# Show ADK workflow information
uv run essay_composer.py --workflow-info

# Use legacy composition method
uv run essay_composer.py "Your topic" --legacy
```

## How It Works

### ADK Agent Architecture

The essay composer uses Google's Agent Development Kit to orchestrate specialized agents:

1. **EssayGeneratorAgent**: Creates initial essay drafts
2. **ReflectorAgent**: Critiques the draft, identifying strengths and weaknesses  
3. **ReviserAgent**: Revises the essay based on the critique

### Workflow

The reflection pattern involves three steps:

1. **Generation**: Creates an initial essay draft
2. **Reflection**: AI critiques the draft, identifying strengths and weaknesses
3. **Revision**: AI revises the essay based on the critique

This process results in higher quality essays compared to single-pass generation.

### Agent Benefits

- **Modularity**: Each agent has a specific responsibility
- **Scalability**: Easy to add new agents or modify existing ones
- **Flexibility**: Can run in ADK mode or fallback to legacy mode
- **Deployment**: Ready for containerization and cloud deployment

## Example Output

```
🎯 Topic: The impact of artificial intelligence on education
==================================================
📝 Generating initial draft...

📄 DRAFT ESSAY:
------------------------------
[Initial essay draft here...]

==================================================
🔍 Reflecting on the draft...

💭 CRITIQUE:
------------------------------
[AI critique here...]

==================================================
✏️  Revising essay based on feedback...

✨ FINAL ESSAY:
------------------------------
[Final polished essay here...]

🎉 Essay completed successfully!
```

## Testing

The project includes comprehensive unit, integration, and end-to-end tests:

### Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_llm_client_unit.py
│   ├── test_prompts_unit.py
│   └── test_agents_unit.py
├── integration/             # Integration tests for component interactions
│   └── test_agent_integration.py
└── e2e/                    # End-to-end tests for complete workflows
    ├── test_essay_composer_e2e.py
    └── test_cli_e2e.py
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/unit/           # Unit tests only
uv run pytest tests/integration/   # Integration tests only
uv run pytest tests/e2e/           # End-to-end tests only

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=.

# Run specific test file
uv run pytest tests/unit/test_llm_client_unit.py

# Run tests in parallel
uv run pytest -n auto
```

### Test Coverage

- **Unit Tests**: Individual component functionality
- **Integration Tests**: Agent interactions and workflow orchestration
- **E2E Tests**: Complete workflows from CLI to final output
- **CLI Tests**: Command-line interface functionality

## Troubleshooting

- **Connection Error**: Make sure LM Studio is running and the server is started
- **Model Not Found**: Ensure you have loaded the `openai/gpt-oss-20b` model in LM Studio
- **Slow Generation**: The gpt-oss-20b model is large; consider using a smaller model or adjust the max_tokens parameter
- **Memory Issues**: The 20B model requires significant RAM; ensure you have at least 16GB available

## Future Enhancements

- Multiple reflection cycles
- Different models for generation vs reflection
- Custom essay structures
- Interactive mode for user feedback
- Export options (PDF, Word, etc.)
