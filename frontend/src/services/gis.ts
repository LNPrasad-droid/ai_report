import api from './api'

export const processGis = (payload: any) => api.post('/gis/process', payload)
