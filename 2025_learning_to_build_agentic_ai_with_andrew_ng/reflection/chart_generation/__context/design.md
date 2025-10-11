# Chart Generation Agent with Reflection Pattern

## Overview

Create a Google Agent ADK application that generates Python matplotlib code to visualize coffee sales data based on user queries. The system implements the reflection design pattern where a generator agent creates code and a critic agent reviews/improves it iteratively.

## Technical Stack

1. **Google Agent ADK** - https://github.com/google/adk-python (latest version)
2. **Reflection AI Design Pattern** - Generator-Critic iterative improvement loop
3. **LMStudio (gpt-oss-20b)** - Local model for agent reasoning
4. **Matplotlib** - Chart generation library
5. **Pandas** - Data processing
6. **Pytest** - Comprehensive testing framework
7. **uv** - dependency managements
8. **cli** - applicaiton 

## User Requirements
s
1. Given the `coffee_sales.csv` file 
2. Generate Python code to display charts based on user requirements
3. Implement reflection pattern for code quality improvement
4. Support safe code execution with validation

## Architecture

### Core Components

1. **Generator Agent** - Creates initial Python chart code based on user queries
2. **Critic Agent** - Reviews generated code for correctness, best practices, and requirements adherence
3. **Executor** - Safely executes the generated Python code
4. **Orchestrator** - Manages the reflection loop (generate → critique → refine)

### Project Structure

```
chart_generation/
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── generator.py      # Code generation agent
│   │   ├── critic.py          # Code critique agent
│   │   └── orchestrator.py    # Reflection loop manager
│   ├── executor/
│   │   ├── __init__.py
│   │   └── code_executor.py   # Safe Python code execution
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_schema.py     # CSV schema parser
│   │   └── prompt_templates.py # Agent prompts
│   └── config.py               # LMStudio configuration
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_generator.py
│   │   ├── test_critic.py
│   │   ├── test_executor.py
│   │   └── test_data_schema.py
│   └── e2e/
│       ├── __init__.py
│       ├── test_reflection_flow.py
│       └── test_chart_generation.py
├── coffee_sales.csv
├── pyproject.toml
├── README.md
└── .env.example
```

## Implementation Details

### 1. Configuration (`src/config.py`)
- LMStudio API endpoint configuration (default: http://localhost:1234/v1)
- Model name: gpt-oss-20b
- ADK client initialization
- Max reflection iterations (default: 3)

### 2. Data Schema Parser (`src/utils/data_schema.py`)
- Parse coffee_sales.csv headers: date, time, cash_type, card, price, coffee_name
- Generate schema description for LLM context
- Data validation utilities

### 3. Generator Agent (`src/agents/generator.py`)
- ADK agent that generates matplotlib code
- Input: user query + data schema
- Output: Python code wrapped in `<execute_python>` tags
- Prompt includes: dataset schema, matplotlib best practices, Q1 definition (Jan-Mar)

### 4. Critic Agent (`src/agents/critic.py`)
- ADK agent that reviews generated code
- Checks: syntax errors, data correctness, chart clarity, requirements coverage
- Output: critique with specific improvement suggestions or approval
- Uses structured output format for parsing

### 5. Orchestrator (`src/agents/orchestrator.py`)
- Implements reflection loop:
  1. Call generator with user query
  2. Call critic to review code
  3. If approved: extract and return code
  4. If not approved: regenerate with critique feedback
  5. Repeat up to max iterations
- Handles iteration limits and fallback behavior

### 6. Code Executor (`src/executor/code_executor.py`)
- Extracts code from `<execute_python>` tags
- Executes in restricted environment (exec with controlled globals)
- Captures matplotlib figures
- Error handling and timeout protection

### 7. Testing Strategy

#### Unit Tests (`tests/unit/`)
- `test_generator.py`: Mock LLM responses, verify prompt construction, code extraction
- `test_critic.py`: Test critique logic, approval/rejection scenarios
- `test_executor.py`: Code extraction, execution safety, error handling
- `test_data_schema.py`: CSV parsing, schema generation

#### E2E Tests (`tests/e2e/`)
- `test_reflection_flow.py`: Full generator→critic→regenerate cycle with mocked LLM
- `test_chart_generation.py`: Real query execution (requires LMStudio running)
  - Test case: "Create a plot comparing Q1 coffee sales in 2024 and 2025"
  - Verify: code generated, executed successfully, chart saved

### 8. Dependencies (`pyproject.toml`)
- google-adk-python (latest)
- matplotlib
- pandas
- pytest
- pytest-asyncio
- python-dotenv

## Test Coverage Goals
- Unit tests: >80% code coverage
- E2E tests: Cover main user workflows including reflection cycles
- Mock LLM calls in unit tests for speed and reliability
- Optional E2E tests with real LMStudio (marked with pytest markers)

## Example Use Case

**Query**: "Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv."

**Process**:
1. Generator creates initial matplotlib code
2. Critic reviews for data accuracy, chart clarity, Q1 definition
3. If approved: extract and execute code
4. If not approved: regenerate with feedback
5. Repeat up to 3 iterations

**Output**: Python code wrapped in `<execute_python>` tags for safe execution

## Implementation Plan

### Phase 1: Foundation
- [ ] Create project structure with pyproject.toml, dependencies, and README
- [ ] Implement LMStudio configuration and ADK client initialization
- [ ] Build CSV schema parser and data utilities

### Phase 2: Core Agents
- [ ] Implement safe Python code executor with tag extraction
- [ ] Create generator agent with prompt templates and ADK integration
- [ ] Create critic agent for code review and feedback

### Phase 3: Reflection System
- [ ] Implement reflection loop orchestrator managing generator-critic cycle
- [ ] Add error handling and iteration limits

### Phase 4: Testing
- [ ] Write unit tests for all components with mocked dependencies
- [ ] Write E2E tests for full reflection workflow and chart generation
- [ ] Add integration tests with real LMStudio

