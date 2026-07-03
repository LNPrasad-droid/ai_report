import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function NavBar() {
  const { user, logout } = useAuth()
  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center px-2 text-lg font-bold">Agentic GeoAI</Link>
            <nav className="ml-6 flex space-x-4">
              <Link to="/map" className="px-2">Map</Link>
              <Link to="/jobs" className="px-2">Jobs</Link>
              <Link to="/reports" className="px-2">Reports</Link>
              <Link to="/chat" className="px-2">AI Chat</Link>
            </nav>
          </div>
          <div className="flex items-center">
            {user ? (
              <>
                <span className="mr-4">{user.email}</span>
                <button onClick={() => logout()} className="px-3 py-1 bg-red-500 text-white rounded">Logout</button>
              </>
            ) : (
              <Link to="/login" className="px-3 py-1 bg-blue-500 text-white rounded">Login</Link>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
