# Feature Specification: Floating AI Chatbot for Docusaurus Book

**Feature Branch**: `004-floating-chatbot`
**Created**: 2025-12-16
**Status**: Draft
**Input**: User description: "Floating AI Chatbot for Docusaurus Book (FastAPI-powered)"

---

## Clarifications

### Session 2025-12-16

- Q: What is the expected backend API contract format? → A: Simple JSON - `POST /chat` with `{"query": "..."}` returns `{"response": "..."}`
- Q: What is the request timeout threshold before showing an error? → A: 30 seconds

---

## Problem Statement

The project consists of:
- A **book website built with Docusaurus** containing educational content about Physical AI and Robotics
- An **AI agent** whose logic, context (RAG), and reasoning are already implemented
- A **FastAPI backend** exposing the agent via HTTP

Currently, the AI agent is not accessible directly from the book UI in a seamless manner. A page-based chatbot experience disrupts reading flow and reduces usability. Users need a way to **ask questions at any time while reading**, without navigating away from the current page.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions While Reading (Priority: P1)

A reader is studying a chapter about robot kinematics and encounters an unfamiliar concept. Without leaving the page, they click a floating button, type their question, and receive an explanation from the AI agent. They close the chat panel and continue reading with their new understanding.

**Why this priority**: This is the core value proposition - seamless access to AI assistance while reading. Without this, the feature has no purpose.

**Independent Test**: Can be fully tested by clicking the floating button, sending a question, and verifying a response appears. Delivers immediate value as the primary interaction.

**Acceptance Scenarios**:

1. **Given** a reader is on any page of the Docusaurus book, **When** they click the floating chatbot button, **Then** a chat panel opens without page navigation or reload
2. **Given** the chat panel is open, **When** the user types a question and submits it, **Then** the question is sent to the AI agent and a response is displayed
3. **Given** the chat panel displays a response, **When** the user clicks close or outside the panel, **Then** the panel closes and the user can continue reading

---

### User Story 2 - Continue Conversation (Priority: P2)

A reader asks a follow-up question related to their previous inquiry. The chat panel maintains the conversation history within the current browsing session, allowing the user to have a coherent multi-turn dialogue.

**Why this priority**: Multi-turn conversation enhances the learning experience but requires the basic chat functionality (P1) to work first.

**Independent Test**: Can be tested by sending multiple messages in sequence and verifying previous messages remain visible in the chat panel.

**Acceptance Scenarios**:

1. **Given** a user has sent a message and received a response, **When** they send another message, **Then** both the previous exchange and new exchange are visible in the chat panel
2. **Given** a user closes and reopens the chat panel during the same browsing session, **When** the panel reopens, **Then** the previous conversation history is preserved

---

### User Story 3 - Access Chatbot from Any Page (Priority: P3)

A reader navigates from Chapter 1 to Chapter 5 using the sidebar. The floating chatbot button remains visible and accessible throughout their navigation. Clicking it opens the chat panel without disrupting their current location.

**Why this priority**: Global availability ensures consistent UX but depends on the basic chat interaction (P1) working correctly.

**Independent Test**: Can be tested by navigating to multiple different pages and verifying the floating button is visible and functional on each.

**Acceptance Scenarios**:

1. **Given** a user is on the homepage, **When** they navigate to any documentation page via sidebar, **Then** the floating chatbot button remains visible in the same position
2. **Given** a user has an open chat panel on Page A, **When** they navigate to Page B, **Then** the chat panel state is preserved (open/closed) and conversation history is maintained

---

### Edge Cases

- What happens when the AI backend is unreachable or returns an error?
  - The chat panel displays a user-friendly error message and allows retry
- What happens when the user submits an empty message?
  - The submit action is disabled or ignored; no request is sent
- What happens when a response takes longer than expected?
  - A loading indicator is displayed; the UI remains responsive
  - After 30 seconds without response, a timeout error is shown with retry option
- What happens when the user rapidly sends multiple messages?
  - Messages are queued and processed in order; UI prevents double-submission

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chatbot MUST display a floating button visible on all pages of the Docusaurus site
- **FR-002**: The floating button MUST remain fixed in position (bottom-right corner) during page scrolling
- **FR-003**: The floating button MUST toggle the chat panel open and closed when clicked
- **FR-004**: The chat panel MUST render as an overlay without causing page navigation or reload
- **FR-005**: The chat panel MUST display user messages and AI responses as distinct, visually differentiated elements
- **FR-006**: The chat panel MUST provide a text input field and submission mechanism for user messages
- **FR-007**: User messages MUST be sent to the FastAPI backend via `POST /chat` with JSON body `{"query": "<user_message>"}`
- **FR-008**: AI agent responses MUST be parsed from the JSON response `{"response": "<ai_response>"}` and displayed in the chat panel
- **FR-009**: The chat panel MUST maintain conversation history during the current browsing session
- **FR-010**: The chatbot MUST NOT interfere with Docusaurus routing, sidebar, or content rendering
- **FR-011**: The chatbot MUST display a loading indicator while awaiting AI agent responses
- **FR-012**: The chatbot MUST display user-friendly error messages when the backend is unreachable or returns errors
- **FR-013**: The chat panel MUST be closable via a close button and optionally by clicking outside the panel

### Non-Functional Requirements

- **NFR-001**: Opening and closing the chat panel MUST be instantaneous (no perceptible delay)
- **NFR-002**: Backend communication MUST NOT block or freeze the UI; requests MUST timeout after 30 seconds
- **NFR-003**: The chatbot MUST work across modern browsers (Chrome, Firefox, Safari, Edge)
- **NFR-004**: The UI MUST be usable in both light and dark themes supported by Docusaurus
- **NFR-005**: Chatbot logic MUST be encapsulated in a dedicated, maintainable component
- **NFR-006**: Backend communication logic MUST be centralized and reusable

### Key Entities

- **Chat Message**: Represents a single message in the conversation; includes sender type (user or AI), message content, and timestamp
- **Chat Session**: Represents the current conversation state; contains an ordered list of messages and session metadata
- **Backend Endpoint**: Represents the FastAPI endpoint URL for sending queries and receiving responses

---

## Constraints & Assumptions

### Technical Constraints

- The existing Docusaurus project MUST NOT be recreated; integration into existing structure required
- The AI agent runs behind a FastAPI HTTP interface; communication follows request-response model
- No long-running CLI processes are allowed in production
- Deployment must be compatible with Vercel (frontend) and an external backend (agent)
- The frontend MUST NOT expose or reimplement RAG/context logic; all context handling remains server-side

### Assumptions

- The FastAPI backend is publicly reachable via a stable URL (configured via environment variable)
- CORS is properly configured on the FastAPI service to allow requests from the Docusaurus domain
- The AI agent is stateless or manages its own session context internally
- The chatbot UI does not require user authentication

---

## Scope Boundaries

### In Scope

- Creating a floating chatbot button visible across the Docusaurus site
- Displaying a collapsible chatbot UI panel on button interaction
- Sending user messages to the FastAPI backend
- Rendering AI agent responses in request-response model
- Maintaining UI state (conversation history) during the current browsing session

### Out of Scope

- Rebuilding or modifying AI agent logic
- Re-embedding book content or changing Qdrant data (already done)
- Streaming tokens or typing animations
- Analytics or logging dashboards
- User authentication for the chatbot
- Persistent conversation history across browser sessions

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access the chatbot from any page within 1 click (floating button always visible)
- **SC-002**: Users can send a question and receive a response without page navigation or reload
- **SC-003**: 95% of user interactions with the chat panel complete without UI freezing or blocking
- **SC-004**: The book content remains fully readable (no obstruction) while the chatbot panel is open
- **SC-005**: The chatbot panel opens and closes in under 100 milliseconds (perceived as instantaneous)
- **SC-006**: Users can complete a 5-message conversation within a single browsing session with history preserved
- **SC-007**: Error states (backend unreachable) display user-friendly messages within 5 seconds of detection

### Acceptance Criteria Checklist

- [ ] A floating chatbot button is visible on all Docusaurus pages
- [ ] Clicking the button opens a chatbot panel without navigation
- [ ] Users can send questions from any page
- [ ] Responses are generated by the existing AI agent via FastAPI
- [ ] The book content remains fully readable while the chatbot is open
- [ ] No new Docusaurus project or page-based chatbot is created
- [ ] Light and dark theme compatibility verified
- [ ] Error handling displays user-friendly messages
