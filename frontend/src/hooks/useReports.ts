import { useQuery } from '@tanstack/react-query'
import { getReports } from '../services/reports'

export const useReports = () => {
  return useQuery(['reports'], () => getReports().then((r) => r.data), { staleTime: 1000 * 60 })
}
