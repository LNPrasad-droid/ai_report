import React from 'react'
import StatusBadge from './StatusBadge'

type Step = {
  name?: string
  status?: string
  start_time?: string
  end_time?: string
  duration_ms?: number
  output_summary?: any
  error?: any
}

export default function TimelineView({ steps }: { steps?: Step[] }) {
  if (!steps || steps.length === 0) return <div className="p-4 bg-white rounded shadow">No timeline available</div>

  return (
    <div className="space-y-4">
      {steps.map((s, idx) => (
        <div key={idx} className="p-4 bg-white rounded shadow">
          <div className="flex items-center justify-between">
            <div className="font-medium">{s.name || `Step ${idx + 1}`}</div>
            <StatusBadge status={s.status} />
          </div>
          <div className="text-sm text-gray-600 mt-2">Start: {s.start_time || 'n/a'}</div>
          <div className="text-sm text-gray-600">End: {s.end_time || 'n/a'}</div>
          <div className="text-sm text-gray-600">Duration: {s.duration_ms ? `${(s.duration_ms / 1000).toFixed(2)}s` : 'n/a'}</div>
          {s.output_summary && (
            <div className="mt-2 text-sm">
              <div className="font-semibold">Output Summary</div>
              <pre className="text-xs whitespace-pre-wrap">{typeof s.output_summary === 'string' ? s.output_summary : JSON.stringify(s.output_summary, null, 2)}</pre>
            </div>
          )}
          {s.error && (
            <div className="mt-2 text-sm text-red-700">
              <div className="font-semibold">Error</div>
              <pre className="text-xs whitespace-pre-wrap">{typeof s.error === 'string' ? s.error : JSON.stringify(s.error, null, 2)}</pre>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
