# Agent API Contract: Book RAG Agent

**Feature Branch**: `003-book-rag-agent`
**Date**: 2025-12-15

## Overview

This document defines the internal API contract for the BookRAGAgent. Since this is a CLI-based agent (not a REST API), this contract describes the function interfaces and tool signatures.

---

## Main Entry Point

### `run_agent(query: str) -> Response`

Main function to process a user query and return a response.

**Input**:
```python
query: str  # User's natural language question
```

**Output**:
```python
class Response:
    answer: str           # The agent's response text
    sources: list[Source] # List of source citations
    is_refusal: bool      # True if unable to answer
    refusal_reason: str   # Reason for refusal (if applicable)
```

**Errors**:
| Error | Description |
|-------|-------------|
| `EmbeddingError` | Failed to generate query embedding |
| `RetrievalError` | Failed to search vector database |
| `AgentError` | Agent failed to generate response |

---

## Retrieval Tool Contract

### `retrieve_book_context(query: str) -> str`

Function tool registered with the agent for retrieving book context.

**Signature** (as seen by agent):
```json
{
  "name": "retrieve_book_context",
  "description": "Retrieve relevant context from the Physical AI & Humanoid Robotics textbook for answering the query. Always call this tool before answering any question.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The user's question about the book content"
      }
    },
    "required": ["query"]
  }
}
```

**Return Format**:
```
Context from the book:

[Source: Chapter X - Section Y]
<chunk text 1>

[Source: Chapter A - Section B]
<chunk text 2>

...

If no relevant context found:
"No relevant content found in the book for this query."
```

---

## Embedding Function Contract

### `get_embedding(text: str) -> list[float]`

Generate a vector embedding for the given text.

**Input**:
```python
text: str  # Text to embed (query or document)
```

**Output**:
```python
list[float]  # Vector embedding (1024 dimensions for Cohere v3)
```

**Configuration**:
```python
{
    "model": "embed-english-v3.0",
    "input_type": "search_query",  # For user queries
    "embedding_types": ["float"]
}
```

**Errors**:
| Error | HTTP Status | Description |
|-------|-------------|-------------|
| `RateLimitError` | 429 | API rate limit exceeded |
| `InvalidInputError` | 400 | Text too long or invalid |
| `AuthenticationError` | 401 | Invalid API key |

---

## Qdrant Search Contract

### `search_vectors(embedding: list[float], top_k: int) -> list[ScoredPoint]`

Search the vector database for similar content.

**Input**:
```python
embedding: list[float]  # Query embedding vector
top_k: int = 5          # Number of results to return
```

**Output**:
```python
class ScoredPoint:
    id: str             # Unique point ID
    score: float        # Similarity score (0-1)
    payload: dict       # Metadata (chapter, section, text, etc.)
```

**Query Parameters**:
```python
{
    "collection_name": "${QDRANT_COLLECTION}",
    "query": embedding,
    "limit": top_k,
    "with_payload": True,
    "score_threshold": 0.75
}
```

---

## Agent Configuration Contract

### Agent Definition

```python
Agent(
    name="BookRAGAgent",
    instructions=SYSTEM_PROMPT,
    model=LitellmModel(
        model="gemini/gemini-2.0-flash",
        api_key="${GEMINI_API_KEY}"
    ),
    tools=[retrieve_book_context]
)
```

### System Prompt Template

```
You are BookRAGAgent, a specialized assistant that answers questions ONLY using content from the Physical AI & Humanoid Robotics textbook.

CRITICAL RULES:
1. ALWAYS call the retrieve_book_context tool before answering any question
2. ONLY use the provided retrieved context to answer questions
3. NEVER use external knowledge or make assumptions
4. NEVER hallucinate or guess information
5. If the context does not contain the answer, respond with: "This question is not answered in the book."
6. Always cite the source chapter/section when available
7. Keep answers concise and accurate to the book's content

When answering:
- Quote or paraphrase the retrieved content faithfully
- Include chapter/section references in your response
- If multiple sources are relevant, synthesize them coherently
```

---

## Environment Variables Contract

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Gemini API authentication |
| `COHERE_API_KEY` | Yes | - | Cohere API authentication |
| `QDRANT_HOST` | Yes | - | Qdrant server hostname |
| `QDRANT_PORT` | No | 6333 | Qdrant server port |
| `QDRANT_COLLECTION` | Yes | - | Collection name |

---

## Error Response Format

All errors follow this format for user display:

```python
class ErrorResponse:
    message: str      # User-friendly error message
    error_type: str   # Error category
    recoverable: bool # Whether user can retry
```

**Standard Error Messages**:

| Error Type | User Message |
|------------|--------------|
| `EmbeddingError` | "Unable to process your question. Please try again." |
| `RetrievalError` | "Book content temporarily unavailable. Please try again." |
| `NoContextError` | "This question is not answered in the book." |
| `InvalidQueryError` | "Please provide a question about the book content." |
