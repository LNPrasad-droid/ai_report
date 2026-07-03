import { useState, useEffect } from 'react'

const STORAGE_KEY = 'ag_workspace_conversations_v1'

export function loadConversations() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    return JSON.parse(raw)
  } catch (e) {
    return []
  }
}

export function saveConversations(convs: any[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(convs))
}

export const useConversation = (initialId?: string) => {
  const [conversations, setConversations] = useState<any[]>(() => loadConversations())
  const [activeId, setActiveId] = useState<string | undefined>(initialId || conversations[0]?.id)

  useEffect(() => saveConversations(conversations), [conversations])

  const createConversation = (title?: string) => {
    const id = `c_${Date.now()}`
    const conv = { id, title: title || 'New Conversation', messages: [], pinned: false, created_at: new Date().toISOString() }
    setConversations((s) => [conv, ...s])
    setActiveId(id)
    return conv
  }

  const addMessage = (convId: string, msg: any) => {
    setConversations((s) => s.map((c: any) => (c.id === convId ? { ...c, messages: [...(c.messages || []), msg] } : c)))
  }

  const updateMessage = (convId: string, msgId: string, patch: any) => {
    setConversations((s) => s.map((c: any) => (c.id === convId ? { ...c, messages: (c.messages || []).map((m: any) => (m.id === msgId ? { ...m, ...patch } : m)) } : c)))
  }

  const activeConversation = conversations.find((c) => c.id === activeId)

  return { conversations, activeConversation, createConversation, addMessage, updateMessage, setActiveId, setConversations }
}
