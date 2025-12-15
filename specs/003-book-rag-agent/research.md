# Research: Book RAG Agent

**Feature Branch**: `003-book-rag-agent`
**Date**: 2025-12-15
**Status**: Complete

## Research Summary

This document captures technical decisions and research findings for implementing the BookRAGAgent.

---

## 1. OpenAI Agent SDK with Gemini Provider

### Decision
Use **OpenAI Agents SDK** with **LiteLLM** integration to support Gemini as the model provider.

### Rationale
- OpenAI Agents SDK provides a clean, standardized interface for building agents
- LiteLLM acts as a unified abstraction layer supporting multiple LLM providers including Gemini
- The pattern `litellm/gemini/gemini-2.0-flash` allows seamless Gemini integration
- Function tools use the `@function_tool` decorator for clean definition

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Google ADK (Agent Development Kit) | Less mature, fewer community examples |
| Direct Gemini API | No agent framework, would require building from scratch |
| LangChain | Heavier dependency, more abstraction than needed |

### Implementation Pattern
```python
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

agent = Agent(
    name="BookRAGAgent",
    instructions="...",
    model=LitellmModel(
        model="gemini/gemini-2.0-flash",
        api_key=os.environ["GEMINI_API_KEY"]
    ),
    tools=[retrieval_tool]
)
```

---

## 2. Cohere Embeddings

### Decision
Use **Cohere embed-english-v3.0** model with `input_type="search_query"` for queries.

### Rationale
- Cohere embed-english-v3.0 produces 1024-dimensional vectors
- The `input_type` parameter optimizes embeddings for search scenarios:
  - `search_document`: For documents being indexed
  - `search_query`: For user queries (optimized for matching)
- Constitution specifies 1536-dimensional embeddings; need to verify existing Qdrant collection schema

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| OpenAI text-embedding-3-small | Would require re-embedding existing content |
| Sentence Transformers | Less accurate for semantic search than Cohere |
| Cohere embed-v4.0 | May not match existing embeddings in Qdrant |

### Implementation Pattern
```python
import cohere

co = cohere.Client(api_key=os.environ["COHERE_API_KEY"])

response = co.embed(
    texts=[query],
    model="embed-english-v3.0",
    input_type="search_query",
    embedding_types=["float"]
)
query_embedding = response.embeddings.float[0]
```

### Key Consideration
**CRITICAL**: Must verify the embedding model and dimensions used in the existing Qdrant collection to ensure compatibility.

---

## 3. Qdrant Vector Search

### Decision
Use **qdrant-client** Python library with `query_points` method for vector similarity search.

### Rationale
- Official Qdrant Python client with full feature support
- Supports both sync and async operations
- `query_points` method provides clean interface for similarity search
- Can include score threshold filtering

### Implementation Pattern
```python
from qdrant_client import QdrantClient

client = QdrantClient(
    host=os.environ["QDRANT_HOST"],
    port=int(os.environ["QDRANT_PORT"])
)

results = client.query_points(
    collection_name=os.environ["QDRANT_COLLECTION"],
    query=query_embedding,
    limit=5,
    with_payload=True
)
```

### Metadata Retrieval
- Chunks include `chapter`, `section`, and `source` fields in payload
- `with_payload=True` ensures metadata is returned with results

---

## 4. Function Tool Design

### Decision
Create a single `retrieve_book_context` function tool using `@function_tool` decorator.

### Rationale
- OpenAI Agents SDK uses `@function_tool` decorator for tool definition
- Single retrieval function keeps the agent focused
- Tool returns formatted context string for injection into agent prompt

### Implementation Pattern
```python
from agents import function_tool

@function_tool
def retrieve_book_context(query: str) -> str:
    """Retrieve relevant context from the book for answering the query.

    Args:
        query: The user's question about the book content.

    Returns:
        Relevant text excerpts from the book with source citations.
    """
    # 1. Generate embedding for query
    # 2. Search Qdrant for similar chunks
    # 3. Format and return context with metadata
    ...
```

---

## 5. UV Package Manager

### Decision
Use **UV** for Python project and dependency management inside `agent/` directory.

### Rationale
- UV is fast, modern Python package manager
- Supports lockfiles for reproducible builds
- Compatible with pyproject.toml standard
- Recommended by project constraints

### Project Setup
```bash
cd agent
uv init
uv add openai-agents cohere qdrant-client python-dotenv litellm
```

---

## 6. Environment Configuration

### Decision
Use **python-dotenv** with `.env` file for configuration management.

### Required Environment Variables
| Variable | Purpose |
|----------|---------|
| `GEMINI_API_KEY` | Gemini model API authentication |
| `COHERE_API_KEY` | Cohere embedding API authentication |
| `QDRANT_HOST` | Qdrant server hostname |
| `QDRANT_PORT` | Qdrant server port |
| `QDRANT_COLLECTION` | Collection name for book embeddings |

### Implementation Pattern
```python
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
COHERE_API_KEY = os.environ["COHERE_API_KEY"]
```

---

## 7. Agent Instructions Design

### Decision
Embed strict instructions directly in agent definition to enforce book-only responses.

### System Prompt Template
```
You are BookRAGAgent, a specialized assistant that answers questions ONLY using content from the Physical AI & Humanoid Robotics textbook.

CRITICAL RULES:
1. ONLY use the provided retrieved context to answer questions
2. NEVER use external knowledge or make assumptions
3. NEVER hallucinate or guess information
4. If the context does not contain the answer, respond with: "This question is not answered in the book."
5. Always cite the source chapter/section when available
6. Keep answers concise and accurate to the book's content

When answering:
- Quote or paraphrase the retrieved content faithfully
- Include chapter/section references in your response
- If multiple sources are relevant, synthesize them coherently
```

---

## 8. Error Handling Strategy

### Decision
Implement graceful degradation with user-friendly error messages.

### Error Scenarios
| Scenario | Handling |
|----------|----------|
| Cohere API unavailable | Return "Unable to process your question. Please try again." |
| Qdrant connection failure | Return "Book content temporarily unavailable. Please try again." |
| Empty retrieval results | Return "This question is not answered in the book." |
| Invalid/empty query | Return "Please provide a question about the book content." |

---

## 9. Retrieval Configuration

### Decision
Use conservative retrieval settings aligned with constitution.

### Configuration
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `top_k` | 5 | Matches spec FR-004, constitution RETRIEVAL_CONFIG |
| `similarity_threshold` | 0.75 | Matches constitution, filters irrelevant results |
| `max_context_tokens` | 4000 | Constitution context_window limit |

---

## Outstanding Questions Resolved

1. **Q: Which Gemini model to use?**
   - A: `gemini/gemini-2.0-flash` via LiteLLM - good balance of speed and capability

2. **Q: How to handle embedding model mismatch?**
   - A: Must verify existing Qdrant collection uses same Cohere model (embed-english-v3.0)

3. **Q: Sync vs Async implementation?**
   - A: Use async pattern with `asyncio` as OpenAI Agents SDK is async-first

---

## Dependencies Summary

```toml
[project]
dependencies = [
    "openai-agents>=0.2.0",
    "litellm>=1.0.0",
    "cohere>=5.0.0",
    "qdrant-client>=1.7.0",
    "python-dotenv>=1.0.0",
]
```
