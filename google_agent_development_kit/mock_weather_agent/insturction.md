Reference:  https://google.github.io/adk-docs/tutorials/agent-team/

ADK Weather Bot - Unified Project Structure
Supports both ADK CLI tools AND custom Python services

This unified structure allows you to:
1. Use `uv run adk web` for quick testing and development
2. Deploy as a custom Python service with FastAPI/Flask
3. Maintain the same core logic for both approaches
4. Scale from development to production seamlessly


```
weather_bot/
├── pyproject.toml              # uv project configuration
├── README.md                  # Documentation
├── .env.example               # Environment template
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
