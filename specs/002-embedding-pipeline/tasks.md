# Tasks: Embedding Pipeline for RAG Retrieval

**Input**: Design documents from `/specs/002-embedding-pipeline/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md
**Branch**: `002-embedding-pipeline`

**Code Organization**: Single file (`backend/main.py`) - all logic in one file per user requirement

**Tests**: Manual verification only (single-file constraint - no separate test files)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- All code goes in `backend/main.py`

## Path Conventions

```text
backend/
├── main.py              # ALL pipeline code
├── .env                 # Environment variables (gitignored)
├── .env.example         # Template
├── pyproject.toml       # UV configuration
└── uv.lock              # Dependency lockfile
```

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create backend environment ready for pipeline execution

- [x] T001 Create `backend/` directory at repository root
- [x] T002 Initialize Python project using UV in `backend/` (`uv init`)
- [x] T003 Add required dependencies via UV: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv
- [x] T004 [P] Create `.env.example` with COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY placeholders in `backend/.env.example`
- [x] T005 [P] Create `.gitignore` with `.env`, `__pycache__/`, `.venv/` entries in `backend/.gitignore`
- [x] T006 Create empty `backend/main.py` with imports and docstring header

**Checkpoint**: Backend environment ready - `uv run python main.py` should execute without errors (empty main)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure in `main.py` that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Add all required imports to `backend/main.py`: requests, BeautifulSoup, xml.etree, cohere, qdrant_client, dotenv, os, hashlib, uuid, logging
- [x] T008 Configure logging with INFO level and timestamped format in `backend/main.py`
- [x] T009 Add `load_dotenv()` call and environment variable loading helper in `backend/main.py`
- [x] T010 Add constants: SITEMAP_URL, COLLECTION_NAME ("rag_embedding"), CHUNK_SIZE (1000), OVERLAP (100), VECTOR_SIZE (1024)

**Checkpoint**: Foundation ready - imports work, logging configured, constants defined

---

## Phase 3: User Story 1 - Crawl and Index Docusaurus Content (Priority: P1) 🎯 MVP

**Goal**: Extract clean text content from deployed Docusaurus site via sitemap

**Independent Test**: Run `get_all_urls()` and `extract_text_from_urls()`, verify URLs extracted and text content returned with metadata

### Implementation for User Story 1

- [x] T011 [US1] Implement `get_all_urls(sitemap_url: str) -> list[str]` function in `backend/main.py`
  - Fetch sitemap.xml using requests
  - Parse XML with ElementTree
  - Handle sitemap namespace
  - Extract all `<loc>` URLs
  - Filter to same domain only
  - Return list of URLs

- [x] T012 [US1] Implement `extract_text_from_urls(urls: list[str]) -> list[dict]` function in `backend/main.py`
  - Iterate through URLs with error handling
  - Fetch HTML content for each URL
  - Remove `<script>`, `<style>`, `<nav>`, `<footer>`, `<aside>`, `<header>` tags
  - Extract main content using Docusaurus selectors: `article`, `.markdown`, `.theme-doc-markdown`, `main`
  - Fallback to `<body>` if no selector matches
  - Extract page title from `<title>` tag
  - Skip pages with <100 characters content
  - Normalize whitespace
  - Return list of dicts: {url, title, content}

- [x] T013 [US1] Add error handling and logging for URL fetching failures in `backend/main.py`
  - Log failed URLs with reason
  - Continue processing remaining URLs on failure
  - Track success/failure counts

**Checkpoint**: User Story 1 complete - can crawl sitemap and extract text independently

---

## Phase 4: User Story 2 - Generate Cohere Embeddings (Priority: P2)

**Goal**: Transform extracted text into vector embeddings using Cohere API

**Independent Test**: Provide sample text chunks, call `chunk_text()` and `embed()`, verify 1024-dim vectors returned

### Implementation for User Story 2

- [x] T014 [US2] Implement `chunk_text(documents: list[dict], chunk_size: int = 1000, overlap: int = 100) -> list[dict]` function in `backend/main.py`
  - Iterate through documents
  - Split content into overlapping chunks
  - Skip empty/whitespace-only chunks
  - Track chunk_index per document
  - Return list of dicts: {text, source_url, title, chunk_index}

- [x] T015 [US2] Implement `embed(chunks: list[dict], cohere_client) -> list[list[float]]` function in `backend/main.py`
  - Extract text from chunks
  - Batch in groups of 96 (Cohere limit)
  - Call cohere.embed() with model="embed-multilingual-v3.0", input_type="search_document"
  - Handle API errors with retry logic
  - Skip failed batches, log errors, continue
  - Return list of embedding vectors

- [x] T016 [US2] Add Cohere client initialization in `backend/main.py`
  - Load COHERE_API_KEY from environment
  - Validate key exists before proceeding

**Checkpoint**: User Story 2 complete - can chunk text and generate embeddings independently

---

## Phase 5: User Story 3 - Store Embeddings in Qdrant (Priority: P3)

**Goal**: Persist embeddings with metadata in Qdrant for RAG retrieval

**Independent Test**: Create collection, upsert sample vectors, query Qdrant to verify storage

### Implementation for User Story 3

- [x] T017 [US3] Implement `create_collection(qdrant_client, collection_name: str = "rag_embedding")` function in `backend/main.py`
  - Check if collection exists
  - Create collection with VectorParams(size=1024, distance=COSINE)
  - Log creation or skip if exists

- [x] T018 [US3] Implement `save_chunk_to_qdrant(qdrant_client, chunks: list[dict], embeddings: list[list[float]], collection_name: str = "rag_embedding")` function in `backend/main.py`
  - Generate deterministic UUID from source_url + chunk_index (MD5 hash)
  - Create PointStruct with vector and payload: {source_url, title, chunk_text, chunk_index, timestamp}
  - Batch upsert all points
  - Log success count

- [x] T019 [US3] Add Qdrant client initialization in `backend/main.py`
  - Load QDRANT_URL and QDRANT_API_KEY from environment
  - Support both local and cloud Qdrant

**Checkpoint**: User Story 3 complete - can create collection and store vectors independently

---

## Phase 6: User Story 4 - End-to-End Pipeline Execution (Priority: P4)

**Goal**: Single command executes full pipeline from URL to stored embeddings

**Independent Test**: Run `python main.py`, verify vectors exist in Qdrant with correct metadata

### Implementation for User Story 4

- [x] T020 [US4] Implement `main()` function in `backend/main.py`
  - Load environment variables
  - Initialize Cohere client
  - Initialize Qdrant client
  - Execute pipeline in order:
    1. Create Qdrant collection
    2. Fetch URLs from sitemap
    3. Extract text from URLs
    4. Chunk text
    5. Generate embeddings
    6. Store in Qdrant
  - Print progress at each stage
  - Generate completion report with stats

- [x] T021 [US4] Add `if __name__ == "__main__": main()` entry point in `backend/main.py`

- [x] T022 [US4] Add comprehensive logging throughout pipeline in `backend/main.py`
  - Log start/end of each stage
  - Log counts: URLs found, documents extracted, chunks created, embeddings generated, vectors stored
  - Log any errors with context

- [x] T023 [US4] Add final statistics report in `backend/main.py`
  - Total pages processed
  - Total chunks created
  - Total vectors stored
  - Any failures logged

**Checkpoint**: User Story 4 complete - full pipeline runs end-to-end

---

## Phase 7: Polish & Validation

**Purpose**: Final verification and cleanup

- [ ] T024 [P] Validate pipeline runs successfully against https://spec-kit-hackathon.vercel.app/sitemap.xml
- [ ] T025 [P] Verify vectors exist in `rag_embedding` collection via Qdrant API/UI
- [ ] T026 [P] Verify metadata correctness (source_url, title, chunk_text fields populated)
- [ ] T027 [P] Run sample similarity search manually to test retrieval quality
- [x] T028 Update `backend/.env.example` with final configuration notes

**Note**: T024-T027 require COHERE_API_KEY and QDRANT_URL to be configured in `.env` before running.

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Phase 1: Setup ──────────────────────────────────────┐
                                                     │
Phase 2: Foundational (BLOCKS all user stories) ◄────┤
                                                     │
Phase 3: US1 - Crawl & Extract ◄─────────────────────┤
         │                                           │
         ▼                                           │
Phase 4: US2 - Chunk & Embed ◄───────────────────────┤
         │                                           │
         ▼                                           │
Phase 5: US3 - Qdrant Storage ◄──────────────────────┤
         │                                           │
         ▼                                           │
Phase 6: US4 - Pipeline Orchestration ◄──────────────┤
         │                                           │
         ▼                                           │
Phase 7: Polish & Validation ◄───────────────────────┘
```

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational only - can implement independently
- **US2 (P2)**: Depends on US1 output (documents) - sequential after US1
- **US3 (P3)**: Depends on US2 output (embeddings) - sequential after US2
- **US4 (P4)**: Integrates US1-US3 - sequential after US3

### Single-File Constraint

⚠️ **All code goes in `backend/main.py`** - no parallel file creation possible for code tasks

Parallel opportunities exist only for:
- T004/T005: Config files (.env.example, .gitignore)
- T024-T027: Validation tasks

---

## Parallel Example: Setup Phase

```bash
# These can run in parallel (different files):
Task T004: Create .env.example in backend/.env.example
Task T005: Create .gitignore in backend/.gitignore
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Crawl & Extract)
4. **STOP and VALIDATE**: Test URL extraction independently
5. Continue to US2-US4

### Full Pipeline Delivery

1. Setup → Foundational → Foundation ready
2. US1 (Crawl) → Test: URLs extracted correctly
3. US2 (Embed) → Test: Vectors generated correctly
4. US3 (Store) → Test: Vectors in Qdrant
5. US4 (Pipeline) → Test: End-to-end execution
6. Polish → Validate against target site

---

## Completion Criteria

This spec is considered **DONE** when:

- ✔ `backend/` directory exists with UV project initialized
- ✔ `backend/main.py` contains all 7 functions
- ✔ Pipeline runs via `uv run python main.py`
- ✔ All book URLs from sitemap are processed
- ✔ `rag_embedding` collection contains vectors
- ✔ Metadata links chunks to source URLs
- ✔ Statistics report printed on completion

---

## Task Summary

| Phase | Tasks | Parallel | Description |
|-------|-------|----------|-------------|
| 1. Setup | T001-T006 | 2 | Project initialization |
| 2. Foundational | T007-T010 | 0 | Core infrastructure |
| 3. US1 Crawl | T011-T013 | 0 | URL extraction |
| 4. US2 Embed | T014-T016 | 0 | Embedding generation |
| 5. US3 Store | T017-T019 | 0 | Qdrant storage |
| 6. US4 Pipeline | T020-T023 | 0 | Orchestration |
| 7. Polish | T024-T028 | 4 | Validation |

**Total Tasks**: 28
**Parallel Opportunities**: 6 tasks (in Setup and Polish phases only)
**MVP Scope**: Phases 1-3 (T001-T013) for basic crawl functionality
