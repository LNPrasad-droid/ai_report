import { useMutation, useQueryClient } from '@tanstack/react-query'
import { createJobFromConversation } from '../services/chat'

export const useCreateJob = () => {
  const qc = useQueryClient()
  return useMutation((payload: any) => createJobFromConversation(payload).then((r) => r.data), {
    onSuccess: (data) => {
      // invalidate jobs list
      qc.invalidateQueries(['jobs'])
    },
  })
}

export default useCreateJob
