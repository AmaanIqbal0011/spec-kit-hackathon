<!--
Sync Impact Report:
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
-->
# AI-Native Textbook on Physical AI & Humanoid Robotics Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### Technical Accuracy
All factual and technical claims must be traceable to credible sources.
Approved Source Types:
  * Peer-reviewed robotics & AI research
  * Official documentation (ROS, NVIDIA, OpenAI, Unity, Gazebo)
  * Industry whitepapers (McKinsey, NVIDIA, Open Robotics)
Minimum Source Ratio:
  * At least 40% peer-reviewed research
  * At least 40% official technical documentation
Citation Format: APA (for theory) + Official Docs (for tooling)

### Educational Clarity
Content must be optimized for students with CS, AI, and engineering backgrounds.
Writing Quality:
  * Target Readability: Flesch-Kincaid Grade 11–13
  * Style: Precise, instructional, implementation-focused

### AI-Native Design
Content must be optimized for AI agents, RAG, and personalization.
AI Output Validation:
  * All Claude-generated content must be reviewed for hallucinations
RAG & AI Agent Standards:
  * All book content must be chunked for vector embedding, indexed in Qdrant Cloud, and stored with metadata in Neon Postgres.
  * The chatbot must answer only from indexed textbook data, support “Answer from Selected Text Only”, and reject hallucinated responses outside knowledge base.
  * Prompt design must enforce context grounding, tool-use transparency, and safety filters for robotics actions.

### Reproducibility
All technical workflows, commands, and architectures must be repeatable.
Code & Simulation Accuracy:
  * All code must be syntactically valid.
  * All ROS, Gazebo, Isaac, and VLA workflows must be technically consistent.

### Industry Relevance
Content must be aligned with real-world ROS 2, Gazebo, NVIDIA Isaac, and VLA stacks.

### Open Knowledge
Content must be structured for community learning and reuse.

## Structural Constraints
Book Format: Docusaurus (Markdown + MDX)
Deployment: GitHub Pages or Vercel
Modular Design:
  * Introduction to Physical AI
  * ROS 2 Fundamentals
  * Gazebo & Unity Simulation
  * NVIDIA Isaac Platform
  * Vision-Language-Action Systems
  * Conversational Robotics
  * Capstone Project
Each chapter must include:
  * Learning Objectives
  * Conceptual Explanation
  * Tooling Overview
  * Implementation Section
  * Summary
  * AI Chat Prompt Suggestions

## Quality & Integrity Controls

Plagiarism Tolerance: 0%
AI-Generated Content Disclosure: Required in project documentation
Fact-Checking: Mandatory for all hardware, simulation, and AI claims
Unsafe Robotics Instructions: Strictly prohibited
No fabricated benchmarks, performance metrics, or hardware claims

## Personalization & Localization Standards

User profiling via Better-Auth must include:
  * Software experience level
  * Hardware/robotics exposure
Personalized content rules:
  * Beginner → more theory + visuals
  * Advanced → more math, ROS, and GPU pipelines
Urdu translation:
  * Must preserve technical meaning
  * Must not oversimplify robotics terminology

## Security & Deployment Standards

API keys must never be stored in public repos
Environment variables enforced for all secrets
Database access must be role-restricted
All external APIs must have rate limiting

## Governance
This constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan. All PRs/reviews must verify compliance. Complexity must be justified.

**Version**: v1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
