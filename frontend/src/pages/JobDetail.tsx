import React from 'react'
import { useParams } from 'react-router-dom'
import { useJob } from '../hooks/useJob'
import LoadingSpinner from '../components/LoadingSpinner'
import TimelineView from '../components/TimelineView'

export default function JobDetail() {
  const { id } = useParams()
  const { data, isLoading, error } = useJob(id)

  if (isLoading) return <LoadingSpinner />
  if (error) return <div className="p-4 bg-red-50">Failed to load job</div>

  const job: any = data
  const steps = job?.steps || job?.timeline || job?.execution || []

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Job {job.id || id}</h1>
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-white rounded shadow">
          <h2 className="font-semibold">Status</h2>
          <div className="mt-2">{job.status}</div>
          <h2 className="font-semibold mt-4">Progress</h2>
          <div className="mt-2">{job.progress || 'N/A'}</div>
          <h2 className="font-semibold mt-4">Duration</h2>
          <div className="mt-2">{job.duration || job.duration_ms ? `${(job.duration_ms/1000).toFixed(2)}s` : 'N/A'}</div>
          <h2 className="font-semibold mt-4">Retries</h2>
          <div className="mt-2">{job.retry_count ?? 0}</div>
        </div>

        <div className="col-span-2">
          <div className="p-4 bg-white rounded shadow mb-4">
            <h2 className="font-semibold">Execution Summary</h2>
            <pre className="mt-2 text-sm whitespace-pre-wrap">{JSON.stringify(job.summary || job.execution_summary || {}, null, 2)}</pre>
          </div>

          <div className="p-4 bg-white rounded shadow mb-4">
            <h2 className="font-semibold">Intermediate Results</h2>
            <pre className="mt-2 text-sm whitespace-pre-wrap">{JSON.stringify(job.intermediate_results || job.results || {}, null, 2)}</pre>
          </div>

          <div className="p-4 bg-white rounded shadow">
            <h2 className="font-semibold">Execution Timeline</h2>
            <TimelineView steps={steps} />
          </div>
        </div>
      </div>

      <div className="mt-4 p-4 bg-white rounded shadow">
        <h2 className="font-semibold">Logs</h2>
        <pre className="mt-2 text-sm whitespace-pre-wrap">{job.logs || 'No logs available'}</pre>
      </div>
    </div>
  )
}
