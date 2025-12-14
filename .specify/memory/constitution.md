<!--
==========================================================================
SYNC IMPACT REPORT
==========================================================================
Version change: 0.0.0 → 1.0.0 (MAJOR: Initial constitution adoption)

Principles added:
  - I. Technical Accuracy
  - II. Educational Clarity
  - III. AI-Native Design
  - IV. Reproducibility
  - V. Industry Relevance
  - VI. Open Knowledge

Sections added:
  - Citation & Source Standards
  - Structural Constraints
  - RAG & AI Agent Standards
  - Personalization & Localization Standards
  - Quality & Integrity Controls
  - Security & Deployment Standards
  - Success Criteria
  - Governance

Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ No changes needed (Constitution Check section generic)
  - .specify/templates/spec-template.md: ✅ No changes needed (Requirements section aligns)
  - .specify/templates/tasks-template.md: ✅ No changes needed (Structure compatible)
  - .specify/templates/phr-template.prompt.md: ✅ No changes needed (PHR format standard)

Deferred items: None

Follow-up TODOs: None
==========================================================================
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Project Mission

Create an AI-native, interactive textbook for teaching Physical AI & Humanoid Robotics that bridges the gap between digital intelligence and physical embodiment through technically accurate, educationally clear, and reproducible content with embedded RAG chatbot and personalized learning experiences.

## Core Principles

### I. Technical Accuracy

All technical claims, robotics workflows, AI architectures, and simulation procedures MUST be traceable to credible, verified sources.

**Requirements:**
- All factual and technical claims MUST cite credible sources
- Zero tolerance for hallucinations or fabricated information
- All code MUST be syntactically valid and tested
- All ROS 2, Gazebo, NVIDIA Isaac, and VLA workflows MUST be technically consistent
- Hardware specifications MUST match official vendor documentation

**Validation:**
- Mandatory fact-checking for all hardware, simulation, and AI claims
- Code validation through syntax checking and execution testing
- Cross-reference against official documentation

### II. Educational Clarity

Content MUST be accessible, pedagogically sound, and structured for progressive learning for students with CS, AI, and engineering backgrounds.

**Requirements:**
- Target Readability: Flesch-Kincaid Grade 11-13
- Style: Precise, instructional, implementation-focused
- Progressive complexity from foundational to advanced concepts
- Clear learning objectives for every chapter
- Practical examples that reinforce theoretical concepts

**Writing Standards - Each chapter MUST include:**
- Learning Objectives (3-5 specific outcomes)
- Conceptual Explanation (theory and context)
- Tooling Overview (relevant software/hardware)
- Implementation Section (hands-on code/simulation)
- Summary (key takeaways)
- AI Chat Prompt Suggestions (for RAG interaction)

### III. AI-Native Design

Content MUST be optimized for AI agents, RAG systems, and automated personalization while remaining human-readable.

**Requirements:**
- Content structured for vector embedding and semantic search
- Metadata-rich chapters for contextual retrieval
- Clear section boundaries for chunking
- Consistent terminology for semantic consistency
- Examples formatted for code extraction
- Prompt-friendly explanations

**AI Optimization Standards:**
- Chunk size: 500-1000 tokens per semantic unit
- Overlap: 100 tokens between chunks
- Metadata per chunk: {module, week, topic, difficulty, keywords}
- Embedding model: text-embedding-3-small (OpenAI)
- Vector dimension: 1536

### IV. Reproducibility

All technical workflows, commands, architectures, and experiments MUST be repeatable by readers with documented prerequisites.

**Requirements:**
- Complete environment setup instructions
- Explicit prerequisite software/hardware requirements
- Version-pinned dependencies
- Step-by-step command sequences
- Expected outputs documented
- Troubleshooting sections for common errors

**Reproducibility Checklist:**
- Environment variables documented
- Installation commands tested on clean system
- Sample outputs provided
- Error scenarios addressed
- Hardware alternatives suggested

### V. Industry Relevance

Content MUST align with real-world ROS 2, Gazebo, NVIDIA Isaac, and VLA stacks as used in professional robotics development.

**Requirements:**
- Use industry-standard tools and frameworks
- Follow official best practices
- Reference current stable versions (not deprecated)
- Include industry use cases and applications
- Align with professional robotics workflows

**Industry Standards:**
- ROS 2: Humble Hawksbill (LTS) or Iron Irwini
- Gazebo: Gazebo Classic 11 or Gazebo Fortress
- NVIDIA Isaac: Latest stable SDK
- Python: 3.10+
- Ubuntu: 22.04 LTS

### VI. Open Knowledge

Content MUST be structured for community learning, reuse, and collaborative improvement under open educational principles.

**Requirements:**
- Content licensed appropriately for reuse
- Clear attribution of sources
- Modular structure for easy extraction
- Community contribution guidelines
- Version control for collaborative editing

## Citation & Source Standards

### Citation Format
- Theory & Concepts: APA 7th Edition
- Technical Documentation: Direct links to official docs with version numbers
- Code Examples: Inline comments with source attribution

### Approved Source Types

**Tier 1: Peer-Reviewed Research (40% minimum)**
- IEEE Transactions on Robotics
- International Journal of Robotics Research
- ACM/IEEE Conference on Human-Robot Interaction
- arXiv preprints (with caution, marked as non-peer-reviewed)
- Nature Robotics, Science Robotics

**Tier 2: Official Technical Documentation (40% minimum)**
- ROS 2 Official Documentation (docs.ros.org)
- NVIDIA Isaac Documentation (docs.omniverse.nvidia.com/isaac)
- Gazebo Documentation (gazebosim.org)
- Unity Robotics Hub (github.com/Unity-Technologies/Unity-Robotics-Hub)
- OpenAI API Documentation

**Tier 3: Industry Whitepapers (20% maximum)**
- NVIDIA Technical Blogs
- Open Robotics Whitepapers
- McKinsey Robotics Reports
- Boston Dynamics Technical Papers

### Prohibited Sources
- Wikipedia (use only as starting point, not citation)
- Medium blogs (unless by verified experts)
- Stack Overflow answers (use concepts only, not direct citation)
- Unverified YouTube tutorials
- AI-generated content without human verification

### Source Verification Checklist
- Author credentials verified
- Publication date within last 5 years (for technical content)
- Content cross-referenced with official documentation
- No conflicts with established best practices

## Structural Constraints

### Book Format
- Platform: Docusaurus v3.x
- Markup: Markdown + MDX for interactive components
- Deployment: GitHub Pages (primary) or Vercel (backup)

### Module Structure

```text
ai-textbook/
├── docs/
│   ├── 00-introduction/
│   │   ├── 00-welcome.md
│   │   ├── 01-what-is-physical-ai.md
│   │   ├── 02-course-overview.md
│   │   └── 03-hardware-requirements.md
│   │
│   ├── 01-ros2-fundamentals/          # Module 1 (Weeks 3-5)
│   │   ├── 01-ros2-architecture.md
│   │   ├── 02-nodes-and-topics.md
│   │   ├── 03-services-and-actions.md
│   │   ├── 04-launch-files.md
│   │   ├── 05-urdf-basics.md
│   │   └── 06-rclpy-integration.md
│   │
│   ├── 02-simulation/                  # Module 2 (Weeks 6-7)
│   │   ├── 01-gazebo-setup.md
│   │   ├── 02-physics-simulation.md
│   │   ├── 03-sensor-simulation.md
│   │   ├── 04-unity-integration.md
│   │   └── 05-digital-twin-concepts.md
│   │
│   ├── 03-isaac-platform/              # Module 3 (Weeks 8-10)
│   │   ├── 01-isaac-overview.md
│   │   ├── 02-isaac-sim.md
│   │   ├── 03-isaac-ros.md
│   │   ├── 04-vslam-navigation.md
│   │   ├── 05-nav2-integration.md
│   │   └── 06-sim-to-real.md
│   │
│   ├── 04-vla-systems/                 # Module 4 (Weeks 11-13)
│   │   ├── 01-vision-language-action.md
│   │   ├── 02-whisper-integration.md
│   │   ├── 03-llm-cognitive-planning.md
│   │   ├── 04-multimodal-interaction.md
│   │   └── 05-conversational-robotics.md
│   │
│   ├── 05-capstone/
│   │   ├── 01-project-overview.md
│   │   ├── 02-system-design.md
│   │   ├── 03-implementation.md
│   │   └── 04-testing-deployment.md
│   │
│   └── 06-appendices/
│       ├── a-glossary.md
│       ├── b-troubleshooting.md
│       ├── c-resources.md
│       └── d-hardware-guide.md
```

### Chapter Template Structure

Every chapter MUST include these sections:

```markdown
# [Chapter Number]: [Chapter Title]

## Learning Objectives
- Objective 1 (specific, measurable)
- Objective 2
- Objective 3

## Prerequisites
- List of required prior knowledge
- Software/hardware requirements
- Estimated time to complete

## Conceptual Explanation
[Theory, context, why this matters]

## Tooling Overview
[Relevant software/hardware tools]
[Installation instructions if needed]

## Implementation Section
### Example 1: [Practical Example]
[Code, simulation, or hands-on exercise]

### Example 2: [Advanced Example]
[Building on previous example]

## Common Pitfalls
[Known errors and how to resolve them]

## Summary
- Key takeaway 1
- Key takeaway 2
- Key takeaway 3

## Further Reading
- [Source 1] - Brief description
- [Source 2] - Brief description

## AI Chat Prompt Suggestions
- "Explain [concept] in simpler terms"
- "Show me alternative approaches to [task]"
- "What are real-world applications of [topic]?"

## Practice Exercises
1. [Hands-on exercise]
2. [Challenge problem]
3. [Extension activity]
```

## RAG & AI Agent Standards

### Content Preparation for RAG

**Chunking Strategy:**
```python
CHUNK_CONFIG = {
    "size": 800,              # tokens per chunk
    "overlap": 100,           # token overlap
    "separator": "\n\n",      # semantic boundary
    "min_chunk_size": 200,    # minimum viable chunk
}
```

**Metadata Schema:**
```typescript
interface ChunkMetadata {
  module: string;              // "01-ros2-fundamentals"
  week: number;                // 3-5
  chapter: string;             // "02-nodes-and-topics"
  section: string;             // "Creating a Publisher Node"
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  keywords: string[];          // ["ROS 2", "publisher", "node"]
  hasCode: boolean;            // true if contains code
  language?: string;           // "python" | "cpp"
  prerequisites: string[];     // ["01-ros2-architecture"]
}
```

**Vector Database Configuration (Qdrant):**
```python
QDRANT_CONFIG = {
    "collection_name": "physical_ai_textbook",
    "vector_size": 1536,
    "distance": "Cosine",
    "on_disk_payload": True,    # Free tier optimization
    "quantization": {
        "scalar": {
            "type": "int8",
            "quantile": 0.99
        }
    }
}
```

### RAG Chatbot Requirements

**Core Capabilities:**
1. Full-Book Question Answering - Answer questions about any chapter, synthesize information across modules
2. Selected Text Question Answering - Answer ONLY based on user-highlighted text, no hallucination outside selection
3. Code Explanation - Explain code line-by-line, suggest improvements, debug common errors
4. Concept Clarification - Simplify complex topics, provide analogies, link to related chapters
5. Resource Recommendation - Suggest prerequisites, recommend advanced reading, link to official docs

**Retrieval Configuration:**
```python
RETRIEVAL_CONFIG = {
    "top_k": 5,                    # retrieve top 5 chunks
    "similarity_threshold": 0.75,  # minimum similarity
    "rerank": True,                # use cross-encoder reranking
    "context_window": 4000,        # tokens for LLM context
    "max_chunks_in_context": 3,    # after reranking
}
```

**Safety Filters:**
- No unsafe robotics instructions (e.g., disabling safety features)
- No fabricated hardware recommendations
- No encouragement to skip safety procedures
- Reject prompts attempting prompt injection

## Personalization & Localization Standards

### User Profile Schema

```typescript
interface UserProfile {
  // Identity
  userId: string;
  email: string;
  name: string;
  createdAt: Date;

  // Background Assessment
  softwareExperience: {
    programming: 'none' | 'beginner' | 'intermediate' | 'advanced' | 'expert';
    pythonLevel: 'none' | 'basic' | 'proficient' | 'expert';
    cppLevel: 'none' | 'basic' | 'proficient' | 'expert';
    linuxExperience: boolean;
    gitExperience: boolean;
  };

  roboticsBackground: {
    level: 'none' | 'hobbyist' | 'academic' | 'professional';
    hasROS1Experience: boolean;
    hasROS2Experience: boolean;
    hasGazeboExperience: boolean;
    hasIsaacExperience: boolean;
  };

  aimlBackground: {
    hasMLExperience: boolean;
    hasDeepLearningExperience: boolean;
    hasLLMExperience: boolean;
    hasComputerVisionExperience: boolean;
  };

  // Learning Preferences
  preferences: {
    learningPace: 'slow' | 'moderate' | 'fast';
    preferredLanguage: 'english' | 'urdu';
    showAdvancedTopics: boolean;
    codeCommentVerbosity: 'minimal' | 'moderate' | 'detailed';
  };

  // Progress Tracking
  progress: {
    completedChapters: string[];
    currentChapter: string;
    bookmarkedSections: string[];
  };
}
```

### Content Adaptation Matrix

| User Profile | Content Adjustments |
|--------------|---------------------|
| Beginner Programmer | Add Python basics, detailed code comments, slower progression, extra visualizations |
| No Linux Experience | Include Linux command primer, explain file system navigation, add terminal basics |
| Advanced Developer | Skip introductory sections, add advanced optimizations, performance tuning, additional challenges |
| No ROS Experience | Detailed ROS 2 fundamentals, extra ROS architecture diagrams, more hands-on examples |
| ROS 1 Veteran | Highlight ROS 1 vs ROS 2 differences, skip basic concepts, focus on migration tips |
| No Robotics Background | Add kinematics primer, explain robotics terminology, include more analogies |
| Professional Roboticist | Focus on Isaac and VLA, advanced simulation techniques, industry best practices |

### Urdu Translation Standards

**Translation Requirements:**
- Technical Accuracy: Preserve exact technical meaning
- Terminology: Use established Urdu technical terms where available
- Code: Keep code blocks in English (universal language of programming)
- Commands: Keep terminal commands in English
- Mixed Language: Use Romanized Urdu script (easier for technical readers)

**Translation Guidelines:**

| Element | Translation Approach | Example |
|---------|---------------------|---------|
| Concept Explanations | Full Urdu translation | "Nodes are..." → "Nodes aise software modules hain..." |
| Technical Terms | Urdu + English in parentheses | "Publisher (پبلشر)" |
| Code Comments | Urdu translation | # Create node → # Node banayein |
| Code Syntax | Keep in English | def main(): remains unchanged |
| Commands | Keep in English | ros2 run remains unchanged |
| Error Messages | Keep in English + Urdu explanation | "Error: ..." followed by Urdu explanation |

## Quality & Integrity Controls

### Plagiarism Standards
- Tolerance: 0%
- Run Turnitin or Copyscape on all written content
- Verify all code examples are original or properly attributed
- Document all inspirations and references

### AI-Generated Content Disclosure

**Requirement:** Mandatory in project documentation

**Disclosure Template:**
```markdown
## AI-Assisted Content

This textbook was created with assistance from AI tools:
- **Claude Code**: Project structure and code generation
- **Spec-Kit Plus**: Specification-driven development
- **AI Review**: All AI-generated content verified by human experts

All technical accuracy, code validity, and educational soundness
have been verified against official documentation and peer-reviewed sources.
```

### Fact-Checking Protocol

**Mandatory Fact-Checking for:**
- Hardware specifications (GPU models, memory, etc.)
- Software version numbers
- Command syntax
- Performance benchmarks
- Cost estimates
- API endpoints and parameters

**Fact-Checking Process:**
1. Identify Claim: Mark all factual claims
2. Find Primary Source: Locate official documentation
3. Verify: Cross-reference with multiple sources
4. Document: Add citation inline
5. Re-verify: Check before each publication

### Prohibited Content

**Unsafe Robotics Instructions:**
- Disabling safety features without explanation
- Operating robots without proper training
- Modifying hardware without safety considerations
- Skipping emergency stop procedures

**Fabricated Information:**
- Invented performance benchmarks
- Made-up hardware specifications
- Non-existent software features
- Fictional case studies without disclaimer

**Unverified Claims:**
- "Industry standard" without citation
- "Best practice" without source
- "Research shows" without reference
- "Experts recommend" without attribution

## Security & Deployment Standards

### API Key Management
- API keys MUST NEVER be stored in public repositories
- Use .env.example with placeholder values
- All secrets via environment variables

**.gitignore MUST include:**
```
.env
.env.local
.env.production
*.key
secrets/
config/api_keys.json
```

### Database Security (Neon Postgres)
- Role-based access with minimal privileges
- Connection strings via environment variables only
- Separate read-only roles for chatbot queries

### API Rate Limiting

```python
OPENAI_LIMITS = {
    "requests_per_minute": 3000,
    "tokens_per_minute": 250000,
    "requests_per_day": 10000,
}
```

### Deployment Security Checklist

**Pre-Deployment:**
- All API keys in environment variables
- .env files in .gitignore
- No hardcoded secrets in code
- Database credentials rotated
- HTTPS enforced for all endpoints
- CORS properly configured
- Rate limiting enabled
- Input validation implemented
- SQL injection protection verified
- XSS protection enabled

**Post-Deployment:**
- Monitor API usage
- Review access logs weekly
- Rotate secrets monthly
- Update dependencies for security patches
- Backup database daily
- Test disaster recovery

## Success Criteria

### Base Requirements (100 points)

**1. AI/Spec-Driven Book Creation (40 points)**
- Book written using Docusaurus
- Deployed to GitHub Pages or Vercel
- Used Spec-Kit Plus for specification-driven development
- Used Claude Code for implementation
- All 4 modules covered comprehensively

**2. RAG Chatbot Development (40 points)**
- Chatbot embedded in published book
- Uses OpenAI Agents/ChatKit SDK
- FastAPI backend deployed
- Neon Serverless Postgres integrated
- Qdrant Cloud Free Tier configured
- Answers questions about book content
- Supports "selected text only" queries

**3. Technical Quality (20 points)**
- Code quality and organization
- Documentation completeness
- Testing implementation
- Deployment stability
- No critical bugs

### Bonus Opportunities (150 points)

**Bonus 1: Claude Code Subagents (50 points)**
- Minimum 3 specialized subagents created
- Subagents demonstrate reusable intelligence
- Agent skills properly documented

**Bonus 2: Authentication System (50 points)**
- Better-Auth integration complete
- Signup/signin flows functional
- User background questionnaire at signup
- User profile stored securely

**Bonus 3: Content Personalization (50 points)**
- Personalization button at chapter start
- Content adapts based on user profile
- Adaptation visible and meaningful

**Bonus 4: Urdu Translation (50 points)**
- Translation button at chapter start
- Translates entire chapter to Urdu
- Preserves technical accuracy
- Code blocks remain in English

## Governance

### Amendment Procedure
1. All amendments MUST be documented with rationale
2. Amendments require explicit approval before implementation
3. Migration plan MUST accompany backward-incompatible changes
4. Version bumped according to semantic versioning rules

### Version Policy
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review
- All PRs/reviews MUST verify compliance with constitution principles
- Complexity MUST be justified against Principle VI (Open Knowledge)
- Technical accuracy claims MUST be fact-checked per Principle I
- Educational content MUST follow chapter template per Principle II

### Supersession
This constitution supersedes all other development practices for this project. In case of conflict between external guidelines and this constitution, this constitution takes precedence.

**Version**: 1.0.0 | **Ratified**: 2025-12-14 | **Last Amended**: 2025-12-14
