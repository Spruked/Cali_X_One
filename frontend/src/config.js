// frontend/src/config.js
// FAIL FAST if env vars are missing
export const API_URL = import.meta.env.VITE_API_URL
export const WS_URL = import.meta.env.VITE_WS_URL

if (!API_URL) {
  throw new Error('❌ VITE_API_URL not defined. Create .env.frontend')
}