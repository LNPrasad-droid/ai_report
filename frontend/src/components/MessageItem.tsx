import React from 'react'
import MarkdownRenderer from './MarkdownRenderer'
import StatusBadge from './StatusBadge'

export default function MessageItem({ message }: { message: any }) {
  const t = message.type || 'assistant'
  const classMap: Record<string, string> = {
    user: 'bg-blue-50 self-end',
    assistant: 'bg-white self-start',
    system: 'bg-gray-50 self-start',
    agent_progress: 'bg-yellow-50 self-start',
    execution_log: 'bg-gray-100 self-start',
  }
  return (
    <div className={`p-3 rounded max-w-3xl ${classMap[t] || 'bg-white'}`}>
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600">{message.role || t}</div>
        {message.meta?.status && <StatusBadge status={message.meta.status} />}
      </div>
      <div className="mt-2 text-sm">
        {message.content && <MarkdownRenderer content={message.content} />}
        {message.meta?.summary && <div className="mt-2 text-xs text-gray-700">{message.meta.summary}</div>}
      </div>
      {message.meta?.error && <pre className="mt-2 text-xs text-red-700">{JSON.stringify(message.meta.error, null, 2)}</pre>}
    </div>
  )
}
