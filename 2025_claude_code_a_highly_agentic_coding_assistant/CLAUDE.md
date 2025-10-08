# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains course materials for learning Claude Code, including a full-stack RAG (Retrieval-Augmented Generation) chatbot system in the `example_1/starting-ragchatbot-codebase/` directory.

## Key Architecture

### RAG Chatbot System (`example_1/starting-ragchatbot-codebase/`)

The system follows a modular Python architecture:

- **FastAPI Backend** (`backend/`): Main API server with endpoints for querying and course stats
- **Frontend** (`frontend/`): Static HTML/CSS/JS web interface
- **RAG System Core Components**:
  - `rag_system.py`: Main orchestrator that coordinates all components
  - `vector_store.py`: ChromaDB integration for semantic search
  - `ai_generator.py`: Anthropic Claude API integration
  - `document_processor.py`: Text chunking and course document parsing
  - `session_manager.py`: Conversation history management
  - `search_tools.py`: Tool-based search functionality

### Configuration
- All settings are centralized in `backend/config.py`
- Environment variables loaded from `.env` file
- Key config: Anthropic API key, embedding model, chunk sizes, ChromaDB path

## Development Commands

### Setup and Installation
```bash
# Install dependencies (uses uv package manager)
uv sync

# Set up environment
# Create .env file with ANTHROPIC_API_KEY=your_key_here
```

### Running the Application
```bash
# Quick start (from ragchatbot-codebase directory)
chmod +x run.sh
./run.sh

# Manual start
cd backend
uv run uvicorn app:app --reload --port 8000
```

### Key URLs
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Project Structure
- Uses `uv` for Python dependency management (pyproject.toml)
- ChromaDB for vector storage (persisted in `backend/chroma_db/`)
- Course documents stored in `docs/` directory
- FastAPI serves both API and static frontend files

## Development Notes

- The system auto-loads documents from `../docs` on startup
- Session management maintains conversation history (configurable limit)
- Vector embeddings use sentence-transformers with all-MiniLM-L6-v2 model
- CORS and trusted host middleware configured for development
- No-cache headers applied to static files for development
- always use uv to run the server, do not use pip
- use uv to manage all the dependencies