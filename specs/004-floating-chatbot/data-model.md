# Data Model: Floating AI Chatbot

**Feature**: 004-floating-chatbot
**Date**: 2025-12-16

---

## Overview

This feature requires minimal data modeling as it operates with session-scoped state only. No persistent storage is required.

---

## Frontend Entities

### ChatMessage

Represents a single message in the conversation.

```typescript
interface ChatMessage {
  id: string;           // Unique identifier (UUID)
  content: string;      // Message text content
  sender: 'user' | 'ai'; // Who sent the message
  timestamp: Date;      // When the message was created
}
```

**Validation Rules**:
- `id`: Auto-generated UUID v4
- `content`: Non-empty string, max 10,000 characters
- `sender`: Must be 'user' or 'ai'
- `timestamp`: Auto-generated on creation

---

### ChatState

Represents the complete chat panel state.

```typescript
interface ChatState {
  isOpen: boolean;           // Whether chat panel is visible
  messages: ChatMessage[];   // Ordered list of messages (oldest first)
  inputValue: string;        // Current input field value
  isLoading: boolean;        // Whether waiting for AI response
  error: string | null;      // Current error message, if any
}
```

**Initial State**:
```typescript
const initialChatState: ChatState = {
  isOpen: false,
  messages: [],
  inputValue: '',
  isLoading: false,
  error: null,
};
```

**State Transitions**:

| Current State | Action | New State |
|---------------|--------|-----------|
| `isOpen: false` | Click floating button | `isOpen: true` |
| `isOpen: true` | Click close/outside | `isOpen: false` |
| `isLoading: false` | Submit message | `isLoading: true`, add user message |
| `isLoading: true` | Receive response | `isLoading: false`, add AI message |
| `isLoading: true` | Timeout/error | `isLoading: false`, `error: <message>` |
| `error: <msg>` | Click retry | `error: null`, retry last message |
| `error: <msg>` | Dismiss error | `error: null` |

---

## Backend Entities

### ChatRequest

Request payload sent to FastAPI endpoint.

```typescript
interface ChatRequest {
  query: string;  // User's question
}
```

**Validation Rules**:
- `query`: Non-empty string, max 10,000 characters
- Required field

---

### ChatResponse

Response payload from FastAPI endpoint.

```typescript
interface ChatResponse {
  response: string;  // AI agent's answer
}
```

**Validation Rules**:
- `response`: String (may be empty if error occurred)

---

### ErrorResponse

Error payload from FastAPI endpoint.

```typescript
interface ErrorResponse {
  detail: string;  // Error description
}
```

---

## Entity Relationships

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ChatState                                              │
│   ├── isOpen: boolean                                    │
│   ├── messages: ChatMessage[]                            │
│   │   └── ChatMessage                                    │
│   │       ├── id: string                                 │
│   │       ├── content: string                            │
│   │       ├── sender: 'user' | 'ai'                      │
│   │       └── timestamp: Date                            │
│   ├── inputValue: string                                 │
│   ├── isLoading: boolean                                 │
│   └── error: string | null                               │
│                                                          │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ HTTP POST /chat
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ChatRequest ──────────► Agent ──────────► ChatResponse │
│   └── query: string       │                └── response  │
│                           │                              │
│                           ▼                              │
│                    Qdrant (existing)                     │
│                    └── Vector chunks                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Send Message Flow

```
1. User types message in input field
   └── ChatState.inputValue updated

2. User clicks send or presses Enter
   ├── Validate: inputValue not empty
   ├── Create ChatMessage { sender: 'user', content: inputValue }
   ├── Append to ChatState.messages
   ├── Set ChatState.isLoading = true
   ├── Clear ChatState.inputValue
   └── Send HTTP POST /chat with ChatRequest { query: content }

3. Backend processes request
   ├── Retrieve relevant chunks from Qdrant
   ├── Generate response using Groq/Llama
   └── Return ChatResponse { response: answer }

4. Frontend receives response
   ├── Create ChatMessage { sender: 'ai', content: response }
   ├── Append to ChatState.messages
   └── Set ChatState.isLoading = false

5. Error handling (if applicable)
   ├── Set ChatState.isLoading = false
   └── Set ChatState.error = errorMessage
```

---

## Storage Scope

| Entity | Storage | Lifetime | Persistence |
|--------|---------|----------|-------------|
| ChatState | React state (memory) | Browser session | None (clears on refresh) |
| ChatMessage | Within ChatState | Browser session | None |
| ChatRequest | HTTP request body | Request duration | None |
| ChatResponse | HTTP response body | Response duration | None |

---

## Constraints

1. **No Cross-Session Persistence**: Conversation history is lost on page refresh (per spec)
2. **No User Identity**: Messages are not attributed to authenticated users
3. **Message Ordering**: Messages maintain insertion order (oldest first)
4. **Single Conversation**: One active conversation at a time
5. **No Message Editing**: Messages cannot be modified after creation
6. **No Message Deletion**: Individual messages cannot be deleted (only full clear)
