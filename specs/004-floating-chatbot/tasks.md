# Tasks: Floating AI Chatbot

**Input**: Design documents from `/specs/004-floating-chatbot/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/chat-api.yaml

**Tests**: Manual testing (browser-based) - no automated test tasks included per spec.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `physical-ai-textbook/src/` (Docusaurus)
- **Backend**: `agent/` (FastAPI)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project verification and backend API creation

- [x] T001 Verify Docusaurus book exists in physical-ai-textbook/ with docusaurus.config.js
- [x] T002 Verify existing agent works locally in agent/main.py
- [x] T003 [P] Create Chatbot component directory at physical-ai-textbook/src/components/Chatbot/
- [x] T004 [P] Add fastapi and uvicorn to agent/pyproject.toml dependencies
- [x] T005 Create FastAPI app with CORS middleware in agent/api.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Backend API and frontend injection point - MUST complete before user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Implement POST /chat endpoint in agent/api.py wrapping existing agent logic
- [x] T007 Implement GET /health endpoint in agent/api.py for health checks
- [x] T008 Add Pydantic models (ChatRequest, ChatResponse) in agent/api.py
- [ ] T009 Test /chat endpoint locally with curl: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"query":"What is ROS 2?"}'`
- [x] T010 Swizzle Docusaurus Root component: `npm run swizzle @docusaurus/theme-classic Root -- --wrap` in physical-ai-textbook/
- [x] T011 Create ChatbotProvider context in physical-ai-textbook/src/components/Chatbot/ChatbotProvider.js
- [x] T012 Create API module with sendMessage function in physical-ai-textbook/src/components/Chatbot/api.js

**Checkpoint**: Backend API functional, frontend injection point ready - user story implementation can begin

---

## Phase 3: User Story 1 - Ask Questions While Reading (Priority: P1) 🎯 MVP

**Goal**: Reader clicks floating button, types question, receives AI response, closes panel

**Independent Test**: Click floating button → panel opens → type question → submit → AI response appears → close panel

### Implementation for User Story 1

- [x] T013 [P] [US1] Create FloatingButton component in physical-ai-textbook/src/components/Chatbot/FloatingButton.js
- [x] T014 [P] [US1] Create ChatPanel component shell in physical-ai-textbook/src/components/Chatbot/ChatPanel.js
- [x] T015 [P] [US1] Create ChatMessage component in physical-ai-textbook/src/components/Chatbot/ChatMessage.js
- [x] T016 [P] [US1] Create styles.module.css with floating button and panel styles in physical-ai-textbook/src/components/Chatbot/styles.module.css
- [x] T017 [US1] Create main index.js export combining all components in physical-ai-textbook/src/components/Chatbot/index.js
- [x] T018 [US1] Integrate Chatbot into Root.js wrapper in physical-ai-textbook/src/theme/Root.js
- [x] T019 [US1] Implement panel open/close toggle state in ChatbotProvider.js
- [x] T020 [US1] Implement message input field and send button in ChatPanel.js
- [x] T021 [US1] Connect send button to API module and display response in ChatbotProvider.js
- [x] T022 [US1] Add loading indicator during API request in ChatPanel.js
- [x] T023 [US1] Add error message display with retry button in ChatPanel.js
- [x] T024 [US1] Implement 30-second timeout in api.js with AbortController
- [x] T025 [US1] Add empty message validation (disable send when input empty) in ChatPanel.js

**Checkpoint**: User Story 1 complete - basic chat functionality works on any page

---

## Phase 4: User Story 2 - Continue Conversation (Priority: P2)

**Goal**: Reader sends follow-up questions, conversation history preserved in session

**Independent Test**: Send message → receive response → send another message → both exchanges visible → close/reopen panel → history preserved

### Implementation for User Story 2

- [x] T026 [US2] Implement messages array state management in ChatbotProvider.js
- [x] T027 [US2] Render message list with scroll area in ChatPanel.js
- [x] T028 [US2] Auto-scroll to bottom on new message in ChatPanel.js
- [x] T029 [US2] Preserve messages state when panel closes/reopens in ChatbotProvider.js
- [x] T030 [US2] Style user messages (right-aligned, primary color) in styles.module.css
- [x] T031 [US2] Style AI messages (left-aligned, muted background) in styles.module.css
- [x] T032 [US2] Add timestamp display below each message in ChatMessage.js

**Checkpoint**: User Story 2 complete - multi-turn conversation with history works

---

## Phase 5: User Story 3 - Access Chatbot from Any Page (Priority: P3)

**Goal**: Floating button visible and functional on all pages, state persists across navigation

**Independent Test**: Navigate homepage → doc page → another doc page → button visible everywhere → open panel → navigate → panel state preserved

### Implementation for User Story 3

- [x] T033 [US3] Verify FloatingButton renders on homepage in physical-ai-textbook/
- [x] T034 [US3] Verify FloatingButton renders on all documentation pages
- [x] T035 [US3] Test state persistence during client-side navigation
- [x] T036 [US3] Ensure chatbot does not interfere with Docusaurus sidebar
- [x] T037 [US3] Ensure chatbot does not interfere with Docusaurus navbar
- [x] T038 [US3] Test panel z-index layering over page content

**Checkpoint**: User Story 3 complete - global availability with state persistence works

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Theme compatibility, accessibility, mobile responsiveness, deployment

- [x] T039 [P] Add light theme styles using CSS variables (--ifm-*) in styles.module.css
- [x] T040 [P] Add dark theme styles using CSS variables (--ifm-*) in styles.module.css
- [x] T041 [P] Add keyboard support: Escape key closes panel in ChatPanel.js
- [x] T042 [P] Add aria-label to FloatingButton for accessibility in FloatingButton.js
- [x] T043 [P] Add role="dialog" and aria-modal to ChatPanel for accessibility in ChatPanel.js
- [x] T044 [P] Add mobile responsive styles (width, height adjustments) in styles.module.css
- [x] T045 [P] Add click-outside-to-close functionality in ChatPanel.js
- [x] T046 [P] Add panel open/close CSS animation (slide-up) in styles.module.css
- [ ] T047 Deploy backend to hosting platform (Railway/Render)
- [ ] T048 Update API URL in physical-ai-textbook/.env to point to deployed backend
- [ ] T049 Deploy frontend via Vercel (automatic from GitHub)
- [ ] T050 End-to-end production test: full chat flow on live site
- [ ] T051 Cross-browser testing: Chrome, Firefox, Safari, Edge
- [ ] T052 Mobile device testing: responsive layout verification

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Core MVP functionality
- **User Story 2 (P2)**: Can start after US1 - Enhances US1 with conversation history
- **User Story 3 (P3)**: Can start after Foundational - Tests global availability

### Within Each User Story

- Components (FloatingButton, ChatPanel, ChatMessage) can be built in parallel [P]
- Integration tasks must follow component creation
- State management connects components to behavior

### Parallel Opportunities

**Phase 1 Setup**:
```
T003 Create Chatbot directory    ──┐
T004 Add FastAPI dependencies    ──┴── can run in parallel
```

**Phase 3 US1 Components**:
```
T013 FloatingButton.js   ──┐
T014 ChatPanel.js        ──┤
T015 ChatMessage.js      ──┼── can run in parallel (different files)
T016 styles.module.css   ──┘
```

**Phase 6 Polish**:
```
T039-T046 ── all can run in parallel (different concerns, different files)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012)
3. Complete Phase 3: User Story 1 (T013-T025)
4. **STOP and VALIDATE**: Test basic chat functionality
5. Deploy if ready for demo

### Incremental Delivery

1. Setup + Foundational → Backend API + Frontend injection ready
2. Add User Story 1 → Basic chat works → **Demo-ready MVP**
3. Add User Story 2 → Conversation history → Enhanced experience
4. Add User Story 3 → Global verification → Full coverage
5. Add Polish → Theme/accessibility/mobile → Production-ready

### Estimated Task Distribution

| Phase | Task Count | Parallel Tasks | Critical Path |
|-------|------------|----------------|---------------|
| Setup | 5 | 2 | T001 → T005 |
| Foundational | 7 | 0 | T006 → T012 |
| User Story 1 | 13 | 4 | T013-T016 → T017-T025 |
| User Story 2 | 7 | 0 | T026 → T032 |
| User Story 3 | 6 | 0 | T033 → T038 |
| Polish | 14 | 8 | T039-T046 → T047-T052 |
| **Total** | **52** | **14** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently testable after completion
- Manual browser testing per spec (no automated tests)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Backend must be running for frontend integration testing
