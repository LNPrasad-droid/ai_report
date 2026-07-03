import React from 'react'

type Props = { children: React.ReactNode }

export default class ErrorBoundary extends React.Component<Props, { hasError: boolean }> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }
  static getDerivedStateFromError() {
    return { hasError: true }
  }
  componentDidCatch(error: any, info: any) {
    console.error('ErrorBoundary caught', error, info)
  }
  render() {
    if (this.state.hasError) {
      return <div className="p-4 bg-red-50 rounded">Something went wrong.</div>
    }
    return this.props.children
  }
}
