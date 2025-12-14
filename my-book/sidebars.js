// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: '1. Introduction to Physical AI',
      collapsed: false,
      link: {
        type: 'doc',
        id: 'introduction/index',
      },
      items: [],
    },
    {
      type: 'category',
      label: '2. ROS 2 Fundamentals',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'ros2/index',
      },
      items: [],
    },
    {
      type: 'category',
      label: '3. Simulation Environments',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'simulation/index',
      },
      items: [],
    },
    {
      type: 'category',
      label: '4. NVIDIA Isaac Platform',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'isaac/index',
      },
      items: [],
    },
    {
      type: 'category',
      label: '5. Vision-Language-Action',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'vla/index',
      },
      items: [],
    },
    {
      type: 'category',
      label: '6. Capstone Project',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'capstone/index',
      },
      items: [],
    },
  ],
};

export default sidebars;
