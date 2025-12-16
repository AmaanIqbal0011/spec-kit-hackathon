/**
 * FloatingButton Component
 *
 * A persistent floating button in the bottom-right corner
 * that toggles the chat panel open/closed.
 */

import React from 'react';
import styles from './styles.module.css';

// Chat icon SVG
const ChatIcon = () => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </svg>
);

// Close icon SVG
const CloseIcon = () => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);

export function FloatingButton({ onClick, isOpen }) {
  return (
    <button
      className={styles.floatingButton}
      onClick={onClick}
      aria-label={isOpen ? 'Close AI Chat Assistant' : 'Open AI Chat Assistant'}
      title={isOpen ? 'Close chat' : 'Ask AI Assistant'}
    >
      {isOpen ? <CloseIcon /> : <ChatIcon />}
    </button>
  );
}

export default FloatingButton;
