import React from 'react'
import { useMetrics } from '../hooks/useMonitoring'
import LoadingSpinner from '../components/LoadingSpinner'
import MonitoringCharts from '../components/MonitoringCharts'

export default function MonitoringDashboard() {
  const { data, isLoading, error } = useMetrics()

  if (isLoading) return <LoadingSpinner />
  if (error) return <div className="p-4 bg-red-50">Failed to load metrics</div>

  const m = data || {}

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Monitoring Dashboard</h1>
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Total Jobs</div>
          <div className="text-2xl font-bold">{m.total_jobs ?? '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Running Jobs</div>
          <div className="text-2xl font-bold">{m.running_jobs ?? '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Completed Jobs</div>
          <div className="text-2xl font-bold">{m.completed_jobs ?? '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Failed Jobs</div>
          <div className="text-2xl font-bold">{m.failed_jobs ?? '—'}</div>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Average Execution Time</div>
          <div className="text-xl font-bold">{m.avg_execution_time ? `${(m.avg_execution_time/1000).toFixed(2)}s` : '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Average LLM Response</div>
          <div className="text-xl font-bold">{m.avg_llm_time ? `${(m.avg_llm_time/1000).toFixed(2)}s` : '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Average GIS Time</div>
          <div className="text-xl font-bold">{m.avg_gis_time ? `${(m.avg_gis_time/1000).toFixed(2)}s` : '—'}</div>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <div className="text-sm text-gray-500">Average ML Inference</div>
          <div className="text-xl font-bold">{m.avg_ml_time ? `${(m.avg_ml_time/1000).toFixed(2)}s` : '—'}</div>
        </div>
      </div>

      <MonitoringCharts data={m} />
    </div>
  )
}
