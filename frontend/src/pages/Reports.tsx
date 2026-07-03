import React from 'react'
import { useReports } from '../hooks/useReports'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Reports() {
  const { data, isLoading, error } = useReports()

  if (isLoading) return <LoadingSpinner />
  if (error) return <div className="p-4 bg-red-50">Failed to load reports</div>

  const reports = data || []

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Reports</h1>
      <div className="space-y-4">
        {reports.map((r: any) => (
          <div key={r.id} className="p-4 bg-white rounded shadow">
            <div className="font-medium">{r.title || r.name || r.id}</div>
            <div className="text-sm text-gray-500">{r.summary || r.created_at || ''}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
