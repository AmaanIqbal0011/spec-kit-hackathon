# Tasks: AI-Native Robotics Textbook

**Input**: Design documents from `/specs/001-physical-ai-robotics-textbook/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md
**Branch**: `001-physical-ai-robotics-textbook`
**Platform**: Docusaurus 3.x | **Deployment**: Vercel

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Paths relative to Docusaurus project root

## Path Conventions

```text
physical-ai-textbook/          # Docusaurus project root
├── docs/                      # Module content
├── src/components/            # React components
├── src/css/                   # Custom styles
├── src/pages/                 # Homepage
├── static/img/                # Images
├── docusaurus.config.js       # Site config
├── sidebars.js                # Navigation
```

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Docusaurus project with basic structure
**Output**: Empty but working book website ready for content

- [X] T001 Install Docusaurus using official docs via Context7 MCP
- [X] T002 Initialize Docusaurus project: `npx create-docusaurus@latest physical-ai-textbook` in the project root
- [X] T003 Run local dev server with `npm run start` and verify homepage loads at localhost:3000
- [X] T004 Add Book Title & Description on Homepage in `src/pages/index.js` or `src/components/HomepageFeatures/index.js`
- [X] T005 [P] Configure site title and description in docusaurus.config.js
- [X] T006 [P] Enable light/dark mode toggle in docusaurus.config.js themeConfig
- [X] T007 Create responsive homepage layout in src/pages/index.js with book overview and module cards
- [X] T008 [P] Add custom CSS variables and base styles in src/css/custom.css

**Checkpoint**: Local dev server running, homepage visible with dark/light toggle

---

## Phase 2 — Lesson-wise Book Structure

**Purpose**: Create docs folder structure and navigation - MUST complete before content writing
**Output**: Full module structure visible in sidebar

### Lessons Folder:
1. Lesson 01 — Introduction to Physical AI
2. Lesson 02 — ROS 2 Fundamentals
3. Lesson 03 — Gazebo & Unity Simulation
4. Lesson 04 — NVIDIA Isaac Platform
5. Lesson 05 — Vision-Language-Action (VLA)
6. Lesson 06 — Humanoid Capstone Project

- [X] T08 [P] Create 6 lesson files (e.g., `docs/lesson-01.md`, `docs/lesson-02.md`, etc.)
- [X] T09 Add all lessons to sidebar under "Lessons" section in `sidebars.js`
- [X] T010 [P] Inside each lesson file (`docs/lesson-01.md`, etc.) add:
    - Lesson Objective
    - Core Explanation
    - Key Terms
    - Summary

### Folder Structure

- [X] T011 Create docs/01-introduction/ folder for Module 1
- [X] T012 [P] Create docs/02-ros2/ folder for Module 2
- [X] T013 [P] Create docs/03-simulation/ folder for Module 3
- [X] T014 [P] Create docs/04-isaac/ folder for Module 4
- [X] T015 [P] Create docs/05-vla/ folder for Module 5
- [X] T016 [P] Create docs/06-capstone/ folder for Module 6

### Module Placeholders

- [X] T017 Create docs/01-introduction/index.md with module template structure (Introduction, Key Concepts, Summary, Knowledge Check)
- [X] T018 [P] Create docs/02-ros2/index.md with module template structure (Introduction, Key Concepts, Workflows, Summary, Knowledge Check)
- [X] T019 [P] Create docs/03-simulation/index.md with module template structure
- [X] T020 [P] Create docs/04-isaac/index.md with module template structure
- [X] T021 [P] Create docs/05-vla/index.md with module template structure
- [X] T022 [P] Create docs/06-capstone/index.md with module template structure

### Navigation

- [X] T020 Configure sidebars.js with 6 modules in correct order (Intro → ROS 2 → Simulation → Isaac → VLA → Capstone)
- [X] T021 [P] Add navbar links in docusaurus.config.js (Start Learning, GitHub)
- [X] T022 [P] Add footer with attribution and resource links in docusaurus.config.js

**Checkpoint**: All 6 modules visible in sidebar, navigation works between modules

---

## Phase 3: User Story 1 - Learn Physical AI Concepts (Priority: P1) MVP

**Goal**: Readers can explain core Physical AI and Embodied Intelligence concepts
**Independent Test**: Complete Introduction module, explain Physical AI vs traditional AI
**Word Target**: 800 words

### Implementation for User Story 1

- [X] T023 [US1] Write Introduction section in docs/01-introduction/index.md with learning objectives (3-5 objectives)
- [X] T024 [US1] Write Key Concepts section: Define Physical AI with clear explanation in docs/01-introduction/index.md
- [X] T025 [US1] Write Key Concepts section: Define Embodied Intelligence in docs/01-introduction/index.md
- [X] T026 [US1] Write Key Concepts section: Explain relationship to traditional AI in docs/01-introduction/index.md
- [X] T027 [US1] Add real-world examples of Physical AI (humanoid robots, autonomous vehicles) in docs/01-introduction/index.md
- [X] T028 [US1] Write Summary section with 3-5 key takeaways in docs/01-introduction/index.md
- [X] T029 [US1] Add Knowledge Check with 3-5 multiple-choice questions using collapsible details in docs/01-introduction/index.md
- [X] T030 [US1] Add APA citations for theoretical content in docs/01-introduction/index.md

**Checkpoint**: Module 1 complete (~800 words), Knowledge Check functional

---

## Phase 4: User Story 2 - Understand ROS 2 Control (Priority: P1)

**Goal**: Readers can explain how ROS 2 controls robot communication (nodes, topics, services)
**Independent Test**: Complete ROS 2 module, explain publish-subscribe architecture
**Word Target**: 1,400 words (includes 2 workflows)

### Implementation for User Story 2

- [X] T031 [US2] Write Introduction section with learning objectives in docs/02-ros2/index.md
- [X] T032 [US2] Write Key Concepts section: Explain ROS 2 architecture overview in docs/02-ros2/index.md
- [X] T033 [US2] Write Key Concepts section: Explain nodes and topics with nervous system analogy in docs/02-ros2/index.md
- [X] T034 [US2] Write Key Concepts section: Explain services and publish-subscribe pattern in docs/02-ros2/index.md
- [X] T035 [US2] Write Workflow 1: Understanding Node Communication in docs/02-ros2/index.md
- [X] T036 [US2] Write Workflow 2: Message Passing Basics in docs/02-ros2/index.md
- [X] T037 [US2] Write Summary section with key takeaways in docs/02-ros2/index.md
- [X] T038 [US2] Add Knowledge Check with 3-5 multiple-choice questions in docs/02-ros2/index.md
- [X] T039 [US2] Add official ROS 2 documentation citations in docs/02-ros2/index.md

**Checkpoint**: Module 2 complete (~1,400 words), 2 workflows present, Knowledge Check functional

---

## Phase 5: User Story 3 - Explore Simulation Environments (Priority: P2)

**Goal**: Readers can explain how Gazebo & Unity create digital twins
**Independent Test**: Complete Simulation module, explain physics simulation and sensor modeling
**Word Target**: 1,400 words (includes 2 workflows)

### Implementation for User Story 3

- [X] T040 [US3] Write Introduction section with learning objectives in docs/03-simulation/index.md
- [X] T041 [US3] Write Key Concepts section: Explain simulation purpose and benefits in docs/03-simulation/index.md
- [X] T042 [US3] Write Key Concepts section: Explain digital twin concepts in docs/03-simulation/index.md
- [X] T043 [US3] Write Key Concepts section: Explain physics engines and sensor simulation in docs/03-simulation/index.md
- [X] T044 [US3] Write Workflow 1: Gazebo Environment Basics in docs/03-simulation/index.md
- [X] T045 [US3] Write Workflow 2: Unity Robotics Integration Concepts in docs/03-simulation/index.md
- [X] T046 [US3] Write Summary section with key takeaways in docs/03-simulation/index.md
- [X] T047 [US3] Add Knowledge Check with 3-5 multiple-choice questions in docs/03-simulation/index.md
- [X] T048 [US3] Add Gazebo and Unity official documentation citations in docs/03-simulation/index.md

**Checkpoint**: Module 3 complete (~1,400 words), 2 workflows present, Knowledge Check functional

---

## Phase 6: User Story 4 - Master NVIDIA Isaac Platform (Priority: P2)

**Goal**: Readers can explain how NVIDIA Isaac enables perception, SLAM, and navigation
**Independent Test**: Complete Isaac module, explain perception pipelines and navigation stack
**Word Target**: 1,400 words (includes 2 workflows)

### Implementation for User Story 4

- [X] T049 [US4] Write Introduction section with learning objectives in docs/04-isaac/index.md
- [X] T050 [US4] Write Key Concepts section: Explain Isaac Sim and Isaac ROS overview in docs/04-isaac/index.md
- [X] T051 [US4] Write Key Concepts section: Explain perception fundamentals in docs/04-isaac/index.md
- [X] T052 [US4] Write Key Concepts section: Explain SLAM (Simultaneous Localization and Mapping) in docs/04-isaac/index.md
- [X] T053 [US4] Write Key Concepts section: Explain navigation concepts in docs/04-isaac/index.md
- [X] T054 [US4] Write Workflow 1: Isaac Sim Setup and Basics in docs/04-isaac/index.md
- [X] T055 [US4] Write Workflow 2: Navigation Stack Overview in docs/04-isaac/index.md
- [X] T056 [US4] Write Summary section with key takeaways in docs/04-isaac/index.md
- [X] T057 [US4] Add Knowledge Check with 3-5 multiple-choice questions in docs/04-isaac/index.md
- [X] T058 [US4] Add NVIDIA Isaac official documentation citations in docs/04-isaac/index.md

**Checkpoint**: Module 4 complete (~1,400 words), 2 workflows present, Knowledge Check functional

---

## Phase 7: User Story 5 - Implement VLA Systems (Priority: P3)

**Goal**: Readers can explain how LLMs convert language into robotic actions
**Independent Test**: Complete VLA module, explain vision-language-action pipeline
**Word Target**: 1,400 words (includes 2 workflows)

### Implementation for User Story 5

- [X] T059 [US5] Write Introduction section with learning objectives in docs/05-vla/index.md
- [X] T060 [US5] Write Key Concepts section: Explain VLA (Vision-Language-Action) architecture in docs/05-vla/index.md
- [X] T061 [US5] Write Key Concepts section: Explain vision and language integration in docs/05-vla/index.md
- [X] T062 [US5] Write Key Concepts section: Explain LLM to action flow in docs/05-vla/index.md
- [X] T063 [US5] Write Key Concepts section: Explain conversational robotics concepts in docs/05-vla/index.md
- [X] T064 [US5] Write Workflow 1: Vision-Language Integration Concepts in docs/05-vla/index.md
- [X] T065 [US5] Write Workflow 2: Action Generation Overview in docs/05-vla/index.md
- [X] T066 [US5] Write Summary section with key takeaways in docs/05-vla/index.md
- [X] T067 [US5] Add Knowledge Check with 3-5 multiple-choice questions in docs/05-vla/index.md
- [X] T068 [US5] Add peer-reviewed VLA research citations (APA format) in docs/05-vla/index.md

**Checkpoint**: Module 5 complete (~1,400 words), 2 workflows present, Knowledge Check functional

---

## Phase 8: User Story 6 - Complete Capstone Project (Priority: P3)

**Goal**: Readers can integrate all concepts through simulated humanoid robot capstone
**Independent Test**: Complete capstone, explain how all components work together
**Word Target**: 1,100 words
**Robot Model**: NVIDIA GR00T / Project GR00T humanoid examples

### Implementation for User Story 6

- [X] T069 [US6] Write Introduction section with capstone overview and learning objectives in docs/06-capstone/index.md
- [X] T070 [US6] Write Key Concepts section: Explain simulated humanoid concept using NVIDIA GR00T in docs/06-capstone/index.md
- [X] T071 [US6] Write System Integration section: Describe full system flow (ROS 2 → Simulation → Isaac → VLA) in docs/06-capstone/index.md
- [X] T072 [US6] Add cross-references to all previous modules (links to relevant sections) in docs/06-capstone/index.md
- [X] T073 [US6] Write Summary section with final learning synthesis in docs/06-capstone/index.md
- [X] T074 [US6] Add Knowledge Check with 3-5 integration-focused questions in docs/06-capstone/index.md
- [X] T075 [US6] Add NVIDIA GR00T and Isaac Sim citations in docs/06-capstone/index.md

**Checkpoint**: Module 6 complete (~1,100 words), integrates all previous modules, Knowledge Check functional

---

## Phase 9: Review & Polish

**Purpose**: Quality assurance, consistency, and professional finish
**Output**: Clean, readable, professional textbook

### Content Cleanup

- [X] T076 Review language clarity across all 6 modules
- [X] T077 Ensure consistent terminology throughout all modules
- [X] T078 Verify flow between modules (prerequisite references work)
- [X] T079 Validate word count is within 6,000-10,000 range

### UI Polish

- [X] T080 [P] Add reading progress bar CSS in src/css/custom.css
- [X] T081 [P] Verify headings and formatting consistency across modules
- [X] T082 Test sidebar navigation works correctly for all modules
- [X] T083 [P] Verify footer displays correctly with attribution
- [X] T084 Make navbar visible on all pages (default behavior of Docusaurus, verification task)
- [X] T085 Add footer with Book name, Author name, Hackathon mention in `src/components/Footer/index.js` or `docusaurus.config.js`

### References & Citations

- [X] T084 [P] Verify all APA citations are properly formatted
- [X] T085 [P] Verify all official documentation links are valid
- [X] T086 Add references section to each module (if not already present)

### Knowledge Check Validation

- [X] T087 Verify all Knowledge Check questions have correct answers and explanations
- [X] T088 Test collapsible details components work in all modules

**Checkpoint**: All content polished, consistent formatting, working navigation

---

## Phase 10: Deployment & Submission

**Purpose**: Deploy to Vercel and prepare for hackathon submission
**Output**: Live textbook at public Vercel URL

- [X] T089 Run production build with `npm run build` and verify no errors
- [X] T090 Test all pages load correctly in production build with `npm run serve`
- [X] T091 Verify navigation works end-to-end (all module links)

**Checkpoint**: Live textbook accessible at public Vercel URL, hackathon-ready

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Phase 1 (Setup) ─────────────────────────────┐
                                              │
Phase 2 (Structure) ──────────────────────────┤ BLOCKS ALL CONTENT
                                              │
              ┌───────────────────────────────┘
              │
              ▼
        ┌─────────────┐
        │   US1 (P1)  │ ← Module 1: Introduction
        │   MVP       │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   US2 (P1)  │ ← Module 2: ROS 2 (depends on US1 concepts)
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   US3 (P2)  │ ← Module 3: Simulation (depends on ROS 2)
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   US4 (P2)  │ ← Module 4: Isaac (depends on Simulation)
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   US5 (P3)  │ ← Module 5: VLA (depends on Isaac)
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │   US6 (P3)  │ ← Module 6: Capstone (depends on ALL)
        └──────┬──────┘
               │
Phase 9 (Polish) ─────────────────────────────┤
                                              │
Phase 10 (Deploy) ────────────────────────────┘
```

### User Story Dependencies

| Story | Module | Depends On | Can Parallelize |
|-------|--------|------------|-----------------|
| US1 | Introduction | Phase 2 | No - must be first |
| US2 | ROS 2 | US1 | No - builds on US1 |
| US3 | Simulation | US2 | No - builds on US2 |
| US4 | Isaac | US3 | No - builds on US3 |
| US5 | VLA | US4 | No - builds on US4 |
| US6 | Capstone | US1-US5 | No - integrates all |

### Parallel Opportunities Within Phases

**Phase 1 (Setup)**:
- T003, T004, T005, T007 can run in parallel

**Phase 2 (Structure)**:
- T009-T013 can run in parallel (folder creation)
- T015-T019 can run in parallel (placeholder files)
- T021-T022 can run in parallel (navbar/footer)

**Phase 9 (Polish)**:
- T080, T081, T083 can run in parallel
- T084, T085 can run in parallel

**Phase 10 (Deploy)**:
- T094, T095 can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Structure
3. Complete Phase 3: User Story 1 (Introduction module)
4. **STOP and VALIDATE**: Test Module 1 independently
5. Deploy preview to Vercel

### Sequential Content Delivery

Due to module dependencies (each builds on previous):

1. Setup + Structure → Foundation ready
2. US1 (Intro) → First module live
3. US2 (ROS 2) → Second module live
4. US3 (Simulation) → Third module live
5. US4 (Isaac) → Fourth module live
6. US5 (VLA) → Fifth module live
7. US6 (Capstone) → All modules complete
8. Polish → Professional quality
9. Deploy → Public URL live

### Task Completion Rule

This project is **COMPLETE** when:

- [ ] All 6 modules are written (T023-T075)
- [ ] Sidebar navigation works (T020)
- [ ] Content is lesson-wise and readable (T076-T078)
- [ ] Word count is 6,000-10,000 (T079)
- [ ] Knowledge Checks work in all modules (T087-T088)
- [ ] Site deploys to public Vercel URL (T092-T093)
- [ ] Matches the approved plan

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 96 |
| Setup Tasks | 7 |
| Structure Tasks | 15 |
| US1 Tasks | 8 |
| US2 Tasks | 9 |
| US3 Tasks | 9 |
| US4 Tasks | 10 |
| US5 Tasks | 10 |
| US6 Tasks | 7 |
| Polish Tasks | 13 |
| Deploy Tasks | 8 |
| Parallel Opportunities | 25 |

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Module writing is sequential due to concept dependencies
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
- Target: 7,500 words total across 6 modules
