/**
 * API Module for Chatbot
 * Simple and clean connection to Hugging Face backend
 */

// API URL Configuration
const HUGGING_FACE_URL = 'https://amaaniqbal0011-hackathon-backend.hf.space';
const LOCAL_URL = 'https://amaaniqbal0011-hackathon-backend.hf.space';
const TIMEOUT_MS = 30000; // 30 seconds

/**
 * Get the correct API URL based on current environment
 * This function is called dynamically to ensure correct URL in browser
 */
function getApiUrl() {
  // Check if we're in the browser
  if (typeof window === 'undefined') {
    return HUGGING_FACE_URL; // SSR/build time default
  }

  const hostname = window.location.hostname;

  // Use localhost backend if running locally
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    console.log('[Chatbot API] Running on localhost - using local backend');
    return LOCAL_URL;
  }

  // Use Hugging Face backend for production
  console.log('[Chatbot API] Running in production - using Hugging Face backend');
  return HUGGING_FACE_URL;
}

/**
 * Send a message to the chat API
 * @param {string} query - User's question
 * @param {Array} history - Conversation history
 * @returns {Promise<string>} AI response
 */
export async function sendMessage(query, history = []) {
  const apiUrl = getApiUrl(); // Get URL dynamically each time
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    console.log(`[Chatbot API] Sending request to: ${apiUrl}/chat`);

    const response = await fetch(`${apiUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, history }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `Server error: ${response.status}`);
    }

    const data = await response.json();
    console.log('[Chatbot API] Response received successfully');
    return data.response;

  } catch (error) {
    clearTimeout(timeoutId);

    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }

    if (error.message.includes('fetch')) {
      throw new Error('Cannot connect to backend. Please check your connection.');
    }

    throw error;
  }
}

/**
 * Check backend health
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  const apiUrl = getApiUrl(); // Get URL dynamically

  try {
    console.log(`[Chatbot API] Health check: ${apiUrl}/health`);
    const response = await fetch(`${apiUrl}/health`);
    if (!response.ok) throw new Error('Health check failed');
    return await response.json();
  } catch (error) {
    throw new Error('Cannot connect to AI service.');
  }
}

export default { sendMessage, checkHealth };
