---
id: 005
title: Regenerate Tasks for OpenAI-Compatible Pattern
stage: tasks
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-book-rag-agent
branch: 003-book-rag-agent
user: user
command: /sp.tasks
labels: ["tasks", "openai-agents-sdk", "gemini", "openai-compatible", "runner-sync", "refactor"]
links:
  spec: specs/003-book-rag-agent/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-book-rag-agent/tasks.md
tests:
  - Manual validation pending (T065-T066, T070-T072, T077-T078, T085)
---

## Prompt

/sp.tasks

⚠️ **Critical Constraint**
> The final implementation MUST closely follow the **given code structure and style**
> (Agent SDK, `function_tool`, `Runner.run_sync`, Gemini via OpenAI-compatible endpoint).
>
> ✅ **ALL work must exist in ONE file: `agent/main.py`**
> ✅ **NO refactoring into multiple files**

---

## Phase 1: Project & Environment Setup

1. Create a folder named `agent/`
2. Initialize a UV-managed Python project inside `agent/`
3. Lock the Python version using UV
4. Create a `.env` file inside `agent/`
5. Add environment variables:
   - `GEMINI_API_KEY`
   - `COHERE_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
6. Add `.env` to `.gitignore`
7. Create a single file: `agent/main.py`
8. Ensure **no other Python files** are created

[... 12 phases with 66 detailed steps ...]

## Phase 12: Final Verification

62. Confirm **all logic exists in `agent/main.py`**
63. Confirm the code structure matches the provided reference code
64. Confirm Gemini is accessed via OpenAI-compatible endpoint
65. Confirm Cohere + Qdrant are the only data sources
66. Mark the agent as **production & hackathon ready**

## Response snapshot

Successfully regenerated tasks.md with **86 tasks** across **10 phases** following the new code structure requirements:

**Key Changes from Previous tasks.md:**
1. Changed from `LitellmModel` to `OpenAIChatCompletionsModel` + `AsyncOpenAI`
2. Changed from async `Runner.run()` to synchronous `Runner.run_sync()`
3. Changed Gemini integration from `litellm/gemini/...` to OpenAI-compatible endpoint
4. Updated environment variables: `QDRANT_URL` + `QDRANT_API_KEY` instead of host/port
5. Added explicit `set_tracing_disabled(True)` requirement

**Task Distribution:**
- Phase 1 (Setup): 8 tasks
- Phase 2 (Dependencies): 6 tasks
- Phase 3 (SDK Bootstrap): 10 tasks
- Phase 4 (Gemini Provider): 4 tasks
- Phase 5 (External Clients): 8 tasks
- Phase 6 (Embedding): 6 tasks
- Phase 7 (US1 - MVP): 24 tasks
- Phase 8 (US2 - Refusal): 6 tasks
- Phase 9 (US3 - Citations): 6 tasks
- Phase 10 (Final Verification): 8 tasks

**Reference Implementation Pattern Included:**
```python
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool

gemini_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=gemini_client
)

result = Runner.run_sync(agent, query)
```

## Outcome

- Impact: Regenerated tasks.md with correct OpenAI-compatible pattern (86 tasks)
- Tests: 8 manual validation tasks pending (require .env and Qdrant)
- Files: 1 file modified (specs/003-book-rag-agent/tasks.md)
- Next prompts: /sp.implement to execute the updated tasks
- Reflection: User requested different SDK pattern than previous implementation; tasks now align with `OpenAIChatCompletionsModel` + `Runner.run_sync` approach

## Evaluation notes (flywheel)

- Failure modes observed: None - Context7 MCP provided correct SDK patterns
- Graders run and results (PASS/FAIL): Task count validation PASS (86 tasks), format validation PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement using new tasks.md and verify Gemini OpenAI-compatible endpoint works correctly
