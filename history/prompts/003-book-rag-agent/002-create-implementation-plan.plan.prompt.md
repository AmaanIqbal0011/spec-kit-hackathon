---
id: 002
title: Create Implementation Plan for Book RAG Agent
stage: plan
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-book-rag-agent
branch: 003-book-rag-agent
user: user
command: /sp.plan
labels: ["planning", "architecture", "rag", "openai-agents-sdk", "gemini", "cohere", "qdrant"]
links:
  spec: specs/003-book-rag-agent/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-book-rag-agent/plan.md
  - specs/003-book-rag-agent/research.md
  - specs/003-book-rag-agent/data-model.md
  - specs/003-book-rag-agent/quickstart.md
  - specs/003-book-rag-agent/contracts/agent-api.md
tests:
  - N/A (planning phase)
---

## Prompt

/sp.plan

## 1. Planning Objective
This plan defines **how to implement** the BookRAGAgent described in SP.Specify.
The goal is to build a **clean, isolated, reproducible RAG agent** that retrieves book content from Qdrant and answers questions using OpenAI Agent SDK with Gemini, fully managed via **UV** inside the `agent/` folder.

## 2. Project Structure Plan
- Create a root `agent/` directory
- Keep **all code, configs, and dependencies** inside this folder
- All code are in only main.py

## 3. Environment & Dependency Setup
- Initialize a new UV project inside `agent/`
- Lock all dependencies using UV
- Create environment variable support for Gemini, Cohere, Qdrant

## 4. Client Setup Plan
- Initialize Cohere client for embedding-only usage
- Initialize Qdrant client in read-only retrieval mode

## 5. Embedding Strategy Plan
- Design a single reusable embedding function using Cohere

## 6. Retrieval Tool Design Plan
- Define retrieval function as a **tool** compatible with OpenAI Agent SDK
- Accept user query, embed, search Qdrant, return context

## 7. Agent Construction Plan
- Create agent using OpenAI Agent SDK with Gemini via LiteLLM
- Register retrieval function tool
- Enforce context-only answering via instructions

## 8-12. Additional sections covering context flow, MCP integration, runtime, testing, and completion criteria.

## Response snapshot

Created comprehensive implementation plan for Book RAG Agent:

**Key Technical Decisions:**
1. **Agent Framework**: OpenAI Agents SDK with LiteLLM for Gemini provider
2. **Embeddings**: Cohere embed-english-v3.0 with `input_type="search_query"`
3. **Vector DB**: Qdrant with `query_points` method, threshold=0.75
4. **Architecture**: Single `main.py` file per user requirement

**Artifacts Generated:**
- `plan.md` - Full implementation plan with phases
- `research.md` - Technical decisions with rationale
- `data-model.md` - Entity definitions (Query, Embedding, RetrievedChunk, Context, Response)
- `quickstart.md` - Setup and usage guide
- `contracts/agent-api.md` - Function interfaces and tool signatures

**Constitution Compliance:**
- All RAG standards met (top_k=5, threshold=0.75, context_window=4000)
- Security standards met (env vars, no hardcoded secrets)
- All 6 core principles verified

**Implementation Phases:**
1. Environment Setup (UV, dependencies, .env)
2. Client Initialization (Cohere, Qdrant)
3. Embedding Layer
4. Retrieval Tool with @function_tool
5. Agent Definition with LitellmModel
6. Runtime & CLI

## Outcome

- Impact: Created complete implementation roadmap for hackathon-ready RAG agent
- Tests: N/A (planning phase)
- Files: 5 planning artifacts created
- Next prompts: `/sp.tasks` to generate detailed implementation tasks
- Reflection: User requirements were clear; single-file architecture simplifies implementation

## Evaluation notes (flywheel)

- Failure modes observed: None - all research completed successfully via Context7 MCP
- Graders run and results (PASS/FAIL): Constitution check PASS, security check PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task generation with `/sp.tasks`
