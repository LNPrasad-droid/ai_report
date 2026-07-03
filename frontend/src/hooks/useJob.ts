import { useQuery } from '@tanstack/react-query'
import { getJob } from '../services/jobs'

export const useJob = (id?: string) => {
  return useQuery(['job', id], () => getJob(id!).then((r) => r.data), {
    enabled: !!id,
    refetchInterval: (data) => (data?.status === 'running' ? 2000 : false),
  })
}
