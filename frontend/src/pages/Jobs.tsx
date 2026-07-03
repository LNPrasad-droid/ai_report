import React from 'react'
import { useJobs } from '../hooks/useJobs'
import LoadingSpinner from '../components/LoadingSpinner'
import { Link } from 'react-router-dom'

export default function Jobs() {
  const { data, isLoading, error } = useJobs({})

  if (isLoading) return <LoadingSpinner />
  if (error) return <div className="p-4 bg-red-50">Failed to load jobs</div>

  const jobs = data || []

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Job History</h1>
      <div className="space-y-4">
        {jobs.map((j: any) => (
          <div key={j.id} className="p-4 bg-white rounded shadow flex justify-between items-center">
            <div>
              <Link to={`/jobs/${j.id}`} className="text-lg font-medium text-blue-600">{j.name || j.id}</Link>
              <div className="text-sm text-gray-600">{j.status} • {j.type || ''}</div>
            </div>
            <div className="text-sm text-gray-500">{j.duration || ''}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
