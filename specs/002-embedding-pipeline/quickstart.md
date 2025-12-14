# Quickstart: Embedding Pipeline

**Feature**: 002-embedding-pipeline
**Time to Complete**: ~10 minutes

## Prerequisites

- Python 3.10+
- Cohere API key (https://dashboard.cohere.com/api-keys)
- Qdrant instance (local Docker or Qdrant Cloud)

## Step 1: Install UV Package Manager

```bash
pip install uv
```

## Step 2: Create Project Structure

```bash
mkdir backend
cd backend
uv init
```

## Step 3: Install Dependencies

```bash
uv add requests beautifulsoup4 cohere qdrant-client python-dotenv
```

## Step 4: Configure Environment

Create `.env` file in `backend/`:

```env
COHERE_API_KEY=your-cohere-api-key-here
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-api-key-if-cloud
```

For local Qdrant:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

## Step 5: Run the Pipeline

```bash
uv run python main.py
```

## Expected Output

```text
[INFO] Fetching URLs from sitemap...
[INFO] Found 25 URLs
[INFO] Extracting text from URLs...
[INFO] Extracted 25 documents
[INFO] Chunking documents...
[INFO] Created 150 chunks
[INFO] Generating embeddings...
[INFO] Generated 150 embeddings
[INFO] Creating Qdrant collection 'rag_embeded'...
[INFO] Saving to Qdrant...
[INFO] Pipeline complete!
[INFO] Stats: 25 pages, 150 chunks, 150 vectors stored
```

## Verify Results

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
info = client.get_collection("rag_embeded")
print(f"Vectors stored: {info.points_count}")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `COHERE_API_KEY not set` | Add key to `.env` file |
| `Connection refused` on Qdrant | Start Docker container or check URL |
| `Rate limit exceeded` | Wait 60 seconds, retry |
| `Empty content extracted` | Check if site requires JavaScript |
