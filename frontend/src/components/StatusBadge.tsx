import React from 'react'

export default function StatusBadge({ status }: { status?: string }) {
  const s = (status || '').toLowerCase()
  const map: Record<string, string> = {
    running: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    pending: 'bg-gray-100 text-gray-800',
    error: 'bg-red-100 text-red-800',
    default: 'bg-gray-100 text-gray-800',
  }
  const cls = map[s] || map.default
  return <span className={`px-2 py-1 rounded text-xs font-medium ${cls}`}>{status || 'unknown'}</span>
}
