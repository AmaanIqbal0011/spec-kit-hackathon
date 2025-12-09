# Project: AI-Native Robotics Textbook

## Phase 1 — Setup & Environment
- [X] T001 Install Node.js (LTS)
- [X] T002 Install Docusaurus using official docs via Context7 MCP
- [X] T003 Initialize Docusaurus project: `npx create-docusaurus@latest my-book classic` in the project root
- [ ] T004 Run local dev server: `npm run start` in the project root
- [ ] T005 Verify homepage loads correctly

## Phase 2 — Navbar & Layout Setup
- [X] T006 Design a clean main navbar with Home, Lessons, Capstone, About in `docusaurus.config.js`
- [X] T007 Add Book Title & Description on Homepage in `src/pages/index.js` or `src/components/HomepageFeatures/index.js`
- [X] T008 Make navbar visible on all pages (default behavior of Docusaurus, verification task)
- [X] T009 Add footer with Book name, Author name, Hackathon mention in `src/components/Footer/index.js` or `docusaurus.config.js`

## Phase 3 — Lesson-wise Book Structure

### Lessons Folder:
1. Lesson 01 — Introduction to Physical AI
2. Lesson 02 — ROS 2 Fundamentals
3. Lesson 03 — Gazebo & Unity Simulation
4. Lesson 04 — NVIDIA Isaac Platform
5. Lesson 05 — Vision-Language-Action (VLA)
6. Lesson 06 — Humanoid Capstone Project

- [X] T010 [P] Create 6 lesson files (e.g., `docs/lesson-01.md`, `docs/lesson-02.md`, etc.)
- [X] T011 Add all lessons to sidebar under "Lessons" section in `sidebars.js`
- [X] T012 [P] Inside each lesson file (`docs/lesson-01.md`, etc.) add:
    - Lesson Objective
    - Core Explanation
    - Key Terms
    - Summary

## Phase 4 — Core Writing

### Lesson 01 — Physical AI
- [X] T013 [P] [US1] Define Physical AI in `docs/lesson-01.md`
- [X] T014 [P] [US1] Define Embodied Intelligence in `docs/lesson-01.md`
- [X] T015 [P] [US1] Add daily life examples in `docs/lesson-01.md`
- [X] T016 [P] [US1] Add lesson summary in `docs/lesson-01.md`

### Lesson 02 — ROS 2
- [X] T017 [P] [US2] Explain nodes, topics, services in `docs/lesson-02.md`
- [X] T018 [P] [US2] Explain robot "nervous system" analogy in `docs/lesson-02.md`
- [X] T019 [P] [US2] Add simple architecture explanation in `docs/lesson-02.md`
- [X] T020 [P] [US2] Add lesson summary in `docs/lesson-02.md`

### Lesson 03 — Gazebo & Unity
- [X] T021 [P] [US3] Explain simulation in `docs/lesson-03.md`
- [X] T022 [P] [US3] Explain digital twin in `docs/lesson-03.md`
- [X] T023 [P] [US3] Explain benefits of simulation in `docs/lesson-03.md`
- [X] T024 [P] [US3] Add lesson summary in `docs/lesson-03.md`

### Lesson 04 — NVIDIA Isaac
- [X] T025 [P] [US4] Explain perception in `docs/lesson-04.md`
- [X] T026 [P] [US4] Explain SLAM in `docs/lesson-04.md`
- [X] T027 [P] [US4] Explain navigation in `docs/lesson-04.md`
- [X] T028 [P] [US4] Add lesson summary in `docs/lesson-04.md`

### Lesson 05 — VLA Systems
- [X] T029 [P] [US5] Explain vision + language in `docs/lesson-05.md`
- [X] T030 [P] [US5] Explain LLM robot control in `docs/lesson-05.md`
- [X] T031 [P] [US5] Explain conversational robotics in `docs/lesson-05.md`
- [X] T032 [P] [US5] Add lesson summary in `docs/lesson-05.md`

## Phase 5 — Final Capstone Lesson

### Lesson 06 — Humanoid Capstone
- [X] T033 [P] [US6] Define simulated humanoid concept in `docs/lesson-06.md`
- [X] T034 [P] [US6] Explain full system flow: ROS 2 → Simulation → Isaac → VLA in `docs/lesson-06.md`
- [X] T035 [P] [US6] Explain learning outcome from capstone in `docs/lesson-06.md`
- [X] T036 [P] [US6] Add final takeaway summary in `docs/lesson-06.md`

## Phase 6 — Review & Cleanup
- [X] T037 Fix grammar and clarity across all `.md` files
- [X] T038 Ensure all lessons follow same format across all `.md` files
- [X] T039 Ensure proper lesson order in `sidebars.js`
- [X] T040 Add basic references section (links only) in `docs/references.md`
- [X] T041 Remove any placeholder content across all `.md` files

## Final Internal Checklist
- [X] T042 Verify Navbar works on all pages
- [X] T043 Verify all 6 lessons exist
- [X] T044 Verify sidebar opens correctly
- [X] T045 Verify every lesson has Objective, Explanation, Summary
- [X] T046 Verify Book matches `sp.spec` & `sp.specify`

---

## Dependencies:
- Phase 1 tasks must be completed before Phase 2.
- Phase 2 tasks must be completed before Phase 3.
- Phase 3 tasks must be completed before Phase 4.
- Phase 4 tasks (Lesson 01-05) can be worked on in parallel once Phase 3 is complete.
- Phase 5 tasks (Lesson 06) depend on Phase 4 completion.
- Phase 6 tasks depend on Phase 5 completion.

## Parallel Execution Examples:
- T013, T014, T015, T016 can be worked on in parallel.
- T017, T018, T019, T020 can be worked on in parallel.
- T021, T022, T023, T024 can be worked on in parallel.
- T025, T026, T027, T028 can be worked on in parallel.
- T029, T030, T031, T032 can be worked on in parallel.
- T033, T034, T035, T036 can be worked on in parallel.

## Implementation Strategy:
- Focus on an MVP approach, completing tasks phase by phase.
- Prioritize core functionality before polishing.
- Utilize the Context7 MCP for official Docusaurus documentation.
