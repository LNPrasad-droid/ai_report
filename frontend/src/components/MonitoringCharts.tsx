import React from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'

export default function MonitoringCharts({ data }: { data: any }) {
  // data expected: { timeseries: [{date, exec_time}], agent_runtimes: [{agent, ms}], success_rate: {success, failure}, daily_counts: [{date, count}] }
  const timeseries = data?.timeseries || []
  const agentRuntimes = data?.agent_runtimes || []
  const successRate = data?.success_rate || { success: 0, failure: 0 }
  const daily = data?.daily_counts || []

  const pieData = [
    { name: 'success', value: successRate.success || 0 },
    { name: 'failure', value: successRate.failure || 0 },
  ]
  const COLORS = ['#10B981', '#EF4444']

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="p-4 bg-white rounded shadow h-64">
        <h3 className="font-semibold mb-2">Execution Time Trend</h3>
        {timeseries.length === 0 ? (
          <div className="text-sm text-gray-500">No data</div>
        ) : (
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={timeseries}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="exec_time" stroke="#2563EB" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="p-4 bg-white rounded shadow h-64">
        <h3 className="font-semibold mb-2">Agent Runtime</h3>
        {agentRuntimes.length === 0 ? (
          <div className="text-sm text-gray-500">No data</div>
        ) : (
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={agentRuntimes}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="agent" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="ms" fill="#6366F1" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="p-4 bg-white rounded shadow h-64">
        <h3 className="font-semibold mb-2">Success vs Failure</h3>
        <ResponsiveContainer width="100%" height={180}>
          <PieChart>
            <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60}>
              {pieData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="p-4 bg-white rounded shadow h-64">
        <h3 className="font-semibold mb-2">Daily Job Count</h3>
        {daily.length === 0 ? (
          <div className="text-sm text-gray-500">No data</div>
        ) : (
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={daily}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#F59E0B" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}
