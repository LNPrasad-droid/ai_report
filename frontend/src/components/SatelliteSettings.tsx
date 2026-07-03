import React from 'react'

export default function SatelliteSettings({ options, onChange }: any) {
  const setField = (k: string, v: any) => onChange && onChange({ ...options, [k]: v })

  return (
    <div className="p-2 bg-white rounded shadow">
      <div className="text-sm font-medium mb-2">Satellite Options</div>
      <div className="space-y-2">
        <select value={options.satellite} onChange={(e) => setField('satellite', e.target.value)} className="w-full p-2 border rounded">
          <option value="Sentinel-2">Sentinel-2</option>
          <option value="Landsat-8">Landsat 8</option>
          <option value="Landsat-9">Landsat 9</option>
        </select>
        <div className="flex gap-2">
          <input type="date" value={options.start} onChange={(e) => setField('start', e.target.value)} className="p-2 border rounded w-1/2" />
          <input type="date" value={options.end} onChange={(e) => setField('end', e.target.value)} className="p-2 border rounded w-1/2" />
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm">Max Cloud %</label>
          <input type="number" value={options.cloud ?? 10} onChange={(e) => setField('cloud', Number(e.target.value))} className="p-2 border rounded w-20" />
        </div>
      </div>
    </div>
  )
}
