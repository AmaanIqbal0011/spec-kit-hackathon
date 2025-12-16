import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

const modules = [
  {
    title: 'Introduction to Physical AI',
    number: '01',
    description: 'Discover the foundations of Physical AI and Embodied Intelligence that bridge digital minds with physical bodies.',
    link: '/docs/introduction',
    icon: '🤖',
    color: '#4F46E5',
  },
  {
    title: 'ROS 2 Fundamentals',
    number: '02',
    description: 'Master robot communication through nodes, topics, and services — the nervous system of modern robots.',
    link: '/docs/ros2',
    icon: '🔗',
    color: '#0891B2',
  },
  {
    title: 'Simulation Environments',
    number: '03',
    description: 'Build digital twins with Gazebo and Unity to test robot behavior safely before real-world deployment.',
    link: '/docs/simulation',
    icon: '🎮',
    color: '#059669',
  },
  {
    title: 'NVIDIA Isaac Platform',
    number: '04',
    description: 'Unlock GPU-accelerated perception, SLAM, and autonomous navigation capabilities.',
    link: '/docs/isaac',
    icon: '👁️',
    color: '#76B900',
  },
  {
    title: 'Vision-Language-Action',
    number: '05',
    description: 'Connect natural language understanding to physical robot actions using cutting-edge VLA systems.',
    link: '/docs/vla',
    icon: '🧠',
    color: '#8B5CF6',
  },
  {
    title: 'Capstone Project',
    number: '06',
    description: 'Integrate everything you\'ve learned into a complete humanoid robot system using NVIDIA GR00T.',
    link: '/docs/capstone',
    icon: '🚀',
    color: '#DC2626',
  },
];

const features = [
  {
    icon: '📚',
    title: 'Structured Learning',
    description: 'Progressive modules that build upon each other, from fundamentals to advanced integration.',
  },
  {
    icon: '🔬',
    title: 'Research-Backed',
    description: 'Content grounded in peer-reviewed research and official documentation from ROS, NVIDIA, and more.',
  },
  {
    icon: '✅',
    title: 'Self-Assessment',
    description: 'Knowledge checks in every module help you verify your understanding before moving forward.',
  },
];

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroBackground}></div>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroBadge}>Interactive Textbook</div>
          <h1 className={styles.heroTitle}>
            Physical AI &<br />
            <span className={styles.heroHighlight}>Humanoid Robotics</span>
          </h1>
          <p className={styles.heroSubtitle}>
            Bridge the gap between digital intelligence and physical embodiment.
            Learn to build robots that perceive, reason, and act in the real world.
          </p>
          <div className={styles.heroButtons}>
            <Link
              className={clsx('button button--lg', styles.primaryButton)}
              to="/docs/introduction">
              Start Learning
            </Link>
            <Link
              className={clsx('button button--lg', styles.secondaryButton)}
              to="/docs/intro">
              Browse Modules
            </Link>
          </div>
          <div className={styles.heroStats}>
            <div className={styles.stat}>
              <span className={styles.statNumber}>6</span>
              <span className={styles.statLabel}>Modules</span>
            </div>
            <div className={styles.statDivider}></div>
            <div className={styles.stat}>
              <span className={styles.statNumber}>8</span>
              <span className={styles.statLabel}>Workflows</span>
            </div>
            <div className={styles.statDivider}></div>
            <div className={styles.stat}>
              <span className={styles.statNumber}>30</span>
              <span className={styles.statLabel}>Questions</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({icon, title, description}) {
  return (
    <div className={clsx('col col--4', styles.featureCard)}>
      <div className={styles.featureIcon}>{icon}</div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((feature, idx) => (
            <FeatureCard key={idx} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}

function ModuleCard({title, number, description, link, icon, color}) {
  return (
    <Link to={link} className={styles.moduleCardLink}>
      <div className={styles.moduleCard}>
        <div className={styles.moduleNumber} style={{background: color}}>{number}</div>
        <div className={styles.moduleContent}>
          <div className={styles.moduleIcon}>{icon}</div>
          <h3 className={styles.moduleTitle}>{title}</h3>
          <p className={styles.moduleDescription}>{description}</p>
          <span className={styles.moduleArrow}>Start module →</span>
        </div>
      </div>
    </Link>
  );
}

function ModulesSection() {
  return (
    <section className={styles.modules}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Learning Path</h2>
          <p className={styles.sectionSubtitle}>
            Six comprehensive modules taking you from foundational concepts to building complete humanoid robot systems.
          </p>
        </div>
        <div className={styles.modulesGrid}>
          {modules.map((module, idx) => (
            <ModuleCard key={idx} {...module} />
          ))}
        </div>
      </div>
    </section>
  );
}

function AboutSection() {
  return (
    <section className={styles.about}>
      <div className="container">
        <div className="row">
          <div className="col col--6">
            <div className={styles.aboutCard}>
              <h2 className={styles.aboutTitle}>
                <span className={styles.aboutIcon}>🎯</span>
                What You'll Master
              </h2>
              <ul className={styles.aboutList}>
                <li><span className={styles.checkmark}>✓</span> Physical AI and Embodied Intelligence concepts</li>
                <li><span className={styles.checkmark}>✓</span> ROS 2 robot communication architecture</li>
                <li><span className={styles.checkmark}>✓</span> Gazebo and Unity simulation environments</li>
                <li><span className={styles.checkmark}>✓</span> NVIDIA Isaac perception and navigation</li>
                <li><span className={styles.checkmark}>✓</span> Vision-Language-Action (VLA) systems</li>
                <li><span className={styles.checkmark}>✓</span> Complete system integration skills</li>
              </ul>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.aboutCard}>
              <h2 className={styles.aboutTitle}>
                <span className={styles.aboutIcon}>📋</span>
                Prerequisites
              </h2>
              <ul className={styles.aboutList}>
                <li><span className={styles.checkmark}>✓</span> Basic programming knowledge</li>
                <li><span className={styles.checkmark}>✓</span> Command-line familiarity</li>
                <li><span className={styles.checkmark}>✓</span> Curiosity about robotics and AI</li>
              </ul>
              <div className={styles.aboutNote}>
                <strong>No prior robotics experience needed!</strong> All concepts are introduced progressively,
                building your knowledge step by step.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.cta}>
      <div className="container">
        <div className={styles.ctaContent}>
          <h2 className={styles.ctaTitle}>Ready to Build Intelligent Robots?</h2>
          <p className={styles.ctaSubtitle}>
            Start your journey into Physical AI today. No signup required.
          </p>
          <Link
            className={clsx('button button--lg', styles.ctaButton)}
            to="/docs/introduction">
            Begin Module 1
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <Layout
      title="Welcome"
      description="Physical AI & Humanoid Robotics Textbook - From Digital Intelligence to Physical Embodiment. Learn ROS 2, simulation, NVIDIA Isaac, and VLA systems.">
      <HomepageHeader />
      <main>
        <FeaturesSection />
        <ModulesSection />
        <AboutSection />
        <CTASection />
      </main>
    </Layout>
  );
}
