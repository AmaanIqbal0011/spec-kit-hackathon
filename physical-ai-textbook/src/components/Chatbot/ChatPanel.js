/**
 * ChatPanel Component
 *
 * The main chat interface panel containing:
 * - Header with title and close button
 * - Message list with scroll
 * - Loading indicator
 * - Error display with retry
 * - Input area with send button
 */

import React, { useRef, useEffect } from 'react';
import { useChatbot } from './ChatbotProvider';
import { ChatMessage } from './ChatMessage';
import styles from './styles.module.css';

// Send icon SVG
const SendIcon = () => (
  <svg
    width="20"
    height="20"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <line x1="22" y1="2" x2="11" y2="13" />
    <polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);

// Loading spinner
const LoadingSpinner = () => (
  <div className={styles.loadingSpinner}>
    <div className={styles.spinner}></div>
    <span>Thinking...</span>
  </div>
);

export function ChatPanel({ isOpen, onClose }) {
  const {
    messages,
    inputValue,
    setInputValue,
    isLoading,
    error,
    sendMessage,
    clearError,
    retryLastMessage,
  } = useChatbot();

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const panelRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading]);

  // Focus input when panel opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Handle keyboard events
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Handle click outside to close
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (isOpen && panelRef.current && !panelRef.current.contains(e.target)) {
        // Check if click is on the floating button (don't close if so)
        const isFloatingButton = e.target.closest('[aria-label*="Chat Assistant"]');
        if (!isFloatingButton) {
          onClose();
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen, onClose]);

  // Handle send message
  const handleSend = () => {
    if (inputValue.trim() && !isLoading) {
      sendMessage(inputValue);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) return null;

  return (
    <div
      ref={panelRef}
      className={styles.chatPanel}
      role="dialog"
      aria-modal="true"
      aria-label="AI Chat Assistant"
    >
      {/* Header */}
      <div className={styles.chatHeader}>
        <h3 className={styles.chatTitle}>AI Assistant</h3>
        <button
          className={styles.closeButton}
          onClick={onClose}
          aria-label="Close chat"
        >
          &times;
        </button>
      </div>

      {/* Messages area */}
      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.emptyState}>
            <p>Ask me anything about the Physical AI & Robotics textbook!</p>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}

        {/* Loading indicator */}
        {isLoading && <LoadingSpinner />}

        {/* Error message */}
        {error && (
          <div className={styles.errorMessage}>
            <p>{error}</p>
            <button
              className={styles.retryButton}
              onClick={() => {
                clearError();
                retryLastMessage();
              }}
            >
              Try Again
            </button>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className={styles.inputArea}>
        <input
          ref={inputRef}
          type="text"
          className={styles.textInput}
          placeholder="Type your question..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          aria-label="Chat input"
        />
        <button
          className={styles.sendButton}
          onClick={handleSend}
          disabled={!inputValue.trim() || isLoading}
          aria-label="Send message"
        >
          <SendIcon />
        </button>
      </div>
    </div>
  );
}

export default ChatPanel;
