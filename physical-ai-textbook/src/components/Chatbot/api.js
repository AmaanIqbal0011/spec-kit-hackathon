/**
 * API Module for Chatbot
 *
 * Handles communication with the FastAPI backend.
 * Includes timeout handling and error parsing.
 */

// API Configuration
// Automatically detect the environment and use the correct API URL
// Use function to avoid SSR issues with window object
const getApiUrl = () => {
  // If environment variable is set, use it
  if (typeof process !== 'undefined' && process.env?.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }

  // Client-side detection
  if (typeof window !== 'undefined') {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }
    return 'https://your-api-endpoint.vercel.app';
  }

  // Default for SSR
  return 'http://localhost:8000';
};

const API_URL = getApiUrl();

// Timeout in milliseconds (30 seconds per spec)
const TIMEOUT_MS = 30000;

/**
 * Send a message to the chat API with conversation history
 *
 * @param {string} query - The user's question
 * @param {Array<{role: string, content: string}>} history - Previous messages in the conversation
 * @returns {Promise<string>} The AI agent's response
 * @throws {Error} If the request fails or times out
 */
export async function sendMessage(query, history = []) {
  // Create abort controller for timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, history }),
      signal: controller.signal,
    });

    // Clear timeout on successful response
    clearTimeout(timeoutId);

    // Handle HTTP errors
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.detail || getErrorMessage(response.status);
      throw new Error(errorMessage);
    }

    // Parse response
    const data = await response.json();
    return data.response;

  } catch (error) {
    // Clear timeout on error
    clearTimeout(timeoutId);

    // Handle abort (timeout)
    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }

    // Handle network errors
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Connection failed. Please check your internet connection.');
    }

    // Re-throw other errors
    throw error;
  }
}

/**
 * Get user-friendly error message based on HTTP status code
 *
 * @param {number} status - HTTP status code
 * @returns {string} User-friendly error message
 */
function getErrorMessage(status) {
  switch (status) {
    case 400:
      return 'Invalid request. Please try again.';
    case 500:
      return 'Server error. Please try again later.';
    case 503:
      return 'AI service is temporarily unavailable. Please try again.';
    default:
      return 'An error occurred. Please try again.';
  }
}

/**
 * Check API health status
 *
 * @returns {Promise<{status: string, version: string}>} Health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return await response.json();
  } catch (error) {
    throw new Error('Unable to connect to the AI service.');
  }
}

export default { sendMessage, checkHealth };
