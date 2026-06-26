import { useQuery } from '@tanstack/react-query'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { api } from '../api/client'
export default function Dashboard() {
  const { data: summary } = useQuery({
    queryKey: ['metrics-summary'],
    queryFn: () => api.get('/api/v1/metrics/summary').then(r => r.data),
  })
  const { data: metrics = [] } = useQuery({
    queryKey: ['metrics'],
    queryFn: () => api.get('/api/v1/metrics/?limit=50').then(r => r.data),
    refetchInterval: 15_000,
  })
  return (
    <div>
      <h1 style={{ fontSize: 28, fontWeight: 700, color: '#0f172a', marginBottom: 24 }}>Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 32 }}>
        {[
          { label: 'Total Metrics', value: summary?.total ?? '—' },
          { label: 'Active Agents', value: summary?.agents ?? '—' },
          { label: 'Metric Types', value: summary?.metric_types?.length ?? '—' },
        ].map(({ label, value }) => (
          <div key={label} style={{ background: '#fff', borderRadius: 12, padding: 24, boxShadow: '0 1px 4px rgba(0,0,0,.06)' }}>
            <div style={{ fontSize: 13, color: '#64748b', marginBottom: 8 }}>{label}</div>
            <div style={{ fontSize: 32, fontWeight: 700, color: '#0f172a' }}>{value}</div>
          </div>
        ))}
      </div>
      <div style={{ background: '#fff', borderRadius: 12, padding: 24, boxShadow: '0 1px 4px rgba(0,0,0,.06)' }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16, color: '#0f172a' }}>Recent Metrics</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={metrics}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="timestamp" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#38bdf8" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
