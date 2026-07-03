import api from './api'

// Create a new job from a conversation payload. Backend orchestrator will process it.
export const createJobFromConversation = (payload: any) => api.post('/jobs', payload)
