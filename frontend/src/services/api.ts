import axios from 'axios'
import { getAuth } from 'firebase/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 60000,
})

// Attach token from localStorage or current Firebase user
api.interceptors.request.use(async (config) => {
  config.headers = config.headers || {}
  const stored = localStorage.getItem('firebase_token')
  if (stored) {
    config.headers['Authorization'] = `Bearer ${stored}`
    return config
  }
  try {
    const auth = getAuth()
    const user = auth.currentUser
    if (user) {
      const token = await user.getIdToken()
      localStorage.setItem('firebase_token', token)
      config.headers['Authorization'] = `Bearer ${token}`
    }
  } catch (err) {
    // ignore - request will go without token
  }
  return config
})

// On 401 attempt to refresh token once and retry
api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config
    if (!original || original._retry) return Promise.reject(error)
    if (error.response && error.response.status === 401) {
      original._retry = true
      try {
        const auth = getAuth()
        const user = auth.currentUser
        if (user) {
          const fresh = await user.getIdToken(true)
          localStorage.setItem('firebase_token', fresh)
          original.headers = original.headers || {}
          original.headers['Authorization'] = `Bearer ${fresh}`
          return api(original)
        }
      } catch (e) {
        // fallthrough
      }
    }
    return Promise.reject(error)
  }
)

export default api
