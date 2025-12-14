# Research: AI-Native Robotics Textbook

**Feature**: 001-physical-ai-robotics-textbook
**Date**: 2025-12-14
**Status**: Complete

## Technical Decisions

### 1. Platform Selection

**Decision**: Docusaurus v3.x

**Rationale**:
- Industry-standard documentation platform with native MDX support
- Built-in sidebar navigation, search, and dark/light mode
- Optimized for content-first static sites
- Native Vercel deployment support with zero configuration
- Aligns with constitution requirement (Structural Constraints)

**Alternatives Considered**:
- GitBook: Rejected due to limited customization and paid features
- MkDocs: Rejected due to weaker MDX support
- VuePress: Rejected due to smaller ecosystem than Docusaurus

---

### 2. Module Structure

**Decision**: 5-section consistent structure per module

**Structure**:
1. Introduction
2. Key Concepts (Core Concepts)
3. Practical Workflows (2 per technical module)
4. Summary
5. Knowledge Check (3-5 multiple-choice questions)

**Rationale**:
- Aligns with spec FR-005 requirement
- Consistent structure aids navigation and learning
- Knowledge Checks provide immediate comprehension feedback
- Progressive disclosure from concepts to application

**Alternatives Considered**:
- Full chapter template from constitution: Rejected as overly complex for 6,000-10,000 word constraint
- Minimal structure: Rejected as insufficient for educational objectives

---

### 3. Content Architecture

**Decision**: 6 modules in sequential dependency order

**Modules**:
1. Introduction to Physical AI & Embodied Intelligence (foundational)
2. ROS 2 Fundamentals (prerequisite for all technical modules)
3. Gazebo & Unity Simulation (depends on ROS 2)
4. NVIDIA Isaac Platform (depends on Simulation)
5. Vision-Language-Action Systems (depends on NVIDIA Isaac)
6. Simulated Humanoid Capstone Project (integrates all modules)

**Rationale**:
- Matches spec FR-003 requirement for 6 modules
- Sequential dependencies ensure progressive learning
- Capstone requires all prior knowledge

**Alternatives Considered**:
- Parallel module structure: Rejected due to prerequisite dependencies
- 8+ modules: Rejected due to word count constraint (6,000-10,000)

---

### 4. Deployment Platform

**Decision**: Vercel with preview deployments

**Rationale**:
- Faster build times than GitHub Pages
- Preview deployments for pull request review
- Native Docusaurus integration
- Free tier sufficient for static content
- Confirmed in clarification session

**Alternatives Considered**:
- GitHub Pages: Rejected by user preference (slower builds, no preview deployments)
- Netlify: Not considered (Vercel selected in clarification)

---

### 5. Capstone Robot Model

**Decision**: NVIDIA GR00T / Project GR00T humanoid examples

**Rationale**:
- Official NVIDIA examples with Isaac Sim documentation
- Cutting-edge humanoid robotics platform
- Directly supports Isaac module content
- Well-documented workflows in official NVIDIA tutorials
- Confirmed in clarification session

**Alternatives Considered**:
- Generic URDF humanoid: Rejected due to limited documentation
- Unitree H1: Rejected due to narrower official support

---

### 6. Word Count Distribution

**Decision**: Target 7,500 words (midpoint of 6,000-10,000 range)

**Distribution**:
| Module | Target Words | Rationale |
|--------|-------------|-----------|
| Introduction | 800 | Foundational concepts, no workflows |
| ROS 2 Fundamentals | 1,400 | Core technical module with 2 workflows |
| Gazebo & Unity | 1,400 | Technical module with 2 workflows |
| NVIDIA Isaac | 1,400 | Technical module with 2 workflows |
| VLA Systems | 1,400 | Technical module with 2 workflows |
| Capstone | 1,100 | Integration project, system overview |
| **Total** | **7,500** | Within 6,000-10,000 constraint |

**Rationale**:
- Technical modules require more depth due to workflow requirements
- Introduction and Capstone are concept-focused (fewer words)
- Buffer for navigation, headers, and citations not counted

---

### 7. Knowledge Check Implementation

**Decision**: MDX-based collapsible multiple-choice questions

**Implementation**:
- 3-5 questions per module
- Immediate answer reveal on selection
- No backend required (static implementation)
- Docusaurus native `<details>` component for answer reveal

**Rationale**:
- Aligns with clarification decision (multiple-choice, 3-5 per module)
- Static implementation avoids backend complexity
- Native MDX support in Docusaurus

**Alternatives Considered**:
- Interactive quiz plugin: Rejected due to added complexity
- External quiz service: Rejected due to user experience fragmentation

---

### 8. Reading Progress Bar

**Decision**: Docusaurus plugin or custom CSS implementation

**Implementation Options**:
- Option A: `docusaurus-plugin-reading-time` + custom progress indicator
- Option B: CSS scroll-progress indicator (native)

**Rationale**:
- User requested progress bar for content pages
- Native CSS solution preferred for simplicity
- No external dependencies required

---

### 9. Light/Dark Mode

**Decision**: Docusaurus built-in theme toggle

**Rationale**:
- Native Docusaurus feature (zero configuration)
- User requested in Phase 1 requirements
- Accessible from navbar

---

### 10. Citation Strategy

**Decision**: Inline links with references section per module

**Format**:
- Theoretical content: APA-style inline citations
- Technical documentation: Direct links to official docs
- References section at module end with categorized sources

**Rationale**:
- Aligns with spec FR-008, FR-009 requirements
- Constitution citation standards (Tier 1, Tier 2 sources)
- Maintains readability while providing attribution

## Dependencies Identified

### Build Dependencies
- Node.js 18+ (Docusaurus requirement)
- npm or yarn package manager

### Docusaurus Dependencies
- `@docusaurus/core` ^3.x
- `@docusaurus/preset-classic` ^3.x
- `@docusaurus/theme-classic` ^3.x

### Optional Enhancements
- `@docusaurus/plugin-ideal-image` (image optimization)
- Custom CSS for progress bar

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Word count exceeds 10,000 | Medium | Low | Track word count per module, trim workflows |
| GR00T documentation gaps | Low | Medium | Fallback to generic Isaac humanoid examples |
| Vercel build failures | Low | Low | GitHub Pages as backup deployment |
| MDX complexity | Low | Low | Use standard Markdown where possible |

## Next Steps

1. Create data-model.md (content entities)
2. Complete plan.md (implementation plan)
3. Proceed to `/sp.tasks` for task generation
