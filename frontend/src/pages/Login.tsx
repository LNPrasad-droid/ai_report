import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function LoginPage() {
  const { loginWithEmail, loginWithGoogle } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleEmailLogin = async (e: any) => {
    e.preventDefault()
    try {
      await loginWithEmail(email, password)
      navigate('/')
    } catch (err) {
      alert('Login failed')
    }
  }

  const handleGoogle = async () => {
    try {
      await loginWithGoogle()
      navigate('/')
    } catch (err) {
      alert('Login failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-20 p-6 bg-white rounded shadow">
      <h2 className="text-2xl mb-4">Sign in</h2>
      <form onSubmit={handleEmailLogin}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="w-full p-2 border mb-2" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="w-full p-2 border mb-4" />
        <button className="w-full p-2 bg-blue-600 text-white rounded">Sign in</button>
      </form>
      <div className="mt-4">
        <button onClick={handleGoogle} className="w-full p-2 bg-red-500 text-white rounded">Sign in with Google</button>
      </div>
    </div>
  )
}
