# Research Notes: Floating AI Chatbot

**Feature**: 004-floating-chatbot
**Date**: 2025-12-16

---

## 1. Docusaurus Component Integration

### Decision: Use Docusaurus Swizzling with Root Component

**Rationale**:
- Docusaurus 3.x supports "swizzling" to override core components
- The `Root` component wraps the entire application, making it ideal for global UI elements
- This approach doesn't require modifying the core Docusaurus structure

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Custom theme plugin | Overkill for a single floating component |
| Direct index.js modification | Would be overwritten on updates |
| Layout swizzle | Only wraps page content, not global |

**Implementation Path**:
```bash
npm run swizzle @docusaurus/theme-classic Root -- --wrap
```
This creates `src/theme/Root.js` which wraps the entire app.

---

## 2. State Management Approach

### Decision: React useState with Context for Cross-Navigation Persistence

**Rationale**:
- Docusaurus uses client-side routing (React Router)
- State in a Root-level component persists across page navigations
- No need for external state libraries (Redux, Zustand) for this simple use case
- Session-scoped state (clears on browser refresh) matches requirements

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| localStorage | Spec explicitly states session-only persistence |
| Redux/Zustand | Overkill for single component state |
| URL parameters | Would clutter URLs and affect bookmarking |

**State Shape**:
```typescript
interface ChatState {
  isOpen: boolean;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}
```

---

## 3. Backend API Integration

### Decision: Create FastAPI HTTP Endpoint Wrapping Existing Agent

**Rationale**:
- Existing agent (`agent/main.py`) is CLI-based with Agents SDK
- Need HTTP interface for browser fetch calls
- FastAPI already in project dependencies (backend/)
- Simple wrapper endpoint preserves agent logic

**API Contract** (from clarification):
```
POST /chat
Request:  {"query": "user question"}
Response: {"response": "AI answer"}
```

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| WebSocket streaming | Out of scope (no streaming requirement) |
| GraphQL | Overkill for single endpoint |
| Direct Groq API call from frontend | Exposes API keys, violates security |

**CORS Configuration Required**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://physical-ai-textbook.vercel.app", "http://localhost:3000"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```

---

## 4. Styling Approach

### Decision: CSS Modules with Docusaurus Theme Variables

**Rationale**:
- Docusaurus uses CSS Modules by convention
- Theme variables (`--ifm-*`) automatically adapt to light/dark mode
- No additional CSS framework needed (Tailwind would add complexity)

**Theme Variables to Use**:
```css
--ifm-color-primary          /* Button background */
--ifm-background-color       /* Panel background */
--ifm-font-color-base        /* Text color */
--ifm-color-emphasis-300     /* Borders */
```

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Tailwind CSS | Adds build complexity, not in current setup |
| Styled-components | Additional dependency, different paradigm |
| Inline styles | Harder to maintain, no theme support |

---

## 5. Error Handling Strategy

### Decision: Graceful Degradation with User-Friendly Messages

**Rationale**:
- Users shouldn't see technical errors
- Retry mechanism improves UX
- 30-second timeout prevents indefinite waiting

**Error States**:
| Error Type | User Message | Action |
|------------|--------------|--------|
| Network error | "Unable to connect. Please check your connection." | Retry button |
| Timeout (30s) | "Response is taking too long. Please try again." | Retry button |
| Server error (5xx) | "The AI service is temporarily unavailable." | Retry button |
| Empty response | "No response received. Please try rephrasing." | Clear input |

---

## 6. Accessibility Considerations

### Decision: ARIA Labels and Keyboard Navigation

**Rationale**:
- Floating elements can be problematic for screen readers
- Focus management important for overlay panels
- Keyboard users need escape key to close

**Implementation**:
- `aria-label` on floating button: "Open AI Chat Assistant"
- `role="dialog"` on chat panel
- `aria-modal="true"` when panel is open
- Focus trap within panel when open
- Escape key closes panel

---

## 7. Performance Considerations

### Decision: Lazy Load Chat Panel Content

**Rationale**:
- Button should load immediately with page
- Panel content can load on first open
- Minimizes initial bundle impact

**Bundle Strategy**:
- Floating button: ~2KB (included in main bundle)
- Chat panel: ~8KB (lazy loaded on first open)
- Total impact: Minimal (<10KB gzipped)

---

## 8. Existing Agent Integration Analysis

### Current Agent Architecture (agent/main.py)

**Key Components**:
1. `create_agent()` - Creates Agents SDK agent with Groq backend
2. `retrieve_context()` - Queries Qdrant for relevant chunks
3. `Runner.run()` - Executes agent with context

**Required Modifications**:
- Extract agent logic into reusable function
- Add HTTP endpoint wrapper
- Handle async properly for HTTP context

**Integration Approach**:
```python
# New file: agent/api.py
from fastapi import FastAPI
from agent.main import create_agent, retrieve_context

app = FastAPI()

@app.post("/chat")
async def chat(request: ChatRequest):
    context = await retrieve_context(request.query)
    response = await run_agent(request.query, context)
    return {"response": response}
```

---

## Summary of Key Decisions

| Area | Decision | Impact |
|------|----------|--------|
| Component Injection | Docusaurus Root swizzle | Global availability |
| State Management | React useState in Root | Session persistence |
| Backend | FastAPI wrapper endpoint | Reuses existing agent |
| Styling | CSS Modules + theme vars | Theme compatibility |
| Error Handling | User-friendly messages + retry | Better UX |
| Accessibility | ARIA + keyboard support | Inclusive design |
| Performance | Lazy load panel | Minimal bundle impact |
