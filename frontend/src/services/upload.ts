import api from './api'

export const uploadAOI = (file: File, onProgress?: (percent: number) => void) => {
  const form = new FormData()
  form.append('file', file)
  return api.post('/files/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent: ProgressEvent) => {
      if (progressEvent.total) {
        const p = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress && onProgress(p)
      }
    },
  })
}

export default uploadAOI
