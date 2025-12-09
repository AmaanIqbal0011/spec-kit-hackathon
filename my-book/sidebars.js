// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Learning Modules',
      items: [
        'lesson-01',
        'lesson-02',
        'lesson-03',
        'lesson-04',
        'lesson-05',
        'lesson-06',
      ],
    },
    'references',
  ],
};

export default sidebars;
