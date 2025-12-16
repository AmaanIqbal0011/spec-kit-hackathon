/**
 * ChatbotProvider - Context provider for global chatbot state management
 *
 * Manages:
 * - Panel open/close state
 * - Messages array
 * - Loading state
 * - Error state
 * - API communication
 */

import React, { createContext, useContext, useState, useCallback } from 'react';
import { sendMessage as sendApiMessage } from './api';

// Create context
const ChatbotContext = createContext(null);

// Custom hook to use chatbot context
export function useChatbot() {
  const context = useContext(ChatbotContext);
  if (!context) {
    throw new Error('useChatbot must be used within a ChatbotProvider');
  }
  return context;
}

// Generate unique ID for messages
function generateId() {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

// Provider component
export function ChatbotProvider({ children }) {
  // Panel visibility state
  const [isOpen, setIsOpen] = useState(false);

  // Messages array - persists during session
  const [messages, setMessages] = useState([]);

  // Input field value
  const [inputValue, setInputValue] = useState('');

  // Loading state during API calls
  const [isLoading, setIsLoading] = useState(false);

  // Error state
  const [error, setError] = useState(null);

  // Track last message for retry
  const [lastQuery, setLastQuery] = useState(null);

  // Toggle panel open/close
  const togglePanel = useCallback(() => {
    setIsOpen(prev => !prev);
  }, []);

  // Open panel
  const openPanel = useCallback(() => {
    setIsOpen(true);
  }, []);

  // Close panel
  const closePanel = useCallback(() => {
    setIsOpen(false);
  }, []);

  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Convert messages to API history format
  const getHistoryForApi = useCallback((currentMessages) => {
    return currentMessages.map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.content,
    }));
  }, []);

  // Send message to API
  const sendMessage = useCallback(async (content) => {
    if (!content.trim()) return;

    // Clear any previous error
    setError(null);

    // Store query for retry
    setLastQuery(content);

    // Create user message
    const userMessage = {
      id: generateId(),
      content: content.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    // Add user message to list and get updated messages for history
    let updatedMessages;
    setMessages(prev => {
      updatedMessages = [...prev, userMessage];
      return updatedMessages;
    });

    // Clear input
    setInputValue('');

    // Set loading
    setIsLoading(true);

    try {
      // Get conversation history (excluding the current message we just added)
      // We need to use the messages state before adding the user message
      const history = getHistoryForApi(messages);

      // Call API with query and history
      const response = await sendApiMessage(content.trim(), history);

      // Create AI message
      const aiMessage = {
        id: generateId(),
        content: response,
        sender: 'ai',
        timestamp: new Date(),
      };

      // Add AI message to list
      setMessages(prev => [...prev, aiMessage]);

    } catch (err) {
      // Set error message
      setError(err.message || 'An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [messages, getHistoryForApi]);

  // Retry last message
  const retryLastMessage = useCallback(() => {
    if (lastQuery) {
      // Remove the last user message (failed one)
      setMessages(prev => prev.slice(0, -1));
      // Resend
      sendMessage(lastQuery);
    }
  }, [lastQuery, sendMessage]);

  // Clear all messages
  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  // Context value
  const value = {
    // State
    isOpen,
    messages,
    inputValue,
    isLoading,
    error,

    // Actions
    togglePanel,
    openPanel,
    closePanel,
    setInputValue,
    sendMessage,
    clearError,
    retryLastMessage,
    clearMessages,
  };

  return (
    <ChatbotContext.Provider value={value}>
      {children}
    </ChatbotContext.Provider>
  );
}

export default ChatbotProvider;
