# RAG System Flow Diagram

```
┌─────────────────┐
│   User Query    │
│   (Frontend)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│                     (app.py)                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  RAG System                                 │
│                (rag_system.py)                              │
│  ┌─────────────────┬──────────────────┬──────────────────┐  │
│  │                 │                  │                  │  │
│  ▼                 ▼                  ▼                  ▼  │
│ Session         Vector Store      Document           Search │
│ Manager         (ChromaDB)        Processor          Tools  │
│                                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Semantic Search Results                        │
│           (Retrieved course chunks)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                AI Generator                                 │
│            (Anthropic Claude)                               │
│                                                             │
│  Context: Query + Retrieved Chunks + Session History        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Generated Response                             │
│        (Answer + Sources + Session ID)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                Frontend Display                             │
│            (HTML/CSS/JavaScript)                            │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Data Flow
1. **User Query** → FastAPI endpoint `/api/query`
2. **Session Management** → Create/retrieve conversation history
3. **Vector Search** → ChromaDB semantic search on course chunks
4. **Context Assembly** → Combine query + retrieved docs + history
5. **AI Generation** → Claude generates response with sources
6. **Response Delivery** → JSON response with answer, sources, session_id

### Document Ingestion Flow
```
Course Documents (docs/) 
          │
          ▼
Document Processor
    (chunking)
          │
          ▼
Vector Store (ChromaDB)
    (embeddings)
          │
          ▼
Search Tools
(semantic search)
```

### Key Technologies
- **FastAPI**: Web framework and API server
- **ChromaDB**: Vector database for semantic search
- **sentence-transformers**: Embedding model (all-MiniLM-L6-v2)
- **Anthropic Claude**: AI generation (claude-sonnet-4-20250514)
- **uv**: Python package management