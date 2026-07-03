import React from 'react'
import { MapContainer, TileLayer, Polygon, Marker } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

const palette = ['#2563EB', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#14B8A6']

function buildPolygon(geo: any) {
  if (!geo) return null
  if (geo.type === 'Polygon') {
    return geo.coordinates[0].map((coord: any) => [coord[1], coord[0]])
  }
  return null
}

function bboxToPolygon(bbox: number[]) {
  if (!bbox || bbox.length !== 4) return null
  return [[bbox[1], bbox[0]], [bbox[1], bbox[2]], [bbox[3], bbox[2]], [bbox[3], bbox[0]]]
}

export default function MapPreview({ items = [], selectedId }: any) {
  const selected = items.find((item: any) => item.id === selectedId)
  const center = selected?.meta?.centroid
    ? [selected.meta.centroid[1], selected.meta.centroid[0]]
    : items[0]?.meta?.centroid
    ? [items[0].meta.centroid[1], items[0].meta.centroid[0]]
    : [20, 78]

  return (
    <div className="h-64 w-full rounded overflow-hidden">
      <MapContainer center={center as any} zoom={6} style={{ height: '100%', width: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {items.map((item: any, index: number) => {
          const color = palette[index % palette.length]
          const geometry = buildPolygon(item.meta?.geometry)
          const bounds = bboxToPolygon(item.meta?.bbox)
          const positions = geometry || bounds
          return positions ? (
            <Polygon
              key={item.id}
              positions={positions}
              pathOptions={{ color, weight: item.id === selectedId ? 4 : 2, fillOpacity: item.id === selectedId ? 0.2 : 0.1 }}
            />
          ) : null
        })}
        {items.map((item: any, index: number) => {
          const centroid = item.meta?.centroid
          const color = palette[index % palette.length]
          return centroid ? <Marker key={`${item.id}-marker`} position={[centroid[1], centroid[0]] as any}></Marker> : null
        })}
      </MapContainer>
    </div>
  )
}
