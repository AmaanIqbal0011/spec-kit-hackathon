---
id: 0001
title: Update Project Constitution
stage: constitution
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: /sp.constitution
labels: ["constitution", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:

---

## Prompt

Project: AI-Native Textbook on Physical AI & Humanoid Robotics
Platform: Spec-Kit Plus + Claude Code + Docusaurus + RAG Chatbot

Core Principles:

* Technical Accuracy through verified robotics, AI, and simulation sources
* Educational Clarity for students with CS, AI, and engineering background
* AI-Native Design (content must be optimized for AI agents, RAG, and personalization)
* Reproducibility (all technical workflows, commands, and architectures must be repeatable)
* Industry Relevance (aligned with real-world ROS 2, Gazebo, NVIDIA Isaac, and VLA stacks)
* Open Knowledge (content structured for community learning and reuse)

Key Standards:

* All factual and technical claims must be traceable to credible sources
* Citation Format: APA (for theory) + Official Docs (for tooling)
* Approved Source Types:

  * Peer-reviewed robotics & AI research
  * Official documentation (ROS, NVIDIA, OpenAI, Unity, Gazebo)
  * Industry whitepapers (McKinsey, NVIDIA, Open Robotics)
* Minimum Source Ratio:

  * At least 40% peer-reviewed research
  * At least 40% official technical documentation
* AI Output Validation:

  * All Claude-generated content must be reviewed for hallucinations
* Writing Quality:

  * Target Readability: Flesch-Kincaid Grade 11–13
  * Style: Precise, instructional, implementation-focused
* Code & Simulation Accuracy:

  * All code must be syntactically valid
  * All ROS, Gazebo, Isaac, and VLA workflows must be technically consistent

Quality & Integrity Controls:

* Plagiarism Tolerance: 0%
* AI-Generated Content Disclosure: Required in project documentation
* Fact-Checking: Mandatory for all hardware, simulation, and AI claims
* Unsafe Robotics Instructions: Strictly prohibited
* No fabricated benchmarks, performance metrics, or hardware claims

Structural Constraints:

* Book Format: Docusaurus (Markdown + MDX)
* Deployment: GitHub Pages or Vercel
* Modular Design:

  * Introduction to Physical AI
  * ROS 2 Fundamentals
  * Gazebo & Unity Simulation
  * NVIDIA Isaac Platform
  * Vision-Language-Action Systems
  * Conversational Robotics
  * Capstone Project
* Each chapter must include:

  * Learning Objectives
  * Conceptual Explanation
  * Tooling Overview
  * Implementation Section
  * Summary
  * AI Chat Prompt Suggestions

RAG & AI Agent Standards:

* All book content must be:

  * Chunked for vector embedding
  * Indexed in Qdrant Cloud
  * Stored with metadata in Neon Postgres
* The chatbot must:

  * Answer only from indexed textbook data
  * Support “Answer from Selected Text Only”
  * Reject hallucinated responses outside knowledge base
* Prompt design must enforce:

  * Context grounding
  * Tool-use transparency
  * Safety filters for robotics actions

Personalization & Localization Standards:

* User profiling via Better-Auth must include:

  * Software experience level
  * Hardware/robotics exposure
* Personalized content rules:

  * Beginner → more theory + visuals
  * Advanced → more math, ROS, and GPU pipelines
* Urdu translation:

  * Must preserve technical meaning
  * Must not oversimplify robotics terminology

Security & Deployment Standards:

* API keys must never be stored in public repos
* Environment variables enforced for all secrets
* Database access must be role-restricted
* All external APIs must have rate limiting

Success Criteria:

* Book successfully published on GitHub Pages or Vercel
* RAG chatbot answers accurately from book content
* Selected-text Q&A works without hallucinations
* Zero plagiarism detected
* All technical workflows validated
* Meets all hackathon base requirements (100/100)
* Eligible for bonus scoring via:

  * Sub-agents
  * Personalized content
  * Urdu translation
  * Authentication system

## Response snapshot

The project constitution at `.specify/memory/constitution.md` has been updated to `v1.0.0` with the new content provided by the user. The `LAST_AMENDED_DATE` and `RATIFICATION_DATE` have been set to `2025-12-06`.

**Sync Impact Report:**
Version change:  -> v1.0.0
List of modified principles:
- [PRINCIPLE_1_NAME] -> Technical Accuracy
- [PRINCIPLE_2_NAME] -> Educational Clarity
- [PRINCIPLE_3_NAME] -> AI-Native Design
- [PRINCIPLE_4_NAME] -> Reproducibility
- [PRINCIPLE_5_NAME] -> Industry Relevance
- [PRINCIPLE_6_NAME] -> Open Knowledge
Added sections:
- Structural Constraints
- Quality & Integrity Controls
- Personalization & Localization Standards
- Security & Deployment Standards
Removed sections:
- None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/*.md: ⚠ pending
Follow-up TODOs: None

Suggested commit message: `docs: amend constitution to v1.0.0 (initial constitution)`

## Outcome

- ✅ Impact: Constitution file updated.
- 🧪 Tests: No tests performed.
- 📁 Files: .specify/memory/constitution.md modified.
- 🔁 Next prompts: Update templates according to Sync Impact Report.
- 🧠 Reflection: PHR created successfully.

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` script not found.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
