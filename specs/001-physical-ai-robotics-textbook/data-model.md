# Data Model: AI-Native Robotics Textbook

**Feature**: 001-physical-ai-robotics-textbook
**Date**: 2025-12-14
**Type**: Static Content Site (No Database)

## Overview

This is a static content textbook with no persistent data storage. The "data model" describes the content structure and file organization that will be authored as Markdown/MDX files.

## Content Entities

### 1. Textbook

The root entity representing the entire educational resource.

**Attributes**:
| Attribute | Type | Description |
|-----------|------|-------------|
| title | string | "Physical AI & Humanoid Robotics" |
| version | string | "1.0.0" |
| createdDate | date | 2025-12-14 |
| targetWordCount | range | 6,000-10,000 |
| moduleCount | number | 6 |

**File Location**: `docusaurus.config.js` (site metadata)

---

### 2. Module

A self-contained learning chapter covering a specific topic.

**Attributes**:
| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier (e.g., "01-introduction") |
| title | string | Yes | Display name |
| order | number | Yes | Sequence position (1-6) |
| description | string | Yes | Brief summary for sidebar/overview |
| targetWords | number | Yes | Word count target |
| hasWorkflows | boolean | Yes | Whether module includes practical workflows |
| workflowCount | number | Conditional | Required if hasWorkflows=true (min 2) |
| prerequisites | string[] | No | List of prerequisite module IDs |

**Instances**:
| ID | Title | Order | Words | Workflows | Prerequisites |
|----|-------|-------|-------|-----------|---------------|
| 01-introduction | Introduction to Physical AI | 1 | 800 | No | None |
| 02-ros2 | ROS 2 Fundamentals | 2 | 1,400 | Yes (2) | 01-introduction |
| 03-simulation | Gazebo & Unity Simulation | 3 | 1,400 | Yes (2) | 02-ros2 |
| 04-isaac | NVIDIA Isaac Platform | 4 | 1,400 | Yes (2) | 03-simulation |
| 05-vla | Vision-Language-Action Systems | 5 | 1,400 | Yes (2) | 04-isaac |
| 06-capstone | Simulated Humanoid Capstone | 6 | 1,100 | No | All previous |

**File Location**: `docs/{module-id}/index.md` or `docs/{module-id}.md`

---

### 3. Module Section

A structural component within each module.

**Attributes**:
| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| type | enum | Yes | Section type (see below) |
| content | markdown | Yes | Section content |
| order | number | Yes | Position within module |

**Section Types** (per FR-005):
| Type | Order | Description | Required |
|------|-------|-------------|----------|
| introduction | 1 | Module overview and learning objectives | Yes |
| concepts | 2 | Core theoretical content | Yes |
| workflows | 3 | Practical hands-on exercises | Conditional |
| summary | 4 | Key takeaways | Yes |
| knowledge-check | 5 | Multiple-choice assessment | Yes |

**File Location**: Within module markdown file as H2 sections

---

### 4. Workflow

A practical, hands-on exercise within a technical module.

**Attributes**:
| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| title | string | Yes | Workflow name |
| moduleId | string | Yes | Parent module reference |
| prerequisites | string[] | No | Required prior knowledge |
| steps | step[] | Yes | Ordered list of steps |
| expectedOutcome | string | Yes | What reader achieves |

**Minimum Count**: 2 per technical module (FR-004)

**Technical Modules Requiring Workflows**:
- 02-ros2 (2 workflows)
- 03-simulation (2 workflows)
- 04-isaac (2 workflows)
- 05-vla (2 workflows)

**Total**: 8 workflows minimum

**File Location**: Within module markdown under `## Practical Workflows` section

---

### 5. Knowledge Check Question

A multiple-choice assessment item within a module.

**Attributes**:
| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Question identifier |
| moduleId | string | Yes | Parent module reference |
| question | string | Yes | Question text |
| options | option[] | Yes | Answer choices (4 options) |
| correctAnswer | string | Yes | Correct option letter (A-D) |
| explanation | string | Yes | Why answer is correct |

**Option Structure**:
| Attribute | Type | Description |
|-----------|------|-------------|
| letter | string | Option identifier (A, B, C, D) |
| text | string | Option content |

**Count**: 3-5 questions per module (clarification decision)

**File Location**: Within module markdown under `## Knowledge Check` section

---

### 6. Citation

A reference to external source material.

**Attributes**:
| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Citation key |
| type | enum | Yes | "research" | "documentation" | "whitepaper" |
| title | string | Yes | Source title |
| authors | string[] | Conditional | Required for research type |
| url | string | Yes | Source URL |
| accessDate | date | Yes | Date accessed |
| format | string | Yes | APA format string |

**Tier Requirements** (from constitution):
- Tier 1 (Research): 40% minimum
- Tier 2 (Documentation): 40% minimum
- Tier 3 (Whitepapers): 20% maximum

**File Location**: Inline in content + References section per module

---

## File Structure

```text
physical-ai-robotics-textbook/
├── docs/
│   ├── intro.md                    # Landing page content
│   ├── 01-introduction/
│   │   └── index.md                # Module 1: Physical AI Intro
│   ├── 02-ros2/
│   │   └── index.md                # Module 2: ROS 2 Fundamentals
│   ├── 03-simulation/
│   │   └── index.md                # Module 3: Gazebo & Unity
│   ├── 04-isaac/
│   │   └── index.md                # Module 4: NVIDIA Isaac
│   ├── 05-vla/
│   │   └── index.md                # Module 5: VLA Systems
│   └── 06-capstone/
│       └── index.md                # Module 6: Humanoid Capstone
├── src/
│   ├── components/
│   │   └── KnowledgeCheck.jsx      # Quiz component (optional)
│   ├── css/
│   │   └── custom.css              # Progress bar, custom styles
│   └── pages/
│       └── index.js                # Homepage
├── static/
│   └── img/                        # Images and diagrams
├── docusaurus.config.js            # Site configuration
├── sidebars.js                     # Navigation structure
└── package.json                    # Dependencies
```

## Relationships

```text
Textbook (1)
    │
    └── Module (6)
            │
            ├── Section (5 per module)
            │       └── introduction | concepts | workflows | summary | knowledge-check
            │
            ├── Workflow (2 per technical module, 8 total)
            │
            ├── KnowledgeCheckQuestion (3-5 per module, ~24 total)
            │
            └── Citation (inline references)
```

## Validation Rules

### Module Validation
- Each module MUST have all 5 required sections
- Technical modules (02-05) MUST have exactly 2 workflows
- All modules MUST have 3-5 knowledge check questions
- Module prerequisites MUST reference valid existing modules

### Content Validation
- Total word count MUST be 6,000-10,000
- Citations MUST follow APA format for research
- Documentation links MUST be to official sources
- All workflows MUST have expected outcomes defined

### Knowledge Check Validation
- Each question MUST have exactly 4 options (A-D)
- correctAnswer MUST be one of A, B, C, D
- explanation MUST reference relevant module content
