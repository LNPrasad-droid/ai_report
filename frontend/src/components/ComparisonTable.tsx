import React from 'react'

export default function ComparisonTable({ data = [] }: any) {
  if (!data || data.length === 0) {
    return <div className="text-xs text-gray-500">No comparison results available.</div>
  }

  return (
    <div className="text-xs text-gray-600 overflow-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="text-gray-500">
            <th className="pb-2">AOI</th>
            <th className="pb-2">Metric</th>
            <th className="pb-2">Value</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row: any, index: number) => (
            <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
              <td className="py-1 pr-2">{row.aoi_name || row.file_name || row.name || 'AOI'}</td>
              <td className="py-1 pr-2">{row.metric || row.label || 'comparison'}</td>
              <td className="py-1">{row.value ?? row.score ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
