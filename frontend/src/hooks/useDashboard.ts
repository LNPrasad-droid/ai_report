import { useQuery } from '@tanstack/react-query'
import { getJobs } from '../services/jobs'
import { getReports } from '../services/reports'

export const useDashboard = () => {
  const jobs = useQuery(['jobs', { recent: true }], () => getJobs({ limit: 10 }).then((r) => r.data), { staleTime: 1000 * 30 })
  const reports = useQuery(['reports', { recent: true }], () => getReports({ limit: 10 }).then((r) => r.data), { staleTime: 1000 * 60 })

  const summary = {
    running: (jobs.data || []).filter((j: any) => j.status === 'running').length,
    completed: (jobs.data || []).filter((j: any) => j.status === 'completed').length,
    failed: (jobs.data || []).filter((j: any) => j.status === 'failed').length,
    recentJobs: jobs.data || [],
    recentReports: reports.data || [],
  }

  return { jobs, reports, summary }
}
