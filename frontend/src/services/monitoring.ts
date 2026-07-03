import api from './api'

export const getMetrics = () => api.get('/monitoring/metrics')
export const getExecution = (jobId: string) => api.get(`/monitoring/executions/${jobId}`)
