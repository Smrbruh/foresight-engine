import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
const statusColor = (s: string) => ({
  pending: '#f59e0b',
  running: '#3b82f6',
  completed: '#22c55e',
  failed: '#ef4444',
}[s] || '#94a3b8')
export default function Predictions() {
  const { data: predictions = [], isLoading } = useQuery({
    queryKey: ['predictions'],
    queryFn: () => api.get('/api/v1/predictions/').then(r => r.data),
    refetchInterval: 10_000,
  })
  if (isLoading) return <div>Loading...</div>
  return (
    <div>
      <h1 style={{ fontSize: 28, fontWeight: 700, color: '#0f172a', marginBottom: 24 }}>Predictions</h1>
      <div style={{ display: 'grid', gap: 12 }}>
        {predictions.length === 0 ? (
          <div style={{ background: '#fff', borderRadius: 12, padding: 32, textAlign: 'center', color: '#94a3b8', boxShadow: '0 1px 4px rgba(0,0,0,.06)' }}>
            No predictions yet
          </div>
        ) : predictions.map((p: any) => (
          <div key={p.id} style={{ background: '#fff', borderRadius: 12, padding: 20, boxShadow: '0 1px 4px rgba(0,0,0,.06)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontWeight: 600, color: '#0f172a', marginBottom: 4 }}>{p.model_type} — Agent #{p.agent_id}</div>
              <div style={{ fontSize: 13, color: '#64748b' }}>Horizon: {p.horizon_hours}h · Created {new Date(p.created_at).toLocaleString()}</div>
            </div>
            <span style={{ padding: '4px 12px', borderRadius: 20, fontSize: 12, fontWeight: 600, background: `${statusColor(p.status)}20`, color: statusColor(p.status) }}>
              {p.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
