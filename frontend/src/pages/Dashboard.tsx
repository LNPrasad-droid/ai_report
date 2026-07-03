import React from 'react'
import { useDashboard } from '../hooks/useDashboard'
import LoadingSpinner from '../components/LoadingSpinner'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const { jobs, reports, summary } = useDashboard()

  if (jobs.isLoading || reports.isLoading) return <LoadingSpinner />

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-white rounded shadow">
          <h3 className="text-sm text-gray-500">Running Jobs</h3>
          <div className="text-2xl font-bold">{summary.running}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <h3 className="text-sm text-gray-500">Completed Jobs</h3>
          <div className="text-2xl font-bold">{summary.completed}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <h3 className="text-sm text-gray-500">Failed Jobs</h3>
          <div className="text-2xl font-bold">{summary.failed}</div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mt-6">
        <div className="p-4 bg-white rounded shadow">
          <h2 className="font-semibold">Recent Jobs</h2>
          <ul className="mt-2 space-y-2">
            {(summary.recentJobs || []).slice(0, 6).map((j: any) => (
              <li key={j.id}>
                <Link to={`/jobs/${j.id}`} className="text-blue-600">{j.name || j.id}</Link>
                <div className="text-sm text-gray-600">{j.status} • {j.type || ''}</div>
              </li>
            ))}
          </ul>
        </div>

        <div className="p-4 bg-white rounded shadow">
          <h2 className="font-semibold">Recent Reports</h2>
          <ul className="mt-2 space-y-2">
            {(summary.recentReports || []).slice(0, 6).map((r: any) => (
              <li key={r.id}>
                <div className="text-sm">{r.title || r.name || r.id}</div>
                <div className="text-xs text-gray-500">{r.created_at || r.createdAt || ''}</div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
