# Mock Weather Agent - Real world Example

This example is from Agent Development Kit tutorial - Quickstart 
[](https://google.github.io/adk-docs/get-started/quickstart)
[Build Your First Intelligent Agent Team: A Progressive Weather Bot with ADK](https://google.github.io/adk-docs/tutorials/agent-team/)



## Learning Objectives
To learn the following:

1. Agent application structure
2. Session and state management for different users and sessions
3. Deployment process

## Pre-Start Notes

1. Google's example is based on Jupyter, while my notes use a Python project to simulate a weather agent as a remote service.
2. `Google Agent adk web` usage conventions are different from Python projects.

>Topic: How to organize code so that it can be used for both remote services and `adk web` for development and debugging?
This document is written according to this goal.

ADK Weather Bot - Unified Project Structure
Supports both ADK CLI tools AND custom Python services

This unified structure allows you to:
1. Use `uv run adk web` for quick testing and development
2. Deploy as a custom Python service with FastAPI/Flask
3. Maintain the same core logic for both approaches
4. Scale from development to production seamlessly

## Project Structure

```
Project structure:
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



**Key Point 1: `adk web server` loading convention**
1. Direct Agent loading: adk web server enters your_agent directory, finds the `agent.py` file and runs this Agent.
2. Package-level Agent loading: In your_agent directory's `__init__.py`, specify the Agent name you want to export to the outside.
3. It must be called `root_agent`, otherwise loading will fail.


**Key Point 2: Docstrings are crucial for function calls**
Key Concept: Docstrings are Crucial! The agent's LLM relies heavily on the function's docstring to understand:

What the tool does.
When to use it.
What arguments it requires (city: str).
What information it returns.

Best Practice: Provide clear and specific instruction prompts. The more detailed the instructions, the better the LLM can understand its role and how to use its tools effectively. Be explicit about error handling if needed.

Best Practice: Choose descriptive name and description values. These are used internally by ADK and are vital for features like automatic delegation (covered later).

**Focus Points**
1. How does ADK automatically make decisions and call Tools, and what happens if the decision is wrong?


## A Little Rant
1. Google developers don't always write code very consistently - functions sometimes have parameters, sometimes they don't.
