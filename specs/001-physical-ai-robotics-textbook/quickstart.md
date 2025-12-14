# Quickstart: AI-Native Robotics Textbook

**Feature**: 001-physical-ai-robotics-textbook
**Date**: 2025-12-14

## Prerequisites

- Node.js 18+ installed ([download](https://nodejs.org/))
- npm or yarn package manager
- Git installed
- Code editor (VS Code recommended)
- Vercel account (for deployment)

## Quick Setup

### 1. Initialize Docusaurus Project

```bash
# Create new Docusaurus project
npx create-docusaurus@latest physical-ai-textbook classic

# Navigate to project
cd physical-ai-textbook

# Install dependencies
npm install
```

### 2. Start Development Server

```bash
npm run start
```

Site will be available at `http://localhost:3000`

### 3. Project Structure Overview

```text
physical-ai-textbook/
├── docs/                    # Module content goes here
├── src/
│   ├── components/          # React components
│   ├── css/custom.css       # Custom styles
│   └── pages/index.js       # Homepage
├── static/img/              # Images
├── docusaurus.config.js     # Site configuration
├── sidebars.js              # Navigation
└── package.json
```

## Configuration

### docusaurus.config.js

Key settings to configure:

```javascript
module.exports = {
  title: 'Physical AI & Robotics',
  tagline: 'From Digital Intelligence to Physical Embodiment',
  url: 'https://your-site.vercel.app',
  baseUrl: '/',

  themeConfig: {
    navbar: {
      title: 'Physical AI Textbook',
      items: [
        { to: '/docs/intro', label: 'Start Learning', position: 'left' },
        { href: 'https://github.com/your-repo', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Built with Docusaurus. ${new Date().getFullYear()}`,
    },
    colorMode: {
      defaultMode: 'light',
      respectPrefersColorScheme: true,
    },
  },
};
```

### sidebars.js

Configure 6-module navigation:

```javascript
module.exports = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: '1. Introduction to Physical AI',
      items: ['01-introduction/index'],
    },
    {
      type: 'category',
      label: '2. ROS 2 Fundamentals',
      items: ['02-ros2/index'],
    },
    {
      type: 'category',
      label: '3. Simulation',
      items: ['03-simulation/index'],
    },
    {
      type: 'category',
      label: '4. NVIDIA Isaac',
      items: ['04-isaac/index'],
    },
    {
      type: 'category',
      label: '5. VLA Systems',
      items: ['05-vla/index'],
    },
    {
      type: 'category',
      label: '6. Capstone Project',
      items: ['06-capstone/index'],
    },
  ],
};
```

## Module Template

Each module follows this structure:

```markdown
---
sidebar_position: 1
title: Module Title
---

# Module Title

## Introduction

Learning objectives:
- Objective 1
- Objective 2
- Objective 3

## Key Concepts

### Concept 1
[Explanation]

### Concept 2
[Explanation]

## Practical Workflows

### Workflow 1: [Title]
**Objective**: [What you'll learn]

**Steps**:
1. Step one
2. Step two
3. Step three

**Expected Outcome**: [Result]

### Workflow 2: [Title]
[Similar structure]

## Summary

Key takeaways:
- Point 1
- Point 2
- Point 3

## Knowledge Check

<details>
<summary>Question 1: [Question text]</summary>

A) Option A
B) Option B
C) Option C
D) Option D

**Answer**: [Correct letter]

**Explanation**: [Why this is correct]
</details>

[Repeat for 3-5 questions]

## References

- [Source 1](url) - Description
- [Source 2](url) - Description
```

## Custom CSS for Progress Bar

Add to `src/css/custom.css`:

```css
/* Reading progress bar */
.progress-bar {
  position: fixed;
  top: 60px;
  left: 0;
  width: 0%;
  height: 3px;
  background: var(--ifm-color-primary);
  z-index: 1000;
  transition: width 0.1s ease;
}

/* Dark mode adjustments */
[data-theme='dark'] .progress-bar {
  background: var(--ifm-color-primary-light);
}
```

## Deployment to Vercel

### 1. Create vercel.json

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "docusaurus-2"
}
```

### 2. Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deployment
vercel --prod
```

### 3. Configure Preview Deployments

In Vercel dashboard:
- Enable "Preview Deployments" for all branches
- Configure custom domain if needed

## Common Commands

| Command | Description |
|---------|-------------|
| `npm run start` | Start dev server |
| `npm run build` | Production build |
| `npm run serve` | Serve production build locally |
| `npm run clear` | Clear cache |

## Troubleshooting

### Build Errors

```bash
# Clear cache and rebuild
npm run clear
npm run build
```

### MDX Errors

- Check for unclosed tags
- Ensure JSX syntax is correct
- Verify frontmatter format

### Navigation Issues

- Verify `sidebars.js` paths match file locations
- Check `sidebar_position` in frontmatter
- Ensure all referenced files exist

## Next Steps

1. Create module folders: `docs/01-introduction/`, etc.
2. Add `index.md` to each module folder
3. Write content following module template
4. Test locally with `npm run start`
5. Deploy with `vercel --prod`
