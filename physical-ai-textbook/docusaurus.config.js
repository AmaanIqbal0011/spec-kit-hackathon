// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'From Digital Intelligence to Physical Embodiment',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://physical-ai-textbook.vercel.app',
  baseUrl: '/',

  organizationName: 'physical-ai-textbook',
  projectName: 'physical-ai-textbook',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/docs',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.jpg',
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Start Learning',
          },
          {
            href: 'https://github.com/physical-ai-textbook/physical-ai-textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Learning Modules',
            items: [
              {
                label: 'Introduction to Physical AI',
                to: '/docs/introduction',
              },
              {
                label: 'ROS 2 Fundamentals',
                to: '/docs/ros2',
              },
              {
                label: 'Simulation Environments',
                to: '/docs/simulation',
              },
            ],
          },
          {
            title: 'Advanced Topics',
            items: [
              {
                label: 'NVIDIA Isaac Platform',
                to: '/docs/isaac',
              },
              {
                label: 'Vision-Language-Action',
                to: '/docs/vla',
              },
              {
                label: 'Capstone Project',
                to: '/docs/capstone',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'ROS 2 Documentation',
                href: 'https://docs.ros.org/en/humble/',
              },
              {
                label: 'NVIDIA Isaac Sim',
                href: 'https://developer.nvidia.com/isaac-sim',
              },
              {
                label: 'Gazebo Simulation',
                href: 'https://gazebosim.org/',
              },
            ],
          },
        ],
        copyright: `Physical AI & Humanoid Robotics Textbook | Built with Docusaurus | ${new Date().getFullYear()}`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['bash', 'python', 'yaml'],
      },
    }),
};

export default config;
