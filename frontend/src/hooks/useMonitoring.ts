import { useQuery } from '@tanstack/react-query'
import { getMetrics, getExecution } from '../services/monitoring'

export const useMetrics = () => {
  return useQuery(['metrics'], () => getMetrics().then((r) => r.data), { staleTime: 1000 * 10, refetchInterval: 10000 })
}

export const useExecution = (jobId?: string) => {
  return useQuery(['execution', jobId], () => getExecution(jobId!).then((r) => r.data), { enabled: !!jobId, refetchInterval: (data) => (data?.status === 'running' ? 2000 : false) })
}
