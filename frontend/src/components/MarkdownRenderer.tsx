import React from 'react'
import ReactMarkdown from 'react-markdown'

export default function MarkdownRenderer({ content }: { content?: string }) {
  if (!content) return null
  return (
    <div className="prose max-w-none">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  )
}
