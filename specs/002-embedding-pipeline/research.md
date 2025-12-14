# Research: Embedding Pipeline for RAG Retrieval

**Feature**: 002-embedding-pipeline
**Date**: 2025-12-14
**Status**: Complete

## Technology Decisions

### 1. Package Manager: UV

**Decision**: Use UV (Astral's fast Python package manager)

**Rationale**:
- 10-100x faster than pip for dependency resolution
- Built-in virtual environment management
- Lockfile support for reproducibility
- Drop-in replacement for pip commands

**Alternatives Considered**:
- pip + venv: Slower, but more widely known
- Poetry: Heavier, more complex for simple projects
- PDM: Good but less ecosystem adoption than UV

**Implementation**:
```bash
# Install UV
pip install uv

# Initialize project
uv init

# Add dependencies
uv add requests beautifulsoup4 cohere qdrant-client python-dotenv
```

### 2. Web Scraping: requests + BeautifulSoup4

**Decision**: Use requests for HTTP + BeautifulSoup4 for HTML parsing

**Rationale**:
- Lightweight, no browser overhead
- Docusaurus generates static HTML (no JS rendering needed)
- BeautifulSoup excels at content extraction
- Well-documented, stable libraries

**Alternatives Considered**:
- Scrapy: Overkill for single-site crawling
- Playwright/Selenium: Unnecessary for static HTML
- httpx: Good async option but sync is sufficient

### 3. Text Chunking: Manual Implementation

**Decision**: Implement simple character-based chunking with overlap

**Rationale**:
- Single-file constraint requires minimal dependencies
- ~500 tokens ≈ ~2000 characters for English text
- Overlap prevents context loss at boundaries

**Alternatives Considered**:
- LangChain TextSplitter: Adds heavy dependency
- tiktoken: Adds dependency for token counting
- NLTK: Overkill for simple chunking

**Implementation Strategy**:
- Chunk size: 1500 characters (~375 tokens)
- Overlap: 200 characters (~50 tokens)
- Split on paragraph boundaries where possible

### 4. Embedding Model: Cohere embed-english-v3.0

**Decision**: Use embed-english-v3.0 (1024 dimensions)

**Rationale**:
- Specified in feature spec (FR-013)
- High quality English embeddings
- 1024 dimensions balances quality vs storage

**API Details**:
- Endpoint: `cohere.embed()`
- Input type: `search_document` for indexing
- Batch size: Up to 96 texts per request
- Rate limits: 10,000 calls/minute (production)

### 5. Vector Database: Qdrant

**Decision**: Qdrant with collection "rag_embeded" (per user spec)

**Rationale**:
- Specified by user requirement
- Free tier available (Qdrant Cloud)
- Simple Python client
- Supports metadata filtering

**Configuration**:
- Collection: "rag_embeded"
- Vector size: 1024 (matching Cohere)
- Distance metric: Cosine
- Payload: source_url, title, chunk_text, chunk_index

### 6. Sitemap Parsing: xml.etree.ElementTree

**Decision**: Use Python's built-in XML parser

**Rationale**:
- No external dependency
- Sufficient for sitemap.xml parsing
- Standard library, always available

**Target Sitemap**: https://spec-kit-hackathon.vercel.app/sitemap.xml

## Architecture Summary

```text
Sitemap URL → get_all_urls() → [URLs]
                    ↓
URLs → extract_text_from_urls() → [Documents]
                    ↓
Documents → chunk_text() → [Chunks]
                    ↓
Chunks → embed() → [Embeddings]
                    ↓
Embeddings → create_collection() + save_chunk_to_qdrant() → Qdrant
```

## Dependencies (requirements.txt)

```text
requests>=2.31.0
beautifulsoup4>=4.12.0
cohere>=5.0.0
qdrant-client>=1.7.0
python-dotenv>=1.0.0
```

## Environment Variables

```text
COHERE_API_KEY=<your-cohere-api-key>
QDRANT_URL=<your-qdrant-url>
QDRANT_API_KEY=<your-qdrant-api-key>
```

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Cohere rate limits | Batch embeddings, add delays if needed |
| Large pages | Truncate to max 50,000 chars per page |
| Network failures | Retry with exponential backoff |
| Empty content | Skip pages with <100 chars content |
| Qdrant connection | Validate connection before bulk insert |
