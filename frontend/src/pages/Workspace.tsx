import React, { useState } from 'react'
import LeftSidebar from '../components/LeftSidebar'
import CenterChat from '../components/CenterChat'
import RightSidebar from '../components/RightSidebar'
import { useConversation } from '../hooks/useConversation'
import { useJob } from '../hooks/useJob'
import { useExecution } from '../hooks/useMonitoring'

export default function Workspace() {
  const { conversations, activeConversation, createConversation, addMessage, setActiveId } = useConversation()
  const [aoiFiles, setAoiFiles] = useState<any[]>([])
  const [selectedAoiId, setSelectedAoiId] = useState<string | undefined>()
  const [satOptions, setSatOptions] = useState<any>({ satellite: 'Sentinel-2', start: '', end: '', cloud: 10 })

  const currentJobId = activeConversation?.messages?.slice().reverse().find((m: any) => m.meta?.job_id)?.meta?.job_id
  const { data: jobData } = useJob(currentJobId)
  const { data: executionData } = useExecution(currentJobId)

  const addFiles = (files: File[]) => {
    const items = files.map((file) => ({
      id: `aoi_${Date.now()}_${file.name}`,
      file,
      name: file.name,
      type: file.type || file.name.split('.').pop(),
      status: 'pending',
      progress: 0,
      meta: {},
    }))
    setAoiFiles((existing) => [...existing, ...items])
    if (!selectedAoiId && items.length > 0) {
      setSelectedAoiId(items[0].id)
    }
  }

  const removeAoi = (id: string) => {
    setAoiFiles((files) => {
      const remaining = files.filter((file) => file.id !== id)
      if (selectedAoiId === id) {
        setSelectedAoiId(remaining[0]?.id)
      }
      return remaining
    })
  }

  const renameAoi = (id: string) => {
    setAoiFiles((files) => {
      const current = files.find((item) => item.id === id)
      const name = prompt('Rename AOI', current?.name)
      if (!name || !current) return files
      return files.map((file) => (file.id === id ? { ...file, name } : file))
    })
  }

  const selectAoi = (id: string) => setSelectedAoiId(id)

  return (
    <div className="flex">
      <LeftSidebar conversations={conversations} activeId={activeConversation?.id} onSelect={(id: string) => setActiveId(id)} onNew={() => createConversation()} />
      <div className="flex-1 flex flex-col">
        {activeConversation ? (
          <CenterChat conversation={activeConversation} addMessage={addMessage} setAoiFiles={setAoiFiles} aoiFiles={aoiFiles} satOptions={satOptions} />
        ) : (
          <div className="p-8">No active conversation. Create one.</div>
        )}
      </div>
      <RightSidebar
        job={jobData}
        execution={executionData}
        aoiFiles={aoiFiles}
        selectedAoiId={selectedAoiId}
        onFilesSelected={addFiles}
        onRemoveAoi={removeAoi}
        onRenameAoi={renameAoi}
        onSelectAoi={selectAoi}
        satOptions={satOptions}
        onSatOptionsChange={setSatOptions}
      />
    </div>
  )
}
