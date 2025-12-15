# Quickstart: Book RAG Agent

**Feature Branch**: `003-book-rag-agent`
**Date**: 2025-12-15

## Prerequisites

Before starting, ensure you have:

- [ ] Python 3.10 or higher installed
- [ ] UV package manager installed (`pip install uv`)
- [ ] Gemini API key
- [ ] Cohere API key
- [ ] Access to Qdrant instance with embedded book content

---

## Setup Steps

### 1. Navigate to Agent Directory

```bash
cd agent
```

### 2. Initialize UV Project (if not exists)

```bash
uv init
```

### 3. Install Dependencies

```bash
uv add openai-agents litellm cohere qdrant-client python-dotenv
```

### 4. Create Environment File

Create `.env` file in the `agent/` directory:

```env
# LLM Provider
GEMINI_API_KEY=your_gemini_api_key_here

# Embedding Provider
COHERE_API_KEY=your_cohere_api_key_here

# Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=physical_ai_textbook
```

### 5. Verify Qdrant Connection

```bash
uv run python -c "
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()
client = QdrantClient(
    host=os.environ['QDRANT_HOST'],
    port=int(os.environ.get('QDRANT_PORT', 6333))
)
info = client.get_collection(os.environ['QDRANT_COLLECTION'])
print(f'Collection: {info.collection_name}')
print(f'Vectors count: {info.points_count}')
print(f'Vector size: {info.config.params.vectors.size}')
"
```

---

## Running the Agent

### Interactive Mode

```bash
cd agent
uv run python main.py
```

### Single Query Mode

```bash
uv run python main.py --query "What is ROS 2?"
```

---

## Example Queries

| Query | Expected Behavior |
|-------|-------------------|
| "What is Physical AI?" | Returns book definition with chapter citation |
| "How do I create a ROS 2 node?" | Returns implementation steps from ROS 2 module |
| "What is the weather today?" | Refuses - not in book scope |
| "Explain SLAM in robotics" | Returns SLAM explanation from relevant chapter |

---

## Troubleshooting

### "Unable to process your question"
- Check `COHERE_API_KEY` is valid
- Verify internet connectivity
- Check Cohere API status

### "Book content temporarily unavailable"
- Verify Qdrant is running
- Check `QDRANT_HOST` and `QDRANT_PORT`
- Verify collection exists

### "This question is not answered in the book"
- Question may be out of scope
- Try rephrasing with book-specific terminology
- Verify book content covers the topic

---

## Project Structure

```
agent/
├── main.py           # All agent code
├── pyproject.toml    # UV project config
├── uv.lock           # Dependency lockfile
└── .env              # Environment variables (not committed)
```

---

## Development Commands

```bash
# Run with verbose output
uv run python main.py --verbose

# Run tests (when available)
uv run pytest

# Update dependencies
uv sync

# Add new dependency
uv add <package-name>
```
