/**
 * Chatbot Component - Main Export
 *
 * Combines FloatingButton and ChatPanel into a single chatbot widget.
 * Uses ChatbotProvider context for state management.
 */

import React from 'react';
import { useChatbot } from './ChatbotProvider';
import { FloatingButton } from './FloatingButton';
import { ChatPanel } from './ChatPanel';

// Re-export components for external use
export { ChatbotProvider, useChatbot } from './ChatbotProvider';
export { FloatingButton } from './FloatingButton';
export { ChatPanel } from './ChatPanel';
export { ChatMessage } from './ChatMessage';

/**
 * Main Chatbot Component
 *
 * Renders the floating button and chat panel.
 * Must be used within a ChatbotProvider context.
 */
export function Chatbot() {
  const { isOpen, togglePanel, closePanel } = useChatbot();

  return (
    <>
      <FloatingButton onClick={togglePanel} isOpen={isOpen} />
      <ChatPanel isOpen={isOpen} onClose={closePanel} />
    </>
  );
}

export default Chatbot;
