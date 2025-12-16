# Chatbot API Deployment Guide

This guide explains how to deploy the Physical AI Textbook chatbot API to Vercel.

## Architecture

- **agent/api.py** - FastAPI server that exposes the RAG chatbot via HTTP endpoints
- **agent/main.py** - RAG agent logic using Groq (Llama), Cohere, and Qdrant
- **Deployment** - Vercel serverless functions

## Prerequisites

1. **Vercel Account** - Sign up at https://vercel.com
2. **API Keys**:
   - Groq API key (for Llama model)
   - Cohere API key (for embeddings)
   - Qdrant URL and API key (for vector database)

## Deployment Steps

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Set Environment Variables in Vercel

Go to your Vercel project settings and add these environment variables:

```
GROQ_API_KEY=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

Alternatively, use the CLI:

```bash
vercel env add GROQ_API_KEY
vercel env add COHERE_API_KEY
vercel env add QDRANT_URL
vercel env add QDRANT_API_KEY
```

### 3. Deploy to Vercel

```bash
# From the project root directory
vercel

# For production deployment
vercel --prod
```

### 4. Update CORS Origins

After deployment, update the `allow_origins` in `agent/api.py` to include your Vercel deployment URL:

```python
allow_origins=[
    "https://your-deployment-url.vercel.app",
    "https://physical-ai-textbook.vercel.app",
    "http://localhost:3000",
],
```

Then redeploy.

## API Endpoints

Once deployed, your API will be available at:

- **POST /chat** - Send questions and receive AI responses
- **GET /health** - Health check endpoint

### Example Request

```bash
curl -X POST https://your-api.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is ROS 2?",
    "history": []
  }'
```

### Example Response

```json
{
  "response": "ROS 2 is a robotic middleware framework..."
}
```

## Local Testing

To test locally before deployment:

```bash
# Install dependencies
cd agent
pip install -r requirements.txt

# Create .env file with your API keys
echo "GROQ_API_KEY=your_key" > .env
echo "COHERE_API_KEY=your_key" >> .env
echo "QDRANT_URL=your_url" >> .env
echo "QDRANT_API_KEY=your_key" >> .env

# Run the API server
python api.py

# Test in another terminal
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

## CLI Usage (Local Only)

The CLI interface in `agent/main.py` is for local development and testing:

```bash
cd agent
python main.py
```

This provides an interactive chat interface that connects directly to the RAG agent.

## Troubleshooting

### Issue: "Connection to Qdrant failed"
- Verify your QDRANT_URL and QDRANT_API_KEY are correct
- Ensure the `rag_embedding` collection exists in your Qdrant instance
- Run `backend/main.py` to populate the vector database if needed

### Issue: "Module not found"
- Check that `agent/requirements.txt` includes all dependencies
- Vercel automatically installs dependencies from requirements.txt

### Issue: "Timeout errors"
- Vercel serverless functions have a 10-second timeout on the Hobby plan
- Consider upgrading to Pro plan for 60-second timeout
- Optimize your RAG query to retrieve fewer chunks (reduce TOP_K in main.py)

## Project Structure

```
physical-ai-and-robotics-book-chatbot/
├── agent/
│   ├── api.py              # FastAPI server (deployed to Vercel)
│   ├── main.py             # RAG agent logic
│   └── requirements.txt    # Python dependencies
├── backend/
│   └── main.py             # Embedding pipeline (run locally)
├── vercel.json             # Vercel deployment configuration
└── DEPLOYMENT.md           # This file
```

## Next Steps

1. Deploy the API to Vercel
2. Integrate the API with your floating chatbot frontend
3. Monitor usage and performance in Vercel dashboard
4. Update the vector database periodically by running `backend/main.py`

## Support

For issues or questions, refer to:
- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Groq API Docs: https://console.groq.com/docs
