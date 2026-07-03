import React from 'react'

export default function LeftSidebar({ conversations, activeId, onSelect, onNew }: any) {
  return (
    <aside className="w-64 border-r p-4 h-screen overflow-auto">
      <div className="mb-4">
        <button onClick={() => onNew()} className="w-full py-2 bg-blue-600 text-white rounded">New Chat</button>
      </div>
      <div>
        <h3 className="text-sm font-semibold text-gray-600 mb-2">Conversations</h3>
        <ul className="space-y-2">
          {conversations.map((c: any) => (
            <li key={c.id} className={`p-2 rounded ${c.id === activeId ? 'bg-gray-100' : ''}`}>
              <button onClick={() => onSelect(c.id)} className="text-left w-full">{c.title}</button>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  )
}
