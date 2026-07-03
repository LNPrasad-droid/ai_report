import api from './api'

export const getReports = (params?: any) => api.get('/report', { params })
export const getReport = (id: string) => api.get(`/report/${id}`)
