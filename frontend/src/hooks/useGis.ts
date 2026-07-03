import { useMutation } from '@tanstack/react-query'
import { processGis } from '../services/gis'

export const useGisProcess = () => {
  return useMutation((payload: any) => processGis(payload).then((r) => r.data))
}
