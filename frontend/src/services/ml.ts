import api from './api'

export const predict = (payload: any) => api.post('/ml/predict', payload)
