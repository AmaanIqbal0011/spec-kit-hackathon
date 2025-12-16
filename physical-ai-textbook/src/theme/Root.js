/**
 * Swizzled Root component for Docusaurus
 * Wraps the entire application with ChatbotProvider and renders the Chatbot
 * This ensures the chatbot is available on all pages.
 */

import React from 'react';
import { ChatbotProvider } from '../components/Chatbot/ChatbotProvider';
import Chatbot from '../components/Chatbot';

// Default implementation - wrap children
export default function Root({ children }) {
  return (
    <ChatbotProvider>
      {children}
      <Chatbot />
    </ChatbotProvider>
  );
}
