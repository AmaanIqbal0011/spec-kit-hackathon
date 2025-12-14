---
id: 002
title: Analyze Homepage Sidebar Issue
stage: misc
date: 2025-12-14
surface: agent
model: claude-sonnet-4-5
feature: 001-physical-ai-robotics-textbook
branch: 001-physical-ai-robotics-textbook
user: default
command: /sp.analyze
labels: [analysis, homepage, sidebar, docusaurus, ux]
links:
  spec: specs/001-physical-ai-robotics-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - (read-only analysis, no files modified)
tests:
  - (read-only analysis, no tests run)
---

## Prompt

Execute `/sp.analyze` with user input requiring homepage visibility rules:
- The lesson sidebar / lesson navbar MUST NOT appear on the homepage
- The homepage should feel like a landing page / overview page
- Lesson navigation should only appear after the user starts reading

## Response snapshot

Produced comprehensive Specification Analysis Report identifying:

**1 CRITICAL issue**: Current implementation uses `routeBasePath: '/'` placing docs at root, causing sidebar to appear on homepage. This violates the new user requirement.

**Key findings:**
- Homepage (`docs/intro.md`) currently has sidebar visible
- `src/pages/index.js` was removed during implementation
- Plan specified standalone homepage but implementation deviated
- 8 total findings across categories (1 critical, 1 high, 4 medium, 2 low)

**Required remediation:**
1. Create standalone `src/pages/index.js` landing page
2. Change docs `routeBasePath` to `/docs/` or `/lessons/`
3. Update all internal navigation links

**Metrics:**
- 94.7% requirement coverage
- ~10,914 words (slightly exceeds 10,000 target)
- All 6 modules complete with 8 workflows

## Outcome

- Impact: Identified 1 critical UX issue requiring pre-deployment fix
- Tests: Read-only analysis, no tests executed
- Files: 0 files modified (analysis only)
- Next prompts: Implement homepage fix, update routing configuration
- Reflection: User requirement surfaced post-implementation; analysis correctly flagged deviation from expected landing page UX

## Evaluation notes (flywheel)

- Failure modes observed: Initial implementation prioritized content over UX specification; homepage-as-doc pattern conflicted with landing page requirement
- Graders run and results (PASS/FAIL): N/A (analysis only)
- Prompt variant (if applicable): Standard /sp.analyze with user context
- Next experiment (smallest change to try): Create minimal standalone index.js, test sidebar visibility
