import React, { useRef } from 'react'

const statusClasses: Record<string, string> = {
  pending: 'text-gray-500 bg-gray-100',
  uploading: 'text-orange-700 bg-orange-100',
  uploaded: 'text-green-700 bg-green-100',
  failed: 'text-red-700 bg-red-100',
}

export default function AOIUploader({ files = [], selectedId, onFilesSelected, onRemove, onRename, onSelect }: any) {
  const inputRef = useRef<HTMLInputElement | null>(null)

  const handleFiles = (filesList: FileList | null) => {
    if (!filesList) return
    const filesArray = Array.from(filesList)
    onFilesSelected && onFilesSelected(filesArray)
  }

  const onDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    handleFiles(event.dataTransfer.files)
  }

  return (
    <div className="p-2 bg-white rounded shadow">
      <div className="text-sm font-medium mb-2">Attach AOIs</div>
      <div onDrop={onDrop} onDragOver={(e) => e.preventDefault()} className="border-dashed border-2 border-gray-300 p-4 text-center mb-3 cursor-pointer">
        <div>Drag & drop files here</div>
        <button onClick={() => inputRef.current?.click()} className="mt-2 px-3 py-1 bg-blue-600 text-white rounded">Browse files</button>
        <input ref={inputRef} type="file" className="hidden" multiple onChange={(e) => handleFiles(e.target.files)} accept=".kml,.kmz,.geojson,.zip" />
      </div>
      {files.length > 0 && (
        <div>
          <div className="text-sm font-semibold mb-2">Upload queue</div>
          <ul className="space-y-2">
            {files.map((item: any) => (
              <li key={item.id} className={`p-2 rounded border ${item.id === selectedId ? 'border-blue-500 bg-blue-50' : 'border-gray-200 bg-gray-50'}`}>
                <div className="flex justify-between items-center gap-2">
                  <button onClick={() => onSelect && onSelect(item.id)} className="text-left flex-1">
                    <div className="font-medium text-sm">{item.name}</div>
                    <div className="text-xs text-gray-500">{item.meta?.geometry_type || item.type || 'file'}</div>
                  </button>
                  <span className={`px-2 py-1 rounded text-xs ${statusClasses[item.status || 'pending'] || 'text-gray-500 bg-gray-100'}`}>{item.status || 'pending'}</span>
                </div>
                <div className="flex justify-between items-center mt-2 text-xs text-gray-600">
                  <span>Area: {item.meta?.area || 'unknown'}</span>
                  <div className="flex gap-2">
                    <button onClick={() => onRename && onRename(item.id)} className="px-2 py-1 bg-gray-100 rounded">Rename</button>
                    <button onClick={() => onRemove && onRemove(item.id)} className="px-2 py-1 bg-red-100 text-red-700 rounded">Remove</button>
                  </div>
                </div>
                {item.progress != null && (
                  <div className="mt-2">
                    <div className="text-[10px] text-gray-500">Upload: {item.progress}%</div>
                    <div className="w-full bg-gray-200 h-2 rounded mt-1"><div style={{ width: `${item.progress}%` }} className="h-2 bg-blue-600 rounded" /></div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="mt-3 text-xs text-gray-500">Supported: .kml .kmz .geojson .zip (ESRI Shapefile)</div>
    </div>
  )
}
