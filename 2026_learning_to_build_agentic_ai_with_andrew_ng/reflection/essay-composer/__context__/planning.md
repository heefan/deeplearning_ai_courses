# Planning 

Requirment: 
1. use local LM Studio
2. use CLI commandline in python 
3. use google adk framework

# Essay Composer with Reflection Pattern

## Architecture Overview

The reflection pattern involves two main phases:

1. **Generation Phase**: Generate an initial essay draft
2. **Reflection Phase**: Critique the draft and produce an improved final version

## Implementation Structure

### Core Components

**`essay_composer.py`** - Main CLI application

- Accept topic input from command line arguments
- Orchestrate the reflection workflow
- Output the final essay

**`llm_client.py`** - LM Studio integration

- Connect to local LM Studio API (OpenAI-compatible)
- Handle prompt formatting and API calls
- Default endpoint: `http://localhost:1234/v1`

**`prompts.py`** - Prompt templates

- **Generator prompt**: Create initial essay draft with intro, body, conclusion
- **Reflector prompt**: Critique the draft (coherence, arguments, structure, clarity)
- **Revision prompt**: Generate final essay based on draft + critique

**`requirements.txt`** - Dependencies

- `openai` (for LM Studio API compatibility)
- `click` or `argparse` (CLI interface)

## Workflow

```
Topic Input → Generator → Draft Essay → Reflector → Critique → Revisor → Final Essay
```

1. User provides essay topic via CLI
2. Generator creates initial draft (intro, body, conclusion)
3. Reflector analyzes draft and provides critique
4. Revisor produces final essay incorporating feedback
5. Display final essay to stdout

## Key Design Decisions

- **Single model**: Use same LM Studio model for all phases
- **Simple structure**: Standard essay format (intro, body, conclusion)
- **Automatic processing**: No user interaction during generation
- **Verbose output**: Show draft, critique, and final essay for transparency

## Future Enhancement Questions

Document these options for future iterations:

1. **Reflection iterations**: Single vs multiple cycles vs configurable
2. **Model configuration**: Single model vs separate models for generation/reflection
3. **Essay structure**: Simple vs structured vs flexible formats
4. **CLI interaction**: Automatic vs interactive vs verbose modes

### To-dos

- [x] Create project structure with requirements.txt and configuration files
- [x] Build LM Studio API client wrapper for model calls
- [x] Design and implement generator, reflector, and revisor prompt templates
- [x] Implement main CLI application with argument parsing and workflow orchestration
- [x] Test end-to-end workflow with LM Studio
- [x] Configure for openai/gpt-oss-20b model
