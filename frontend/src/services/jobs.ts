import api from './api'

export const getJobs = (params?: any) => api.get('/jobs', { params })
export const getJob = (id: string) => api.get(`/jobs/${id}`)
