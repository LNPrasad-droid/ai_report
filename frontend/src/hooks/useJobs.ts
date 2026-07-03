import { useQuery } from '@tanstack/react-query'
import { getJobs } from '../services/jobs'

export const useJobs = (params?: any) => {
  return useQuery(['jobs', params || {}], () => getJobs(params).then((r) => r.data), { staleTime: 1000 * 30 })
}
