# Tasks: Book RAG Agent

**Input**: Design documents from `/specs/003-book-rag-agent/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Critical Constraint**: ALL implementation must be done inside a SINGLE FILE: `agent/main.py`

**Code Structure Constraint**: Implementation MUST use:
- `OpenAIChatCompletionsModel` with `AsyncOpenAI` (NOT LiteLLM)
- `Runner.run_sync` for synchronous execution
- Gemini via OpenAI-compatible endpoint (`https://generativelanguage.googleapis.com/v1beta/openai/`)
- `@function_tool` decorator for retrieval tool

**Tests**: Manual CLI testing only (no automated tests requested)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

```text
agent/
├── main.py              # ALL code lives here (single file)
├── pyproject.toml       # UV project configuration
├── uv.lock              # Dependency lockfile
├── .env                 # Environment variables (not committed)
└── .env.example         # Template for environment variables
```

---

## Phase 1: Project & Environment Setup

**Purpose**: Create project structure, initialize UV, configure environment

- [x] T001 Create `agent/` directory at repository root
- [x] T002 Initialize UV Python project in `agent/` directory with `uv init`
- [x] T003 Set Python version to 3.10+ in `agent/pyproject.toml`
- [x] T004 [P] Create `agent/.env` file with environment variables (GEMINI_API_KEY, COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY)
- [x] T005 [P] Create `agent/.env.example` template with placeholder values for all environment variables
- [x] T006 [P] Add `.env` to `.gitignore` in repository root (if not already present)
- [x] T007 Create empty `agent/main.py` file (single implementation file)
- [x] T008 Ensure NO other Python files exist in `agent/` directory

**Checkpoint**: ✅ Project structure ready, environment configured

---

## Phase 2: Dependency Installation (UV)

**Purpose**: Install and lock all required dependencies

- [x] T009 Add `openai-agents` dependency to `agent/pyproject.toml`
- [x] T010 [P] Add `python-dotenv` dependency to `agent/pyproject.toml`
- [x] T011 [P] Add `cohere` dependency to `agent/pyproject.toml`
- [x] T012 [P] Add `qdrant-client` dependency to `agent/pyproject.toml`
- [x] T013 Run `uv sync` to lock dependencies and create `agent/uv.lock`
- [x] T014 Verify environment runs with `uv run python -c "print('OK')"`

**Checkpoint**: ✅ Dependencies installed and locked

---

## Phase 3: Agent SDK Bootstrap (Inside main.py)

**Purpose**: Core imports, logging setup, and environment loading

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Imports & Configuration

- [x] T015 Add import for `Agent` from `agents` in `agent/main.py`
- [x] T016 Add import for `Runner` from `agents` in `agent/main.py`
- [x] T017 Add import for `OpenAIChatCompletionsModel` from `agents` in `agent/main.py`
- [x] T018 Add import for `function_tool` from `agents` in `agent/main.py`
- [x] T019 Add import for `AsyncOpenAI` from `openai` in `agent/main.py`
- [x] T020 Add import for `set_tracing_disabled` from `agents` in `agent/main.py`
- [x] T021 Add imports for `cohere`, `qdrant_client`, `os`, `dotenv` in `agent/main.py`

### Environment & Logging Setup

- [x] T022 Add `load_dotenv()` call at module level in `agent/main.py`
- [x] T023 Enable verbose stdout logging with print statements in `agent/main.py`
- [x] T024 Disable tracing explicitly with `set_tracing_disabled(True)` in `agent/main.py`

**Checkpoint**: ✅ SDK bootstrap complete

---

## Phase 4: Gemini Model Provider Setup

**Purpose**: Configure Gemini as the model provider via OpenAI-compatible endpoint

- [x] T025 Read `GEMINI_API_KEY` from environment using `os.environ.get()` in `agent/main.py`
- [x] T026 Initialize `AsyncOpenAI` client with Gemini API key and base URL `https://generativelanguage.googleapis.com/v1beta/openai/` in `agent/main.py`
- [x] T027 Create `OpenAIChatCompletionsModel` instance with model name `gemini-2.0-flash` in `agent/main.py`
- [x] T028 Pass the `AsyncOpenAI` client to `OpenAIChatCompletionsModel` via `openai_client` parameter in `agent/main.py`

**Checkpoint**: ✅ Gemini model provider ready

---

## Phase 5: External Client Initialization (Inside main.py)

**Purpose**: Initialize Cohere and Qdrant clients

### Cohere Client

- [x] T029 Read `COHERE_API_KEY` from environment in `agent/main.py`
- [x] T030 Initialize `cohere.Client` with API key in `agent/main.py`
- [x] T031 Add comment restricting Cohere usage to embeddings only in `agent/main.py`

### Qdrant Client

- [x] T032 Read `QDRANT_URL` from environment in `agent/main.py`
- [x] T033 Read `QDRANT_API_KEY` from environment in `agent/main.py`
- [x] T034 Initialize `QdrantClient` with URL and API key in `agent/main.py`
- [x] T035 Define `QDRANT_COLLECTION` constant for the book collection name in `agent/main.py`
- [x] T036 Add `validate_connections()` function to verify Qdrant connectivity at runtime in `agent/main.py`

**Checkpoint**: ✅ External clients initialized

---

## Phase 6: Embedding Function Definition

**Purpose**: Implement embedding generation using Cohere

- [x] T037 Define `get_embedding(text: str) -> list[float]` function in `agent/main.py`
- [x] T038 Use Cohere `embed-english-v3.0` model in embedding function in `agent/main.py`
- [x] T039 Set `input_type="search_query"` parameter in Cohere embed call in `agent/main.py`
- [x] T040 Accept raw text input and strip whitespace in `get_embedding()` in `agent/main.py`
- [x] T041 Return single embedding vector from response in `agent/main.py`
- [x] T042 Add error handling for Cohere API failures in `get_embedding()` in `agent/main.py`

**Checkpoint**: ✅ Embedding function ready

---

## Phase 7: User Story 1 - Ask Book Question (Priority: P1) 🎯 MVP

**Goal**: User can ask a question about the book and receive an accurate, grounded answer

**Independent Test**: Submit a question known to be in the book, verify answer cites book content

### Retrieval Tool Implementation

- [x] T043 [US1] Define `retrieve(query: str) -> str` function with `@function_tool` decorator in `agent/main.py`
- [x] T044 [US1] Accept user query as input parameter in retrieve function in `agent/main.py`
- [x] T045 [US1] Call `get_embedding(query)` within retrieve function in `agent/main.py`
- [x] T046 [US1] Query Qdrant using vector similarity search with `search()` method in `agent/main.py`
- [x] T047 [US1] Limit results to TOP_K=5 chunks in Qdrant query in `agent/main.py`
- [x] T048 [US1] Extract `text` field from Qdrant payload for each result in `agent/main.py`
- [x] T049 [US1] Return retrieved text chunks as formatted string (NOT answer generation) in `agent/main.py`
- [x] T050 [US1] Add error handling for Qdrant search failures in retrieve function in `agent/main.py`

### Agent Instruction Definition

- [x] T051 [US1] Define `INSTRUCTIONS` constant as multiline string in `agent/main.py`
- [x] T052 [US1] State in instructions: "Agent is book-specific" in `agent/main.py`
- [x] T053 [US1] State in instructions: "Must call retrieve tool first" in `agent/main.py`
- [x] T054 [US1] State in instructions: "Must use ONLY retrieved content" in `agent/main.py`
- [x] T055 [US1] State in instructions: "Say 'I don't know' if answer not in context" in `agent/main.py`

### Agent Construction

- [x] T056 [US1] Create `Agent` instance with name "BookRAGAgent" in `agent/main.py`
- [x] T057 [US1] Attach `INSTRUCTIONS` to agent via `instructions` parameter in `agent/main.py`
- [x] T058 [US1] Attach Gemini-backed `OpenAIChatCompletionsModel` to agent via `model` parameter in `agent/main.py`
- [x] T059 [US1] Register `retrieve` as the only tool via `tools=[retrieve]` in `agent/main.py`

### Execution via Runner

- [x] T060 [US1] Define `main()` function as entry point in `agent/main.py`
- [x] T061 [US1] Use `Runner.run_sync(agent, query)` for synchronous execution in `agent/main.py`
- [x] T062 [US1] Capture final output from result in `agent/main.py`
- [x] T063 [US1] Print or return the final answer in `agent/main.py`
- [x] T064 [US1] Add `if __name__ == "__main__":` block to run main() in `agent/main.py`

### Manual Validation

- [ ] T065 [US1] Test with book-related question - verify retrieval tool is invoked
- [ ] T066 [US1] Verify answer uses retrieved content from the book

**Checkpoint**: ✅ User Story 1 complete - MVP functional

---

## Phase 8: User Story 2 - Handle Out-of-Scope Questions (Priority: P2)

**Goal**: Agent refuses to answer questions not covered in the book without hallucinating

**Independent Test**: Ask off-topic questions, verify agent refuses gracefully with "I don't know"

### Fallback Handling

- [x] T067 [US2] Add empty result detection in retrieve function when Qdrant returns no matches in `agent/main.py`
- [x] T068 [US2] Return fallback message "No relevant content found in the book." when no chunks retrieved in `agent/main.py`
- [x] T069 [US2] Ensure `INSTRUCTIONS` emphasizes refusal behavior when context is empty in `agent/main.py`

### Manual Validation

- [ ] T070 [US2] Test with off-topic question: "What is the weather today?" - verify "I don't know" response
- [ ] T071 [US2] Test with non-book topic: "Explain quantum physics" - verify refusal
- [ ] T072 [US2] Ensure no hallucinated answers occur for out-of-scope questions

**Checkpoint**: ✅ User Story 2 complete - refusal handling works

---

## Phase 9: User Story 3 - Receive Contextual Citations (Priority: P3)

**Goal**: Answers include chapter/section references when metadata is available

**Independent Test**: Ask a question, verify response includes source citations

### Citation Formatting

- [x] T073 [US3] Update retrieve function to include `[Source: Chapter X - Section Y]` prefix for each chunk in `agent/main.py`
- [x] T074 [US3] Extract `chapter`, `section` from Qdrant payload metadata in `agent/main.py`
- [x] T075 [US3] Handle missing metadata gracefully (use "Unknown" if not present) in `agent/main.py`
- [x] T076 [US3] Update `INSTRUCTIONS` to instruct agent to include citations in answers in `agent/main.py`

### Manual Validation

- [ ] T077 [US3] Test citation display - verify chapter/section shown in response
- [ ] T078 [US3] Test multi-source answer - verify all sources cited

**Checkpoint**: ✅ User Story 3 complete - citations displayed

---

## Phase 10: Final Verification & Polish

**Purpose**: Validate implementation matches requirements

- [x] T079 Confirm ALL logic exists only in `agent/main.py` (no other .py files)
- [x] T080 Confirm code structure matches the reference: `OpenAIChatCompletionsModel` + `AsyncOpenAI` + `Runner.run_sync`
- [x] T081 Confirm Gemini is accessed via OpenAI-compatible endpoint (NOT LiteLLM)
- [x] T082 Confirm Cohere is used ONLY for embeddings
- [x] T083 Confirm Qdrant is the ONLY data source for retrieval
- [x] T084 Verify UV environment is reproducible with `uv sync`
- [ ] T085 Run full end-to-end test with sample query
- [x] T086 Mark agent as **production & hackathon ready**

**Checkpoint**: ✅ All verification passed - agent ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Dependencies)
    │
    ▼
Phase 3 (SDK Bootstrap)
    │
    ▼
Phase 4 (Gemini Provider)
    │
    ▼
Phase 5 (External Clients)
    │
    ▼
Phase 6 (Embedding Function)
    │
    ├───────────────┬───────────────┐
    ▼               ▼               ▼
Phase 7 (US1)   Phase 8 (US2)   Phase 9 (US3)
    │               │               │
    └───────────────┴───────────────┘
                    │
                    ▼
              Phase 10 (Final Verification)
```

### User Story Dependencies

- **User Story 1 (P1)**: Requires Phases 1-6 complete - No dependencies on other stories
- **User Story 2 (P2)**: Requires Phase 7 (US1) complete - Builds on retrieval function
- **User Story 3 (P3)**: Requires Phase 7 (US1) complete - Extends context formatting

### Within Each Phase

- All tasks within a phase are sequential (single-file constraint)
- Complete phase before moving to next
- Manual validation at each checkpoint

### Parallel Opportunities

- **Phase 1**: T004, T005, T006 can run in parallel (different files/operations)
- **Phase 2**: T009, T010, T011, T012 can run in parallel (pyproject.toml edits)
- **Single-file constraint**: Most implementation tasks are sequential within `main.py`

---

## Parallel Example: Phase 1 Setup

```bash
# Launch parallel setup tasks:
Task: "Create agent/.env file with environment variables"
Task: "Create agent/.env.example template"
Task: "Add .env to .gitignore"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Dependencies
3. Complete Phase 3: SDK Bootstrap
4. Complete Phase 4: Gemini Provider
5. Complete Phase 5: External Clients
6. Complete Phase 6: Embedding Function
7. Complete Phase 7: User Story 1
8. **STOP and VALIDATE**: Test with book questions
9. Deploy/demo if ready - this is a functional RAG agent!

### Incremental Delivery

1. Complete Setup + Dependencies + Bootstrap → Foundation ready
2. Complete Provider + Clients + Embedding → Infrastructure ready
3. Add User Story 1 → Test → **MVP Complete!**
4. Add User Story 2 → Test → Refusal handling added
5. Add User Story 3 → Test → Citations added
6. Each story adds value without breaking previous functionality

### Single-File Development Flow

Since all code is in `main.py`:
1. Add new section/function to file
2. Test immediately with `uv run python agent/main.py`
3. Iterate until section works
4. Move to next task

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 8 | Project initialization |
| Phase 2: Dependencies | 6 | Install dependencies |
| Phase 3: SDK Bootstrap | 10 | Imports & config |
| Phase 4: Gemini Provider | 4 | Model setup |
| Phase 5: External Clients | 8 | Cohere & Qdrant |
| Phase 6: Embedding | 6 | Embedding function |
| Phase 7: US1 (P1) | 24 | Ask book question - MVP |
| Phase 8: US2 (P2) | 6 | Out-of-scope handling |
| Phase 9: US3 (P3) | 6 | Contextual citations |
| Phase 10: Final | 8 | Verification |
| **Total** | **86** | |

### Per User Story Breakdown

- **US1**: 24 tasks (28%) - Core functionality (MVP)
- **US2**: 6 tasks (7%) - Error handling
- **US3**: 6 tasks (7%) - Citations

### Suggested MVP Scope

**User Story 1 only** (Phases 1-7): 66 tasks
- Delivers working RAG agent
- Answers book questions with grounded responses
- Manual validation included

---

## Key Implementation Pattern (Reference)

```python
# agent/main.py - Target structure

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
import cohere
from qdrant_client import QdrantClient

# Load environment
load_dotenv()

# Disable tracing
set_tracing_disabled(True)

# Environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
QDRANT_COLLECTION = "physical_ai_textbook"

# Initialize clients
gemini_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=gemini_client
)

cohere_client = cohere.Client(api_key=COHERE_API_KEY)
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Embedding function (Cohere only)
def get_embedding(text: str) -> list[float]:
    response = cohere_client.embed(
        texts=[text.strip()],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]

# Retrieval tool
@function_tool
def retrieve(query: str) -> str:
    """Retrieve relevant content from the book."""
    embedding = get_embedding(query)
    results = qdrant_client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=embedding,
        limit=5
    )
    if not results:
        return "No relevant content found in the book."
    # Format results with citations
    chunks = []
    for r in results:
        chapter = r.payload.get("chapter", "Unknown")
        section = r.payload.get("section", "Unknown")
        text = r.payload.get("text", "")
        chunks.append(f"[Source: Chapter {chapter} - {section}]\n{text}")
    return "\n\n".join(chunks)

# Agent instructions
INSTRUCTIONS = """You are BookRAGAgent, a specialized assistant for the Physical AI & Humanoid Robotics textbook.

RULES:
1. ALWAYS call the retrieve tool first before answering
2. Use ONLY the retrieved content to answer
3. If no relevant content is found, say "I don't know"
4. Include source citations in your answers
5. Never hallucinate or use external knowledge
"""

# Create agent
agent = Agent(
    name="BookRAGAgent",
    instructions=INSTRUCTIONS,
    model=model,
    tools=[retrieve]
)

# Main execution
def main():
    query = input("Ask a question about the book: ")
    result = Runner.run_sync(agent, query)
    print(result.final_output)

if __name__ == "__main__":
    main()
```

---

## Notes

- All tasks target `agent/main.py` (single-file constraint)
- No test file tasks (manual testing only per spec)
- [P] tasks indicate parallel potential where applicable
- [Story] labels map tasks to user stories for traceability
- Commit after each logical task group
- Validate at checkpoints before proceeding
- **CRITICAL**: Use `OpenAIChatCompletionsModel` + `AsyncOpenAI` (NOT LiteLLM)
- **CRITICAL**: Use `Runner.run_sync` (NOT async `Runner.run`)
