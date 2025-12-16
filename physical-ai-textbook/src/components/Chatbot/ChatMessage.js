/**
 * ChatMessage Component
 *
 * Renders a single message in the chat panel.
 * Displays user messages right-aligned and AI messages left-aligned.
 */

import React from 'react';
import styles from './styles.module.css';

export function ChatMessage({ message }) {
  const { content, sender, timestamp } = message;
  const isUser = sender === 'user';

  // Format timestamp
  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div
      className={`${styles.message} ${isUser ? styles.userMessage : styles.aiMessage}`}
    >
      <div className={styles.messageContent}>
        {content}
      </div>
      <div className={styles.messageTimestamp}>
        {formatTime(timestamp)}
      </div>
    </div>
  );
}

export default ChatMessage;
