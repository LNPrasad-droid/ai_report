import React from 'react'
import { useParams } from 'react-router-dom'
import { useExecution } from '../hooks/useMonitoring'
import LoadingSpinner from '../components/LoadingSpinner'
import TimelineView from '../components/TimelineView'

export default function ExecutionTimeline() {
  const { jobId } = useParams()
  const { data, isLoading, error } = useExecution(jobId)

  if (isLoading) return <LoadingSpinner />
  if (error) return <div className="p-4 bg-red-50">Failed to load execution</div>

  const exec = data || {}
  const steps = exec.steps || exec.timeline || exec.execution || []

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Execution Timeline — {jobId}</h1>
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Status</div>
          <div className="text-lg font-bold">{exec.status || '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Duration</div>
          <div className="text-lg font-bold">{exec.duration_ms ? `${(exec.duration_ms/1000).toFixed(2)}s` : '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Retries</div>
          <div className="text-lg font-bold">{exec.retry_count ?? 0}</div>
        </div>
      </div>

      <TimelineView steps={steps} />
    </div>
  )
}
