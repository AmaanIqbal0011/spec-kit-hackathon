# Book RAG Agent - main.py
# All agent code consolidated in this single file
# Uses OpenAI-compatible endpoint for Gemini, NOT LiteLLM

"""
BookRAGAgent: A RAG-based chatbot that answers questions exclusively from book content.

This agent retrieves relevant context from a Qdrant vector database and generates
answers strictly grounded in that content, ensuring zero hallucination.

Code Structure:
- OpenAIChatCompletionsModel with AsyncOpenAI (Gemini via OpenAI-compatible endpoint)
- Runner.run_sync for synchronous execution
- @function_tool decorator for retrieval tool
- Cohere for embeddings only
- Qdrant for vector search
"""

# =============================================================================
# 1. IMPORTS (T015-T021)
# =============================================================================

import os
import sys

# Agent SDK imports
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents import OpenAIChatCompletionsModel

# OpenAI client for Gemini
from openai import AsyncOpenAI

# External clients
import cohere
from qdrant_client import QdrantClient

# Environment
from dotenv import load_dotenv


# =============================================================================
# 2. ENVIRONMENT SETUP (T022-T024)
# =============================================================================

# Load environment variables from .env file
load_dotenv()

# Enable verbose stdout logging
print("[BookRAGAgent] Starting up...")

# Disable tracing explicitly (T024)
set_tracing_disabled(True)

# =============================================================================
# 3. CONFIGURATION CONSTANTS
# =============================================================================

# RAG Configuration
TOP_K = 5  # Number of chunks to retrieve (T047)
QDRANT_COLLECTION = "rag_embedding"  # Book collection name (T035)

# Gemini OpenAI-compatible endpoint
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# =============================================================================
# 4. ENVIRONMENT VARIABLE LOADING (T025, T029, T032-T033)
# =============================================================================

# Gemini API Key (T025)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable is not set.")
    sys.exit(1)

# Cohere API Key (T029)
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
if not COHERE_API_KEY:
    print("ERROR: COHERE_API_KEY environment variable is not set.")
    sys.exit(1)

# Qdrant Configuration (T032-T033)
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
if not QDRANT_URL or not QDRANT_API_KEY:
    print("ERROR: QDRANT_URL and QDRANT_API_KEY environment variables must be set.")
    sys.exit(1)

# =============================================================================
# 5. GEMINI MODEL PROVIDER SETUP (T026-T028)
# =============================================================================

# Initialize AsyncOpenAI client with Gemini's OpenAI-compatible endpoint (T026)
groq_client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_BASE_URL
)

# Create OpenAIChatCompletionsModel with Groq model (T027-T028)
# Using llama-3.3-70b-versatile for tool calling support
model = OpenAIChatCompletionsModel(
    model='llama-3.3-70b-versatile',
    openai_client=groq_client
)

print("[BookRAGAgent] Gemini model provider initialized (OpenAI-compatible endpoint)")

# =============================================================================
# 6. EXTERNAL CLIENT INITIALIZATION (T030-T034, T036)
# =============================================================================

# Initialize Cohere client - ONLY for embeddings (T030-T031)
# NOTE: Cohere is restricted to embedding generation only
cohere_client = cohere.Client(api_key=COHERE_API_KEY)

# Initialize Qdrant client (T034)
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)


def validate_connections() -> bool:
    """Validate connectivity to Qdrant service (T036)."""
    try:
        # Test Qdrant connection
        collection_info = qdrant_client.get_collection(QDRANT_COLLECTION)
        print(f"[BookRAGAgent] Connected to Qdrant collection: {QDRANT_COLLECTION}")
        print(f"[BookRAGAgent]   Vectors count: {collection_info.points_count}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to connect to Qdrant: {e}")
        return False


# =============================================================================
# 7. EMBEDDING FUNCTION (T037-T042)
# =============================================================================

def get_embedding(text: str) -> list[float]:
    """
    Generate a vector embedding for the given text using Cohere (T037).

    Args:
        text: The text to embed (query)

    Returns:
        Vector embedding as a list of floats

    Raises:
        Exception: If embedding generation fails
    """
    # Strip whitespace from input (T040)
    text = text.strip()

    if not text:
        raise ValueError("Cannot generate embedding for empty text")

    try:
        # Use Cohere embed-multilingual-v3.0 model with search_query input type (T038-T039)
        response = cohere_client.embed(
            texts=[text],
            model="embed-multilingual-v3.0",
            input_type="search_query",

        )
        # Return single embedding vector (T041)
        return response.embeddings[0]
    except Exception as e:
        # Error handling for Cohere API failures (T042)
        raise Exception(f"Failed to generate embedding: {e}")


# =============================================================================
# 8. RETRIEVAL FUNCTION (T043-T050, T067-T068, T073-T075)
# =============================================================================

def do_retrieve(query: str) -> str:
    """
    Retrieve relevant content from the Physical AI & Humanoid Robotics textbook (T043).

    This tool searches the book's vector database for content relevant to the query
    and returns formatted text with source citations.

    Args:
        query: The user's question about the book content (T044)

    Returns:
        Relevant text excerpts from the book with source citations,
        or a message indicating no relevant content was found.
    """
    try:
        # Generate query embedding using Cohere (T045)
        embedding = get_embedding(query)

        # Query Qdrant using vector similarity search (T046)
        results = qdrant_client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=embedding,
            limit=TOP_K,  # Limit to TOP_K=5 chunks (T047)
            with_payload=True
        )

        # Empty result detection (T067)
        if not results.points:
            # Return fallback message when no chunks retrieved (T068)
            return "No relevant content found in the book."

        # Format results with citations (T048-T049, T073-T075)
        chunks = []
        for r in results.points:
            # Extract metadata from Qdrant payload (T074)
            title = r.payload.get("title", "Unknown")  # Handle missing (T075)
            source_url = r.payload.get("source_url", "Unknown")  # Handle missing (T075)
            # Try both 'chunk_text' and 'text' field names
            text = r.payload.get("chunk_text", r.payload.get("text", ""))  # Extract text field (T048)

            # Format with source citation prefix (T073)
            chunks.append(f"[Source: {title}]\n{text}")

        # Return retrieved text chunks as formatted string (T049)
        return "\n\n".join(chunks)

    except Exception as e:
        # Error handling for Qdrant search failures (T050)
        return f"Error retrieving context: {str(e)}"


# Create function_tool wrapper for agent-based usage (if needed)
@function_tool
def retrieve(query: str) -> str:
    """Retrieve relevant content from the book."""
    return do_retrieve(query)


# =============================================================================
# 9. AGENT INSTRUCTIONS (T051-T055, T069, T076)
# =============================================================================

# Define INSTRUCTIONS constant as multiline string (T051)
INSTRUCTIONS = """You are BookRAGAgent, a specialized assistant for the Physical AI & Humanoid Robotics textbook.

CORE BEHAVIOR:
- You are a polite, calm, and helpful textbook assistant
- Your primary role is to answer questions strictly from the book using retrieved context

CRITICAL RULES:
1. You are BOOK-SPECIFIC – you ONLY answer questions related to this textbook 
2. You MUST call the retrieve tool FIRST before answering any textbook-related question 
3. You MUST use ONLY the retrieved content to answer – NEVER use external knowledge 
4. You MUST NOT hallucinate, guess, or infer beyond the retrieved context
5. You MUST include source citations (chapter/section) when available 

CONTEXT HANDLING:
- If retrieved context is EMPTY or NOT RELEVANT:
  - Respond politely and warmly
  - Say something like:
    "I’m sorry, I couldn’t find this information in the textbook, so I don’t know."
  - Do NOT attempt to answer beyond the book 

GREETING & SMALL TALK HANDLING:
- If the user greets you (e.g., "hi", "hello", "assalam o alaikum"):
  - You MAY respond warmly and politely
  - Example:
    "Hello! I’m here to help you with questions from the Physical AI & Humanoid Robotics textbook."
- Greetings do NOT require calling the retrieve tool

ANSWERING GUIDELINES:
- Always base answers on retrieved content
- Quote or faithfully paraphrase the retrieved text
- Add citations like:
  [Source: Chapter X – Section Y]
- If multiple sections are used, synthesize them clearly and cite all relevant sources
- Keep answers concise, accurate, and strictly aligned with the book

REFUSAL POLICY:
- If a question is outside the scope of the textbook:
  - Respond politely:
    "I don’t know – this question is not answered in the book."

REMEMBER:
- Book first, context first, accuracy always
- Be respectful and friendly, but never break textbook boundaries"""


# =============================================================================
# 10. AGENT CONSTRUCTION (T056-T059)
# =============================================================================

# Create Agent instance with name "BookRAGAgent" (T056)
agent = Agent(
    name="BookRAGAgent",
    instructions=INSTRUCTIONS,  # Attach instructions (T057)
    model=model,  # Attach Gemini-backed OpenAIChatCompletionsModel (T058)
    tools=[retrieve]  # Register retrieve as the only tool (T059)
)

print("[BookRAGAgent] Agent constructed with retrieve tool")


# =============================================================================
# 11. CONVERSATION HISTORY SUPPORT
# =============================================================================

# Type alias for conversation history
# Each message is a dict with 'role' ('user' or 'assistant') and 'content'
ConversationHistory = list[dict[str, str]]


def format_history_for_prompt(history: ConversationHistory, max_turns: int = 5) -> str:
    """
    Format conversation history into a string for the prompt.

    Args:
        history: List of previous messages
        max_turns: Maximum number of conversation turns to include (default: 5)

    Returns:
        Formatted string of conversation history
    """
    if not history:
        return ""

    # Take only the last N turns (each turn = user + assistant)
    recent_history = history[-(max_turns * 2):]

    formatted = []
    for msg in recent_history:
        role = "User" if msg.get("role") == "user" else "Assistant"
        content = msg.get("content", "")
        formatted.append(f"{role}: {content}")

    return "\n".join(formatted)


async def run_rag_query(query: str, history: ConversationHistory = None) -> str:
    """
    Run RAG query with conversation history support.

    Args:
        query: The user's current question
        history: Optional list of previous messages in the conversation

    Returns:
        The AI agent's response
    """
    if history is None:
        history = []

    # Step 1: Retrieve context based on both current query and recent context
    print("[BookRAGAgent] Retrieving context...")

    # If there's history, enhance the retrieval query with recent context
    if history and len(history) >= 2:
        # Get the last assistant response for context
        last_response = ""
        for msg in reversed(history):
            if msg.get("role") == "assistant":
                last_response = msg.get("content", "")[:200]  # First 200 chars
                break

        # Create enhanced query for better retrieval
        enhanced_query = f"{query}"
        if last_response:
            # Add context hint for follow-up questions
            enhanced_query = f"Context: {last_response[:100]}... Question: {query}"
    else:
        enhanced_query = query

    context = do_retrieve(enhanced_query)

    # Step 2: Format conversation history
    history_text = format_history_for_prompt(history)

    # Step 3: Build prompt with context and history
    if history_text:
        augmented_prompt = f"""You are a helpful assistant for the Physical AI & Humanoid Robotics textbook.

CONVERSATION HISTORY:
{history_text}

RETRIEVED CONTEXT FROM BOOK:
{context}

CURRENT USER QUESTION: {query}

INSTRUCTIONS:
- Use the conversation history to understand follow-up questions and maintain context
- Answer based on the retrieved context from the book
- If the context doesn't contain relevant information, say "I don't know - this question is not answered in the book."
- Reference previous parts of the conversation when relevant
- Include source citations when available
- Be concise, accurate, and conversational"""
    else:
        augmented_prompt = f"""Based on the following context from the Physical AI & Humanoid Robotics textbook, answer the user's question.

CONTEXT:
{context}

USER QUESTION: {query}

INSTRUCTIONS:
- Answer ONLY based on the context provided above
- If the context says "No relevant content found", respond with "I don't know - this question is not answered in the book."
- Include source citations when available
- Be concise and accurate"""

    # Step 4: Create a simple agent without tools for generation
    generation_agent = Agent(
        name="BookRAGGenerator",
        instructions="You are a helpful assistant that answers questions based only on the provided context. Never use external knowledge. Maintain conversational continuity when history is provided.",
        model=model,
        tools=[]  # No tools - just generate
    )

    # Step 5: Run generation (async)
    result = await Runner.run(generation_agent, augmented_prompt)
    return result.final_output


def main():
    """Main entry point for the Book RAG Agent CLI (T060)."""
    print("=" * 60)
    print("BookRAGAgent - Physical AI & Humanoid Robotics Textbook Q&A")
    print("=" * 60)
    print("Ask questions about the book. Type 'quit' or 'exit' to stop.")
    print()

    # Validate connections before starting
    if not validate_connections():
        print("Failed to validate connections. Exiting.")
        sys.exit(1)

    print()

    while True:
        try:
            # Get user input
            query = input("You: ").strip()

            if not query:
                continue

            if query.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            print("[BookRAGAgent] Processing query...")

            # Use RAG pipeline (retrieve then generate)
            response = run_rag_query(query)

            # Print the response
            print(f"\nBookRAGAgent: {response}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


# Entry point (T064)
if __name__ == "__main__":
    main()
