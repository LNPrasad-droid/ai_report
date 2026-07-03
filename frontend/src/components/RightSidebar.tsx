import React from 'react'
import AOIUploader from './AOIUploader'
import SatelliteSettings from './SatelliteSettings'
import MapPreview from './MapPreview'
import ComparisonTable from './ComparisonTable'

const statusColors: Record<string, string> = {
  uploaded: 'bg-green-100 text-green-800',
  uploading: 'bg-yellow-100 text-yellow-800',
  failed: 'bg-red-100 text-red-800',
  pending: 'bg-gray-100 text-gray-800',
}

export default function RightSidebar({ job, execution, aoiFiles, selectedAoiId, onFilesSelected, onRemoveAoi, onRenameAoi, onSelectAoi, satOptions, onSatOptionsChange }: any) {
  const selected = aoiFiles.find((item: any) => item.id === selectedAoiId) || aoiFiles[0]
  const completed = aoiFiles.filter((item: any) => item.status === 'uploaded').length
  const failed = aoiFiles.filter((item: any) => item.status === 'failed').length
  const pending = aoiFiles.filter((item: any) => item.status === 'pending' || item.status === 'uploading').length

  return (
    <aside className="w-80 border-l p-4 h-screen overflow-auto space-y-4">
      <AOIUploader files={aoiFiles} selectedId={selectedAoiId} onFilesSelected={onFilesSelected} onRemove={onRemoveAoi} onRename={onRenameAoi} onSelect={onSelectAoi} />

      <div className="p-2 bg-white rounded shadow">
        <h3 className="text-sm font-semibold mb-2">AOI Summary</h3>
        <div className="grid grid-cols-4 gap-2 text-center text-xs">
          <div className="p-2 bg-gray-50 rounded">
            <div className="font-semibold">Total</div>
            <div>{aoiFiles.length}</div>
          </div>
          <div className="p-2 bg-gray-50 rounded">
            <div className="font-semibold">Uploaded</div>
            <div>{completed}</div>
          </div>
          <div className="p-2 bg-gray-50 rounded">
            <div className="font-semibold">Pending</div>
            <div>{pending}</div>
          </div>
          <div className="p-2 bg-gray-50 rounded">
            <div className="font-semibold">Failed</div>
            <div>{failed}</div>
          </div>
        </div>
      </div>

      <SatelliteSettings options={satOptions} onChange={onSatOptionsChange} />

      <div className="p-2 bg-white rounded shadow">
        <h3 className="text-sm font-semibold mb-2">Selected AOI</h3>
        {selected ? (
          <div>
            <div className="text-sm font-medium">{selected.name}</div>
            <div className="text-xs text-gray-500">{selected.meta?.geometry_type || 'unknown'}</div>
            <div className="text-xs text-gray-500">Area: {selected.meta?.area || 'unknown'}</div>
            <div className="text-xs text-gray-500">Status: <span className={`${statusColors[selected.status || 'pending']} px-2 py-1 rounded`}>{selected.status || 'pending'}</span></div>
            <div className="mt-2"><MapPreview items={aoiFiles} selectedId={selectedAoiId} /></div>
          </div>
        ) : (
          <div className="text-sm text-gray-500">No AOI selected</div>
        )}
      </div>

      <div className="p-2 bg-white rounded shadow">
        <h3 className="text-sm font-semibold mb-2">Current Job</h3>
        {job ? (
          <div className="space-y-2 text-xs text-gray-600">
            <div>ID: <span className="font-mono">{job.id}</span></div>
            <div>Status: {job.status}</div>
            <div>Duration: {job.duration || '—'}</div>
          </div>
        ) : (
          <div className="text-sm text-gray-500">No active job</div>
        )}
      </div>

      <div className="p-2 bg-white rounded shadow">
        <h3 className="text-sm font-semibold mb-2">Execution Timeline</h3>
        {execution?.steps ? (
          <ul className="space-y-2 text-xs text-gray-600">
            {execution.steps.map((s: any, i: number) => (
              <li key={i} className="p-2 bg-gray-50 rounded">
                <div className="flex justify-between"><div>{s.name}</div><div>{s.status}</div></div>
                <div>{s.start_time} → {s.end_time}</div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-sm text-gray-500">No execution data</div>
        )}
      </div>

      <div className="p-2 bg-white rounded shadow">
        <h3 className="text-sm font-semibold mb-2">Comparison</h3>
        <ComparisonTable data={job?.comparison || job?.results?.comparison || []} />
      </div>
    </aside>
  )
}
