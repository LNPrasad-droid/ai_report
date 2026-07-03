import { useMutation } from '@tanstack/react-query'
import { searchSatellite } from '../services/satellite'

export const useSatelliteSearch = () => {
  return useMutation((payload: any) => searchSatellite(payload).then((r) => r.data))
}
