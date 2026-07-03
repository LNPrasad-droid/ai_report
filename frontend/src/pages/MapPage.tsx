import React, { useState } from 'react'
import { MapContainer, TileLayer } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { useSatelliteSearch } from '../hooks/useSatellite'
import LoadingSpinner from '../components/LoadingSpinner'

export default function MapPage() {
  const [bbox, setBbox] = useState('')
  const search = useSatelliteSearch()

  const doSearch = async (e: any) => {
    e.preventDefault()
    try {
      await search.mutateAsync({ bbox })
      // results are not stored but job will show in Jobs list
    } catch (err) {
      // handled by toast via global interceptor
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Map</h1>
      <form onSubmit={doSearch} className="mb-4 flex gap-2">
        <input value={bbox} onChange={(e) => setBbox(e.target.value)} placeholder="bbox (minX,minY,maxX,maxY)" className="p-2 border rounded w-full" />
        <button className="px-4 py-2 bg-blue-600 text-white rounded">Search</button>
      </form>
      <div className="h-[600px] bg-white rounded shadow">
        <MapContainer center={[20, 78]} zoom={5} style={{ height: '100%', width: '100%' }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        </MapContainer>
      </div>
      {search.isLoading && <LoadingSpinner />}
    </div>
  )
}
