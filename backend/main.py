"""
Embedding Pipeline for RAG Retrieval

This pipeline crawls a Docusaurus documentation site, extracts text content,
generates Cohere embeddings, and stores them in Qdrant for RAG-based retrieval.

Target: https://spec-kit-hackathon.vercel.app/
Collection: rag_embedding

Usage:
    uv run python main.py
"""

import os
import hashlib
import uuid
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import time

import requests
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

# =============================================================================
# Configuration Constants
# =============================================================================

SITEMAP_URL = "https://spec-kit-hackathon.vercel.app/sitemap.xml"
COLLECTION_NAME = "rag_embedding"
CHUNK_SIZE = 1000  # characters per chunk
OVERLAP = 100  # character overlap between chunks
VECTOR_SIZE = 1024  # Cohere embed-multilingual-v3.0 dimensions
EMBEDDING_MODEL = "embed-multilingual-v3.0"
BATCH_SIZE = 96  # Cohere API batch limit
QDRANT_BATCH_SIZE = 20  # Qdrant upsert batch size
QDRANT_TIMEOUT = 60  # Qdrant client timeout in seconds
MAX_RETRIES = 3  # Maximum retry attempts for failed operations

# =============================================================================
# Logging Configuration
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# =============================================================================
# URL Discovery (User Story 1)
# =============================================================================

def get_all_urls(sitemap_url: str) -> list[str]:
    """
    Fetch and parse sitemap.xml to extract all page URLs.

    Args:
        sitemap_url: URL to the sitemap.xml file

    Returns:
        List of URLs found in the sitemap
    """
    logger.info(f"Fetching sitemap from: {sitemap_url}")

    try:
        response = requests.get(sitemap_url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch sitemap: {e}")
        return []

    # Parse XML with namespace handling
    root = ET.fromstring(response.content)
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # Extract all <loc> URLs
    urls = []
    for loc in root.findall(".//ns:loc", namespace):
        if loc.text:
            urls.append(loc.text)

    # Filter to same domain only
    base_domain = sitemap_url.split("/sitemap")[0]
    urls = [url for url in urls if url.startswith(base_domain)]

    logger.info(f"Found {len(urls)} URLs in sitemap")
    return urls


# =============================================================================
# Content Extraction (User Story 1)
# =============================================================================

def extract_text_from_urls(urls: list[str]) -> list[dict]:
    """
    Fetch each URL and extract main content, removing boilerplate.

    Args:
        urls: List of URLs to process

    Returns:
        List of documents with url, title, and content
    """
    logger.info(f"Extracting text from {len(urls)} URLs...")

    documents = []
    success_count = 0
    failure_count = 0

    for i, url in enumerate(urls, 1):
        try:
            logger.info(f"[{i}/{len(urls)}] Processing: {url}")

            response = requests.get(url, timeout=120)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script and style tags
            for tag in soup.find_all(["script", "style"]):
                tag.decompose()

            # Remove navigation, footer, sidebar, header
            for tag in soup.find_all(["nav", "footer", "aside", "header"]):
                tag.decompose()

            # Extract main content using Docusaurus-friendly selectors
            main_content = None
            for selector in ["article", ".markdown", ".theme-doc-markdown", "main"]:
                if selector.startswith("."):
                    main_content = soup.find(class_=selector[1:])
                else:
                    main_content = soup.find(selector)
                if main_content:
                    break

            # Fallback to body if no selector matches
            if not main_content:
                main_content = soup.body

            # Extract text content
            content = ""
            if main_content:
                content = main_content.get_text(separator="\n", strip=True)
                # Normalize whitespace
                content = " ".join(content.split())

            # Extract title
            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            else:
                title = url.split("/")[-1] or "Untitled"

            # Skip pages with insufficient content
            if len(content) < 100:
                logger.warning(f"Skipping {url} - insufficient content ({len(content)} chars)")
                continue

            documents.append({
                "url": url,
                "title": title,
                "content": content
            })
            success_count += 1

        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            failure_count += 1
            continue
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            failure_count += 1
            continue

    logger.info(f"Extraction complete: {success_count} successful, {failure_count} failed")
    return documents


# =============================================================================
# Text Chunking (User Story 2)
# =============================================================================

def chunk_text(
    documents: list[dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP
) -> list[dict]:
    """
    Split documents into overlapping chunks for embedding.

    Args:
        documents: List of documents with url, title, content
        chunk_size: Maximum characters per chunk
        overlap: Character overlap between chunks

    Returns:
        List of chunks with text, source_url, title, chunk_index
    """
    logger.info(f"Chunking {len(documents)} documents (size={chunk_size}, overlap={overlap})...")

    chunks = []

    for doc in documents:
        text = doc["content"]
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            # Skip empty or whitespace-only chunks
            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "source_url": doc["url"],
                    "title": doc["title"],
                    "chunk_index": chunk_index
                })
                chunk_index += 1

            # Move start position with overlap
            start += chunk_size - overlap

            # Prevent infinite loop on very small texts
            if chunk_size - overlap <= 0:
                break

    logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks


# =============================================================================
# Embedding Generation (User Story 2)
# =============================================================================

def embed(chunks: list[dict], cohere_client: cohere.Client) -> list[list[float]]:
    """
    Generate Cohere embeddings for all chunks.

    Args:
        chunks: List of chunks with text field
        cohere_client: Initialized Cohere client

    Returns:
        List of embedding vectors (1024 dimensions each)
    """
    logger.info(f"Generating embeddings for {len(chunks)} chunks...")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = []

    # Process in batches (Cohere limit is 96)
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(texts) + BATCH_SIZE - 1) // BATCH_SIZE

        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} texts)")

        try:
            response = cohere_client.embed(
                texts=batch,
                model=EMBEDDING_MODEL,
                input_type="search_document"
            )
            embeddings.extend(response.embeddings)
        except Exception as e:
            logger.error(f"Embedding batch {batch_num} failed: {e}")
            # Skip failed batch, log error, continue
            # Add empty embeddings to maintain index alignment
            embeddings.extend([None] * len(batch))
            continue

    # Filter out failed embeddings and their corresponding chunks
    valid_embeddings = [e for e in embeddings if e is not None]
    logger.info(f"Generated {len(valid_embeddings)} embeddings successfully")

    return embeddings


# =============================================================================
# Qdrant Collection Management (User Story 3)
# =============================================================================

def create_collection(
    qdrant_client: QdrantClient,
    collection_name: str = COLLECTION_NAME
) -> None:
    """
    Create Qdrant collection if it doesn't exist.

    Args:
        qdrant_client: Initialized Qdrant client
        collection_name: Name of the collection to create
    """
    logger.info(f"Checking Qdrant collection: {collection_name}")

    try:
        collections = qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]

        if collection_name in collection_names:
            logger.info(f"Collection '{collection_name}' already exists, skipping creation")
            return

        # Create collection with correct vector configuration
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        logger.info(f"Created collection '{collection_name}' with {VECTOR_SIZE} dimensions")

    except Exception as e:
        logger.error(f"Failed to create collection: {e}")
        raise


# =============================================================================
# Vector Storage (User Story 3)
# =============================================================================

def save_chunk_to_qdrant(
    qdrant_client: QdrantClient,
    chunks: list[dict],
    embeddings: list[list[float]],
    collection_name: str = COLLECTION_NAME
) -> int:
    """
    Upsert embeddings with metadata to Qdrant in batches with retry logic.

    Args:
        qdrant_client: Initialized Qdrant client
        chunks: List of chunks with metadata
        embeddings: List of embedding vectors
        collection_name: Target collection name

    Returns:
        Number of points successfully stored
    """
    logger.info(f"Saving {len(chunks)} vectors to Qdrant collection '{collection_name}'...")

    points = []
    timestamp = datetime.now(timezone.utc).isoformat()

    for chunk, embedding in zip(chunks, embeddings):
        # Skip if embedding failed
        if embedding is None:
            continue

        # Generate deterministic UUID from source_url + chunk_index
        id_content = f"{chunk['source_url']}:{chunk['chunk_index']}"
        point_id = str(uuid.UUID(bytes=hashlib.md5(id_content.encode()).digest()))

        points.append(PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "source_url": chunk["source_url"],
                "title": chunk["title"],
                "chunk_text": chunk["text"],
                "chunk_index": chunk["chunk_index"],
                "timestamp": timestamp
            }
        ))

    if not points:
        logger.warning("No valid points to store")
        return 0

    # Batch upsert with retry logic
    total_stored = 0
    total_batches = (len(points) + QDRANT_BATCH_SIZE - 1) // QDRANT_BATCH_SIZE

    for i in range(0, len(points), QDRANT_BATCH_SIZE):
        batch = points[i:i + QDRANT_BATCH_SIZE]
        batch_num = i // QDRANT_BATCH_SIZE + 1

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"Upserting batch {batch_num}/{total_batches} ({len(batch)} points), attempt {attempt}")
                qdrant_client.upsert(
                    collection_name=collection_name,
                    points=batch
                )
                total_stored += len(batch)
                logger.info(f"Batch {batch_num} stored successfully")
                break  # Success, move to next batch

            except Exception as e:
                logger.warning(f"Batch {batch_num} attempt {attempt} failed: {e}")
                if attempt < MAX_RETRIES:
                    wait_time = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Batch {batch_num} failed after {MAX_RETRIES} attempts, skipping")

    logger.info(f"Successfully stored {total_stored}/{len(points)} vectors")
    return total_stored


# =============================================================================
# Main Pipeline (User Story 4)
# =============================================================================

def main():
    """Execute the full embedding pipeline."""

    logger.info("=" * 60)
    logger.info("Starting Embedding Pipeline for RAG Retrieval")
    logger.info("=" * 60)

    # Load environment variables
    load_dotenv()

    # Validate environment
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not cohere_api_key:
        logger.error("COHERE_API_KEY not set in environment")
        return

    if not qdrant_url:
        logger.error("QDRANT_URL not set in environment")
        return

    # Initialize clients
    logger.info("Initializing Cohere client...")
    cohere_client = cohere.Client(cohere_api_key)

    logger.info(f"Initializing Qdrant client ({qdrant_url})...")
    qdrant_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key if qdrant_api_key else None,
        timeout=QDRANT_TIMEOUT
    )

    # Step 1: Create Qdrant collection
    logger.info("-" * 40)
    logger.info("Step 1: Creating Qdrant collection")
    create_collection(qdrant_client, COLLECTION_NAME)

    # Step 2: Fetch URLs from sitemap
    logger.info("-" * 40)
    logger.info("Step 2: Fetching URLs from sitemap")
    urls = get_all_urls(SITEMAP_URL)

    if not urls:
        logger.error("No URLs found in sitemap. Exiting.")
        return

    # Step 3: Extract text from URLs
    logger.info("-" * 40)
    logger.info("Step 3: Extracting text from URLs")
    documents = extract_text_from_urls(urls)

    if not documents:
        logger.error("No documents extracted. Exiting.")
        return

    # Step 4: Chunk text
    logger.info("-" * 40)
    logger.info("Step 4: Chunking documents")
    chunks = chunk_text(documents, CHUNK_SIZE, OVERLAP)

    if not chunks:
        logger.error("No chunks created. Exiting.")
        return

    # Step 5: Generate embeddings
    logger.info("-" * 40)
    logger.info("Step 5: Generating embeddings")
    embeddings = embed(chunks, cohere_client)

    # Step 6: Store in Qdrant
    logger.info("-" * 40)
    logger.info("Step 6: Storing vectors in Qdrant")
    stored_count = save_chunk_to_qdrant(qdrant_client, chunks, embeddings, COLLECTION_NAME)

    # Final statistics report
    logger.info("=" * 60)
    logger.info("Pipeline Complete!")
    logger.info("=" * 60)
    logger.info(f"Statistics:")
    logger.info(f"  - URLs found: {len(urls)}")
    logger.info(f"  - Documents extracted: {len(documents)}")
    logger.info(f"  - Chunks created: {len(chunks)}")
    logger.info(f"  - Embeddings generated: {len([e for e in embeddings if e is not None])}")
    logger.info(f"  - Vectors stored: {stored_count}")
    logger.info(f"  - Collection: {COLLECTION_NAME}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
