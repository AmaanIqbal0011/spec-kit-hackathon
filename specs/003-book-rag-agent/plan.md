# Implementation Plan: Book RAG Agent

**Branch**: `003-book-rag-agent` | **Date**: 2025-12-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-book-rag-agent/spec.md`

## Summary

Implement a RAG-based chatbot agent (BookRAGAgent) that answers questions exclusively from book content stored in Qdrant. The agent uses OpenAI Agents SDK with LiteLLM for Gemini provider integration, Cohere for embeddings, and operates entirely within the `agent/` directory managed by UV package manager. All code consolidated in single `main.py` file per user requirement.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: openai-agents, litellm, cohere, qdrant-client, python-dotenv
**Storage**: Qdrant vector database (existing, read-only access)
**Testing**: Manual testing via CLI (pytest for unit tests if needed)
**Target Platform**: Local development / hackathon deployment
**Project Type**: Single CLI application
**Performance Goals**: Response within 5 seconds under normal conditions
**Constraints**: All code in `agent/main.py`, UV package manager, environment variables for secrets
**Scale/Scope**: Single-user CLI tool, ~5 retrieval chunks per query

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Technical Accuracy | PASS | Uses official SDKs (Cohere, Qdrant, OpenAI Agents) |
| II. Educational Clarity | N/A | Agent code, not book content |
| III. AI-Native Design | PASS | RAG retrieval follows constitution specs (top_k=5, threshold=0.75) |
| IV. Reproducibility | PASS | UV lockfile ensures reproducible builds |
| V. Industry Relevance | PASS | Uses industry-standard RAG patterns |
| VI. Open Knowledge | PASS | Simple, single-file architecture |

### RAG & AI Agent Standards Compliance

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Retrieval top_k=5 | PASS | Configured in constants |
| Similarity threshold 0.75 | PASS | Applied in Qdrant query |
| Context window 4000 tokens | PASS | Enforced in context aggregation |
| Zero hallucination | PASS | Strict agent instructions |
| Safety filters | PASS | Book-only responses enforced |

### Security & Deployment Standards Compliance

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| API keys in env vars | PASS | python-dotenv + .env |
| No hardcoded secrets | PASS | All keys from environment |
| .gitignore includes .env | REQUIRED | Must add .env to .gitignore |

## Project Structure

### Documentation (this feature)

```text
specs/003-book-rag-agent/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research output
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup guide
├── contracts/           # API contracts
│   └── agent-api.md     # Function interfaces
└── tasks.md             # Phase 2 output (from /sp.tasks)
```

### Source Code (repository root)

```text
agent/
├── main.py              # All agent code (single file per requirement)
├── pyproject.toml       # UV project configuration
├── uv.lock              # Dependency lockfile
└── .env                 # Environment variables (not committed)
```

**Structure Decision**: Single-file architecture (`agent/main.py`) as specified by user requirements. All components (configuration, clients, embedding, retrieval tool, agent definition, runtime) consolidated in one file for hackathon simplicity.

## Implementation Architecture

### Component Layout in main.py

```python
# main.py structure:

# 1. Imports and Environment Setup
# 2. Configuration Constants
# 3. Client Initialization (Cohere, Qdrant)
# 4. Embedding Function
# 5. Retrieval Tool (with @function_tool decorator)
# 6. Agent Definition
# 7. Main Runner Function
# 8. CLI Entry Point
```

### Data Flow

```
User Query → Embedding (Cohere) → Vector Search (Qdrant) → Context Assembly → Agent (Gemini via LiteLLM) → Response
```

## Implementation Phases

### Phase 1: Environment Setup
1. Initialize UV project in `agent/` directory
2. Add dependencies to pyproject.toml
3. Create `.env.example` template
4. Add `.env` to `.gitignore`

### Phase 2: Client Initialization
1. Load environment variables with python-dotenv
2. Initialize Cohere client for embeddings
3. Initialize Qdrant client for vector search
4. Validate connections on startup

### Phase 3: Embedding Layer
1. Implement `get_embedding(text: str) -> list[float]`
2. Use Cohere embed-english-v3.0 (or matching model)
3. Set `input_type="search_query"` for queries
4. Handle API errors gracefully

### Phase 4: Retrieval Tool
1. Implement `retrieve_book_context` with `@function_tool`
2. Generate query embedding
3. Search Qdrant with similarity threshold
4. Format results with metadata (chapter, section)
5. Handle empty results with fallback message

### Phase 5: Agent Definition
1. Create Agent with LitellmModel (Gemini)
2. Define strict system instructions
3. Register retrieval tool
4. Configure for book-only responses

### Phase 6: Runtime & CLI
1. Implement async main runner
2. Add CLI argument parsing
3. Implement interactive mode
4. Add error handling for all scenarios

## Key Implementation Details

### 1. Agent Configuration

```python
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

agent = Agent(
    name="BookRAGAgent",
    instructions=SYSTEM_PROMPT,
    model=LitellmModel(
        model="gemini/gemini-2.0-flash",
        api_key=os.environ["GEMINI_API_KEY"]
    ),
    tools=[retrieve_book_context]
)
```

### 2. Retrieval Tool Pattern

```python
@function_tool
def retrieve_book_context(query: str) -> str:
    """Retrieve relevant context from the book."""
    embedding = get_embedding(query)
    results = qdrant_client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=embedding,
        limit=TOP_K,
        with_payload=True,
        score_threshold=SIMILARITY_THRESHOLD
    )
    return format_context(results)
```

### 3. Configuration Constants

```python
TOP_K = 5
SIMILARITY_THRESHOLD = 0.75
MAX_CONTEXT_TOKENS = 4000
EMBEDDING_MODEL = "embed-english-v3.0"  # Verify against existing collection
```

## Complexity Tracking

> No complexity violations identified. Single-file architecture is the simplest viable solution.

| Decision | Justification |
|----------|---------------|
| Single main.py file | User requirement for hackathon simplicity |
| LiteLLM abstraction | Required for Gemini + OpenAI Agents SDK integration |
| No database ORM | Read-only Qdrant access, no writes needed |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Embedding model mismatch | Verify existing Qdrant collection schema before implementation |
| Qdrant unavailable | Graceful error handling with user-friendly message |
| Rate limiting (Cohere/Gemini) | Implement basic retry logic |
| Context too long | Truncate to top chunks within token limit |

## Dependencies

```toml
[project]
name = "book-rag-agent"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "openai-agents>=0.2.0",
    "litellm>=1.0.0",
    "cohere>=5.0.0",
    "qdrant-client>=1.7.0",
    "python-dotenv>=1.0.0",
]
```

## Success Criteria Mapping

| Spec Criteria | Implementation |
|---------------|----------------|
| SC-001: Response < 5s | Async architecture, top-k limit |
| SC-002: 95% accuracy | Strict context-only answers |
| SC-003: 100% refusal for out-of-scope | System prompt enforcement |
| SC-004: 90% retrieval success | Similarity threshold tuning |
| SC-005: 80% source citations | Metadata in response formatting |
| SC-006: Graceful error handling | Try/except with user messages |

## Next Steps

1. Run `/sp.tasks` to generate detailed implementation tasks
2. Verify Qdrant collection schema (embedding model, dimensions)
3. Implement and test each phase sequentially
4. Create PHR after implementation complete

---

**Plan Status**: Ready for `/sp.tasks`
