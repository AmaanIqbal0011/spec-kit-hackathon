# Quickstart: Floating AI Chatbot

**Feature**: 004-floating-chatbot
**Date**: 2025-12-16

---

## Overview

This feature adds a floating AI chatbot button to the Physical AI & Robotics Docusaurus book. The chatbot communicates with the existing RAG agent via a FastAPI endpoint.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Docusaurus Frontend                          │
│                   (physical-ai-textbook/)                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  src/theme/Root.js (swizzled)                           │    │
│  │  └── <ChatbotProvider>                                  │    │
│  │       ├── <FloatingButton />  (bottom-right, fixed)     │    │
│  │       └── <ChatPanel />       (overlay when open)       │    │
│  └─────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │ POST /chat
                             │ {"query": "..."}
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                              │
│                       (agent/api.py)                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  /chat endpoint                                         │    │
│  │  └── retrieve_context() → Qdrant                        │    │
│  │  └── run_agent() → Groq/Llama                           │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Files

### Frontend (Docusaurus)

| File | Purpose |
|------|---------|
| `physical-ai-textbook/src/theme/Root.js` | Swizzled root component, injects chatbot globally |
| `physical-ai-textbook/src/components/Chatbot/index.js` | Main chatbot component |
| `physical-ai-textbook/src/components/Chatbot/FloatingButton.js` | Floating button UI |
| `physical-ai-textbook/src/components/Chatbot/ChatPanel.js` | Chat panel with messages |
| `physical-ai-textbook/src/components/Chatbot/ChatMessage.js` | Individual message component |
| `physical-ai-textbook/src/components/Chatbot/styles.module.css` | Component styles |
| `physical-ai-textbook/src/components/Chatbot/api.js` | Backend communication |

### Backend (FastAPI)

| File | Purpose |
|------|---------|
| `agent/api.py` | FastAPI app with /chat endpoint |
| `agent/main.py` | Existing agent logic (reused) |

---

## Quick Setup

### 1. Frontend Setup

```bash
cd physical-ai-textbook

# Swizzle Root component (one-time)
npm run swizzle @docusaurus/theme-classic Root -- --wrap

# Create component directory
mkdir -p src/components/Chatbot

# Start development server
npm start
```

### 2. Backend Setup

```bash
cd agent

# Install dependencies (if not already)
uv sync

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run FastAPI server
uvicorn api:app --reload --port 8000
```

### 3. Environment Variables

**Frontend** (`physical-ai-textbook/.env`):
```
REACT_APP_CHAT_API_URL=http://localhost:8000
```

**Backend** (`agent/.env`):
```
QDRANT_API_KEY=your_qdrant_key
QDRANT_URL=your_qdrant_url
COHERE_API_KEY=your_cohere_key
GROQ_API_KEY=your_groq_key
```

---

## API Contract

### POST /chat

**Request**:
```json
{
  "query": "What is ROS 2?"
}
```

**Response**:
```json
{
  "response": "ROS 2 is a flexible framework for writing robot software..."
}
```

**Error Response**:
```json
{
  "detail": "Error description"
}
```

---

## Component Structure

```jsx
// Simplified component hierarchy

<Root>                          // Swizzled Docusaurus root
  <ChatbotProvider>             // State management context
    <OriginalRoot />            // Original Docusaurus content
    <FloatingButton />          // Fixed position button
    <ChatPanel>                 // Overlay panel (when open)
      <MessageList>
        <ChatMessage />         // User messages
        <ChatMessage />         // AI messages
      </MessageList>
      <InputArea>
        <TextInput />
        <SendButton />
      </InputArea>
    </ChatPanel>
  </ChatbotProvider>
</Root>
```

---

## State Management

```javascript
// Chat state shape
const chatState = {
  isOpen: false,           // Panel visibility
  messages: [],            // Array of { id, content, sender, timestamp }
  inputValue: '',          // Current input
  isLoading: false,        // Waiting for response
  error: null,             // Error message
};

// Actions
const actions = {
  togglePanel: () => {},
  sendMessage: (content) => {},
  clearError: () => {},
  retryLastMessage: () => {},
};
```

---

## Styling Guide

### Theme Variables

```css
/* Use Docusaurus theme variables for automatic light/dark support */

.floatingButton {
  background-color: var(--ifm-color-primary);
  color: var(--ifm-color-primary-contrast-foreground);
}

.chatPanel {
  background-color: var(--ifm-background-color);
  border: 1px solid var(--ifm-color-emphasis-300);
}

.userMessage {
  background-color: var(--ifm-color-primary-lighter);
}

.aiMessage {
  background-color: var(--ifm-color-emphasis-100);
}
```

### Z-Index Layers

```css
--chatbot-button-z: 1000;
--chatbot-panel-z: 1001;
--chatbot-overlay-z: 999;
```

---

## Testing Checklist

### Manual Testing

- [ ] Floating button visible on homepage
- [ ] Floating button visible on all doc pages
- [ ] Button click opens chat panel
- [ ] Close button closes panel
- [ ] Click outside closes panel
- [ ] Escape key closes panel
- [ ] Can type message in input
- [ ] Enter key sends message
- [ ] Send button sends message
- [ ] User message appears immediately
- [ ] Loading indicator shows during request
- [ ] AI response appears after request
- [ ] Error message appears on failure
- [ ] Retry button works on error
- [ ] Conversation persists during navigation
- [ ] Light/dark theme both work
- [ ] Panel doesn't block book content

### Browser Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

---

## Deployment

### Frontend (Vercel)

```bash
cd physical-ai-textbook
npm run build
# Deploy via Vercel CLI or GitHub integration
```

**Vercel Environment Variables**:
```
REACT_APP_CHAT_API_URL=https://your-api-domain.com
```

### Backend (Railway/Render)

```bash
cd agent
# Deploy api.py as main entry point
# Set all environment variables in hosting dashboard
```

**Required Environment Variables**:
- `QDRANT_API_KEY`
- `QDRANT_URL`
- `COHERE_API_KEY`
- `GROQ_API_KEY`

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Button not visible | Root not swizzled | Run swizzle command |
| CORS error | Backend not configured | Add CORS middleware |
| No response | Backend down | Check backend logs |
| Timeout | Slow AI response | Increase timeout, check Groq API |
| Style issues | Theme vars not used | Use `--ifm-*` variables |
