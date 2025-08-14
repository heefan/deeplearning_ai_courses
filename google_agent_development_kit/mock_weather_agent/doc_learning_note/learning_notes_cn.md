# Mock Weather Agent - Real world Example

This example is from Agent Development Kit tutorial - Quickstart 
[](https://google.github.io/adk-docs/get-started/quickstart)
[Build Your First Intelligent Agent Team: A Progressive Weather Bot with ADK](https://google.github.io/adk-docs/tutorials/agent-team/)



## 学习目标
to learn the followings, 

1. agent application structure. 
2. session and state for different users and sessions
2. deployment process

## 开始前说明

1. Google的例子是按照Jupyter来做的，而我的笔记是使用python项目模拟weather agent成一个远程服务。
2. `Google Agent adk web`使用规范和python项目不同。

>Topic: 怎么组织代码，使得该代码既可以用于Remote service，又可以使用`adk web`做开发调试？
本文按照这个目标来编写代码。

ADK Weather Bot - Unified Project Structure
Supports both ADK CLI tools AND custom Python services

This unified structure allows you to:
1. Use `uv run adk web` for quick testing and development
2. Deploy as a custom Python service with FastAPI/Flask
3. Maintain the same core logic for both approaches
4. Scale from development to production seamlessly

## 程序结构

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



**知识点 1: `adk web server` loading convention **
1. 直接Agent载入：adk web server 是进入your_agent目录，找到`agent.py`这个文件并且运行这个Agent。
2. Package-level Agent载入： 在your_agent目录的`__init__.py`中指定你要导出给外部的Agent名称。
3. 必须是叫做`root_agent`，否则载入失败。 


**知识点2: Docstrings 是function call的关键**
Key Concept: Docstrings are Crucial! The agent's LLM relies heavily on the function's docstring to understand:

What the tool does.
When to use it.
What arguments it requires (city: str).
What information it returns.

Best Practice: Provide clear and specific instruction prompts. The more detailed the instructions, the better the LLM can understand its role and how to use its tools effectively. Be explicit about error handling if needed.

Best Practice: Choose descriptive name and description values. These are used internally by ADK and are vital for features like automatic delegation (covered later).

**关注点**
1. ADK是怎么自动进行决定和调用Tools的，如果决定错误怎么办？


## A Little Rant
1. Google developer 写代码也不太规范，function有时候带参数，有时候不带。

