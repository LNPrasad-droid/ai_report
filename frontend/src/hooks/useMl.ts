import { useMutation } from '@tanstack/react-query'
import { predict } from '../services/ml'

export const useMlPredict = () => {
  return useMutation((payload: any) => predict(payload).then((r) => r.data))
}
