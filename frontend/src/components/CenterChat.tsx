import React, { useState, useRef, useEffect } from 'react'
import MessageItem from './MessageItem'
import { useCreateJob } from '../hooks/useCreateJob'
import LoadingSpinner from './LoadingSpinner'

export default function CenterChat({ conversation, addMessage, setAoiFiles, aoiFiles, satOptions }: any) {
  const [text, setText] = useState('')
  const createJob = useCreateJob()
  const [uploading, setUploading] = useState(false)
  const listRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight })
  }, [conversation])

  const updateAoi = (id: string, patch: any) => {
    setAoiFiles((files: any[]) => files.map((item) => (item.id === id ? { ...item, ...patch } : item)))
  }

  const uploadOne = async (fileItem: any) => {
    setUploading(true)
    updateAoi(fileItem.id, { status: 'uploading', progress: 0 })
    try {
      const uploadModule = await import('../services/upload')
      const res = await uploadModule.uploadAOI(fileItem.file, (p: number) => updateAoi(fileItem.id, { progress: p }))
      const meta = res.data
      updateAoi(fileItem.id, { status: 'uploaded', progress: 100, meta, file_id: meta.file_id || meta.fileId || meta.id })
      return meta
    } finally {
      setUploading(false)
    }
  }

  const send = async () => {
    if (!text.trim()) return
    const msg = { id: `m_${Date.now()}`, type: 'user', content: text, created_at: new Date().toISOString() }
    addMessage(conversation.id, msg)
    setText('')

    const payloadBase: any = { conversation_id: conversation.id, messages: [...(conversation.messages || []), msg] }
    const fileIds: string[] = []

    if (aoiFiles?.length) {
      for (const fileItem of aoiFiles) {
        if (fileItem.status === 'uploaded' && fileItem.file_id) {
          fileIds.push(fileItem.file_id)
          continue
        }

        addMessage(conversation.id, { id: `m_${Date.now()+Math.random()}`, type: 'system', content: `Uploading ${fileItem.name}...`, created_at: new Date().toISOString() })
        try {
          const meta = await uploadOne(fileItem)
          fileIds.push(meta.file_id || meta.fileId || meta.id)
        } catch (err: any) {
          updateAoi(fileItem.id, { status: 'failed' })
          addMessage(conversation.id, { id: `m_${Date.now()+Math.random()}`, type: 'system', content: `Upload failed for ${fileItem.name}`, meta: { error: err?.message || err } })
          return
        }
      }
      payloadBase.aoi_file_ids = fileIds
    }

    if (satOptions) payloadBase.satellite = satOptions

    try {
      const res = await createJob.mutateAsync(payloadBase)
      const assistantMsg = { id: `m_${Date.now()+1}`, type: 'assistant', content: 'Processing…', created_at: new Date().toISOString(), meta: { job_id: res.id } }
      addMessage(conversation.id, assistantMsg)
    } catch (err: any) {
      addMessage(conversation.id, { id: `m_${Date.now()+2}`, type: 'system', content: 'Failed to send request', meta: { error: err?.message || err } })
    }
  }

  return (
    <div className="flex-1 flex flex-col h-screen">
      <div ref={listRef} className="flex-1 overflow-auto p-4 space-y-4">
        {(conversation.messages || []).map((m: any) => (
          <MessageItem key={m.id} message={m} />
        ))}
      </div>
      <div className="p-4 border-t">
        <div className="flex gap-2">
          <textarea value={text} onChange={(e) => setText(e.target.value)} className="flex-1 p-2 border rounded" rows={3} />
          <div className="flex flex-col">
            <button onClick={send} className="px-4 py-2 bg-blue-600 text-white rounded mb-2">Send</button>
            {uploading && <LoadingSpinner />}
          </div>
        </div>
      </div>
    </div>
  )
}
