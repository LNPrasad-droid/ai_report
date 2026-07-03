import React, { createContext, useContext, useState } from 'react'

const ToastContext = createContext<any>(null)

export const ToastProvider = ({ children }: any) => {
  const [toasts, setToasts] = useState<string[]>([])
  const push = (msg: string) => {
    setToasts((s) => [...s, msg])
    setTimeout(() => {
      setToasts((s) => s.slice(1))
    }, 4000)
  }
  return (
    <ToastContext.Provider value={{ push }}>
      {children}
      <div className="fixed bottom-4 right-4 space-y-2">
        {toasts.map((t, i) => (
          <div key={i} className="bg-gray-800 text-white px-4 py-2 rounded shadow">{t}</div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export const useToast = () => useContext(ToastContext)
export default ToastContext
