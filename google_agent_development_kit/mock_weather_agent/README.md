# Weather Bot - Unified ADK Project

A unified weather bot that supports both Google Agent Development Kit (ADK) CLI tools and custom Python services. This project demonstrates how to build an agent that can be used with `uv run adk web` for development and testing, while also being deployable as a custom FastAPI or Flask service.

## Features

- 🌤️ **Weather Information**: Get current weather conditions and forecasts
- 🔧 **ADK Integration**: Works seamlessly with `uv run adk web`
- 🚀 **Multiple Deployment Options**: FastAPI, Flask, and CLI services
- 🛡️ **Safety Features**: Input validation and safety callbacks
- 📦 **Unified Codebase**: Same core logic for all deployment methods

## Project Structure

```
weather_bot/
├── pyproject.toml              # uv project configuration
├── README.md                  # Documentation
├── env.example                # Environment template
├── .gitignore                 # Git ignore file
│
├── agent.py                   # ADK CLI entry point (for `adk web`)
├── tools.py                   # Tool implementations  
├── callbacks.py               # Safety callbacks
│
├── src/
│   └── weather_bot/           # Python package for custom services
│       ├── __init__.py
│       ├── core/              # Core business logic (shared)
│       │   ├── __init__.py
│       │   ├── agents.py      # Agent factory
│       │   ├── tools.py       # Tool implementations
│       │   ├── callbacks.py   # Safety callbacks
│       │   └── config.py      # Configuration
│       ├── adk_integration/   # ADK-specific code
│       │   ├── __init__.py
│       │   └── session.py     # Session management
│       └── services/          # Custom service implementations
│           ├── __init__.py
│           ├── fastapi_app.py # FastAPI service
│           ├── flask_app.py   # Flask service
│           └── cli.py         # Custom CLI
│
├── scripts/
│   ├── demo.py               # Standalone demo
│   ├── run_fastapi.py        # FastAPI server runner
│   ├── run_flask.py          # Flask server runner
│   └── deploy.py             # Deployment script
│
└── tests/
    ├── __init__.py
    ├── test_tools.py
    ├── test_agents.py
    └── test_services.py
```

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- [Google ADK](https://github.com/google/agent-development-kit)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd weather_bot
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment**:
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

### Usage

#### ADK CLI (Recommended for Development)

```bash
# Start the ADK web interface
uv run adk web

# Or run the agent directly
uv run python agent.py
```

#### Custom Services

**FastAPI Service**:
```bash
python scripts/run_fastapi.py
# API docs: http://localhost:8000/docs
```

**Flask Service**:
```bash
python scripts/run_flask.py
# Service: http://localhost:5000
```

**CLI Interface**:
```bash
# Interactive mode
python -m src.weather_bot.services.cli --interactive

# Single query
python -m src.weather_bot.services.cli --message "What's the weather in London?"
```

**Demo Script**:
```bash
python scripts/demo.py
```

## Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_weather_api_key_here

# Optional Configuration
MODEL_NAME=gpt-4
TEMPERATURE=0.7
MAX_TEMPERATURE=50.0
MIN_TEMPERATURE=-50.0
```

### API Keys

- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)
- **Weather API Key**: Get from [OpenWeatherMap](https://openweathermap.org/api)

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black .
uv run isort .
```

### Linting

```bash
uv run flake8 .
```

## API Reference

### Weather Tools

- `get_current_weather(location)`: Get current weather for a location
- `get_weather_forecast(location, days)`: Get weather forecast for a location

### Safety Callbacks

- `validate_weather_request()`: Validate weather request parameters
- `validate_temperature_data()`: Validate temperature data
- `sanitize_location_input()`: Sanitize location input

## Deployment

### Using the Deployment Script

```bash
python scripts/deploy.py
```

### Manual Deployment

1. **Install dependencies**:
   ```bash
   uv sync --production
   ```

2. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY=your_key
   export WEATHER_API_KEY=your_key
   ```

3. **Run the service**:
   ```bash
   # FastAPI
   uvicorn src.weather_bot.services.fastapi_app:app --host 0.0.0.0 --port 8000
   
   # Flask
   python -m src.weather_bot.services.flask_app
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Google Agent Development Kit](https://github.com/google/agent-development-kit)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [OpenAI API](https://platform.openai.com/) 