import api from './api'

export const searchSatellite = (payload: any) => api.post('/satellite/search', payload)
