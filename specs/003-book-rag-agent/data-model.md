# Data Model: Book RAG Agent

**Feature Branch**: `003-book-rag-agent`
**Date**: 2025-12-15

## Overview

This document defines the data entities and their relationships for the BookRAGAgent system.

---

## Core Entities

### 1. Query

Represents a user's natural language question.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `text` | string | The raw user question | Required, non-empty, max 2000 chars |
| `timestamp` | datetime | When query was received | Auto-generated |

**Validation Rules**:
- Must be non-empty after whitespace trimming
- Must not exceed 2000 characters
- Single-word queries are allowed but may return broader results

---

### 2. Embedding

Vector representation of text for semantic search.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `vector` | float[] | Numerical embedding | Required, dimension must match collection |
| `model` | string | Embedding model used | e.g., "embed-english-v3.0" |
| `dimension` | int | Vector dimension | 1024 for Cohere v3, 1536 for OpenAI |

**Validation Rules**:
- Vector dimension must match Qdrant collection schema
- All values must be valid floats (no NaN/Inf)

---

### 3. RetrievedChunk

A text segment retrieved from the vector database.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | string | Unique chunk identifier | UUID from Qdrant |
| `text` | string | The text content | Required |
| `score` | float | Similarity score | 0.0 to 1.0 |
| `chapter` | string | Source chapter | Optional metadata |
| `section` | string | Source section | Optional metadata |
| `module` | string | Module identifier | Optional metadata |
| `keywords` | string[] | Associated keywords | Optional metadata |

**Validation Rules**:
- Score must be between 0.0 and 1.0
- Text must be non-empty
- Chunks with score < 0.75 are filtered out

---

### 4. Context

Aggregated context from multiple retrieved chunks.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `chunks` | RetrievedChunk[] | Array of relevant chunks | Max 5 chunks |
| `total_tokens` | int | Estimated token count | Max 4000 |
| `formatted_text` | string | Concatenated context | For agent injection |

**Validation Rules**:
- Maximum 5 chunks (configurable via top_k)
- Total tokens must not exceed 4000
- Chunks ordered by relevance score (descending)

---

### 5. Response

Agent's answer to the user query.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `answer` | string | The generated response | Required |
| `sources` | Source[] | Citation references | May be empty |
| `is_refusal` | bool | True if no context found | Default: false |
| `refusal_reason` | string | Why refused (if applicable) | Optional |

**Validation Rules**:
- If `is_refusal` is true, `refusal_reason` must be provided
- Answer must not contain hallucinated content
- Sources must reference actual retrieved chunks

---

### 6. Source (Citation)

Reference to book content source.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `chapter` | string | Chapter reference | e.g., "01-ros2-fundamentals" |
| `section` | string | Section reference | e.g., "Creating a Publisher Node" |
| `module` | string | Module reference | e.g., "Module 1" |

---

## Entity Relationships

```
┌─────────────┐
│    Query    │
└──────┬──────┘
       │ generates
       ▼
┌─────────────┐
│  Embedding  │
└──────┬──────┘
       │ searches
       ▼
┌─────────────────┐
│ RetrievedChunk  │ (0..5)
└──────┬──────────┘
       │ aggregates
       ▼
┌─────────────┐
│   Context   │
└──────┬──────┘
       │ generates
       ▼
┌─────────────┐
│  Response   │───────┐
└─────────────┘       │
                      │ contains
                      ▼
               ┌─────────────┐
               │   Source    │ (0..n)
               └─────────────┘
```

---

## State Transitions

### Query Processing Flow

```
[Received] → [Embedding] → [Searching] → [Retrieved] → [Responding] → [Complete]
                                ↓
                           [No Results] → [Refusal] → [Complete]
```

### Error States

| State | Trigger | Recovery |
|-------|---------|----------|
| `EmbeddingFailed` | Cohere API error | Return user-friendly error |
| `SearchFailed` | Qdrant connection error | Return user-friendly error |
| `NoResults` | Empty retrieval | Return refusal message |
| `ContextTooLarge` | Tokens exceed limit | Truncate to top chunks |

---

## Qdrant Collection Schema (Expected)

The agent expects the existing Qdrant collection to have this schema:

```python
{
    "collection_name": "physical_ai_textbook",
    "vectors": {
        "size": 1024,  # or 1536 depending on model
        "distance": "Cosine"
    },
    "payload_schema": {
        "text": "string",
        "module": "string",
        "week": "integer",
        "chapter": "string",
        "section": "string",
        "difficulty": "string",
        "keywords": "string[]",
        "hasCode": "boolean",
        "language": "string"
    }
}
```

---

## Configuration Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `TOP_K` | 5 | Number of chunks to retrieve |
| `SIMILARITY_THRESHOLD` | 0.75 | Minimum similarity score |
| `MAX_CONTEXT_TOKENS` | 4000 | Maximum tokens in context |
| `MAX_QUERY_LENGTH` | 2000 | Maximum query characters |
