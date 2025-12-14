# Data Model: Embedding Pipeline

**Feature**: 002-embedding-pipeline
**Date**: 2025-12-14

## Entities

### 1. Document (In-Memory)

Represents a single crawled page before chunking.

```python
@dataclass
class Document:
    url: str           # Source URL
    title: str         # Page title from <title> or <h1>
    content: str       # Cleaned text content
    crawled_at: str    # ISO timestamp
```

**Lifecycle**: Created during extraction → Consumed during chunking → Discarded

### 2. Chunk (In-Memory)

A segment of document text ready for embedding.

```python
@dataclass
class Chunk:
    text: str          # Chunk content (max ~1500 chars)
    source_url: str    # Origin document URL
    title: str         # Origin document title
    chunk_index: int   # Position in document (0-based)
```

**Lifecycle**: Created during chunking → Consumed during embedding → Discarded

### 3. VectorRecord (Qdrant)

Stored item in Qdrant vector database.

```python
# Qdrant Point structure
{
    "id": str,           # UUID or hash of source_url + chunk_index
    "vector": list[float],  # 1024-dimensional Cohere embedding
    "payload": {
        "source_url": str,
        "title": str,
        "chunk_text": str,
        "chunk_index": int
    }
}
```

**Persistence**: Stored in Qdrant collection "rag_embeded"

## Qdrant Collection Schema

**Collection Name**: `rag_embeded`

```python
# Collection configuration
{
    "vectors": {
        "size": 1024,
        "distance": "Cosine"
    },
    "payload_schema": {
        "source_url": "keyword",    # Filterable
        "title": "text",            # Searchable
        "chunk_text": "text",       # Searchable
        "chunk_index": "integer"    # Sortable
    }
}
```

## Data Flow

```text
┌─────────────────────────────────────────────────────────────────┐
│                        SITEMAP                                   │
│  https://spec-kit-hackathon.vercel.app/sitemap.xml              │
└─────────────────────┬───────────────────────────────────────────┘
                      │ get_all_urls()
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      URL LIST                                    │
│  [url1, url2, url3, ...]                                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │ extract_text_from_urls()
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DOCUMENTS                                   │
│  [{url, title, content, crawled_at}, ...]                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │ chunk_text()
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CHUNKS                                     │
│  [{text, source_url, title, chunk_index}, ...]                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │ embed()
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EMBEDDINGS                                   │
│  [[0.123, -0.456, ...], ...]  (1024-dim vectors)                │
└─────────────────────┬───────────────────────────────────────────┘
                      │ save_chunk_to_qdrant()
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QDRANT COLLECTION                             │
│  Collection: "rag_embeded"                                       │
│  Points: [{id, vector, payload}, ...]                           │
└─────────────────────────────────────────────────────────────────┘
```

## ID Generation Strategy

For deduplication, generate deterministic IDs:

```python
def generate_id(source_url: str, chunk_index: int) -> str:
    """Generate deterministic UUID from URL + index."""
    import hashlib
    import uuid
    content = f"{source_url}:{chunk_index}"
    hash_bytes = hashlib.md5(content.encode()).digest()
    return str(uuid.UUID(bytes=hash_bytes))
```

This ensures:
- Same URL + chunk_index always produces same ID
- Re-indexing updates existing vectors (upsert behavior)
- No duplicate vectors for same content
