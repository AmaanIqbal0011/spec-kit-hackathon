# FastAPI Chat API for Book RAG Agent
# Exposes the RAG agent via HTTP endpoint for the floating chatbot

"""
Physical AI Textbook Chat API

Provides HTTP endpoints for the floating chatbot to communicate with the RAG agent.
- POST /chat: Send a question, receive an AI-generated response
- GET /health: Health check endpoint
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

# Import agent functions from main.py
from main import run_rag_query, validate_connections


# =============================================================================
# LIFESPAN HANDLER
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate connections on startup."""
    print("[ChatAPI] Starting up...")
    if not validate_connections():
        print("[ChatAPI] WARNING: Connection validation failed")
    else:
        print("[ChatAPI] Connection validation successful")
    yield
    print("[ChatAPI] Shutting down...")


# =============================================================================
# FASTAPI APP INITIALIZATION
# =============================================================================

app = FastAPI(
    title="Physical AI Textbook Chat API",
    description="API for the floating chatbot to communicate with the RAG agent",
    version="1.0.0",
    lifespan=lifespan
)

# =============================================================================
# CORS MIDDLEWARE CONFIGURATION
# =============================================================================

# Allow requests from Docusaurus frontend (both production and development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://physical-ai-textbook.vercel.app",
        "https://spec-kit-hackathon.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class Message(BaseModel):
    """A single message in the conversation history."""
    role: str = Field(
        ...,
        description="The role of the message sender",
        examples=["user", "assistant"]
    )
    content: str = Field(
        ...,
        description="The message content"
    )


class ChatRequest(BaseModel):
    """Request payload for chat endpoint."""
    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The user's question about the textbook content",
        examples=["What is ROS 2?", "How do I create a publisher node?"]
    )
    history: list[Message] = Field(
        default=[],
        description="Optional conversation history for context",
        max_length=20  # Limit history to prevent token overflow
    )


class ChatResponse(BaseModel):
    """Response payload from chat endpoint."""
    response: str = Field(
        ...,
        description="The AI agent's response to the query"
    )


class HealthResponse(BaseModel):
    """Response payload for health check endpoint."""
    status: str = Field(..., description="Current health status")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Error response payload."""
    detail: str = Field(..., description="Human-readable error message")


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        200: {"description": "Successful response from AI agent"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        503: {"model": ErrorResponse, "description": "Service unavailable"},
    },
    summary="Send a question to the AI agent",
    description="Accepts a user question, retrieves relevant context from the textbook, and returns an AI-generated response.",
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message and return the AI agent's response.

    The endpoint:
    1. Validates the request
    2. Retrieves relevant context from Qdrant
    3. Generates a response using the Groq/Llama model with conversation history
    4. Returns the formatted response
    """
    try:
        print(f"[ChatAPI] Received query: {request.query[:100]}...")
        print(f"[ChatAPI] History length: {len(request.history)} messages")

        # Convert Pydantic models to dicts for the RAG function
        history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]

        # Call the RAG query function with history (async)
        response = await run_rag_query(request.query, history=history_dicts)

        print(f"[ChatAPI] Generated response: {response[:100]}...")

        return ChatResponse(response=response)

    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        # Handle connection errors (Qdrant, Groq)
        raise HTTPException(status_code=503, detail="AI service is temporarily unavailable")
    except Exception as e:
        # Handle unexpected errors
        print(f"[ChatAPI] Error processing request: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
    description="Returns the health status of the API",
)
async def health() -> HealthResponse:
    """Return the health status of the API."""
    return HealthResponse(status="healthy", version="1.0.0")


# =============================================================================
# ENTRY POINT
# =============================================================================

# For Vercel serverless deployment
# Export the FastAPI app instance
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
