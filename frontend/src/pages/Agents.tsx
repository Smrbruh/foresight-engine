import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
export default function Agents() {
  const { data: agents = [], isLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: () => api.get('/api/v1/agents/').then(r => r.data),
  })
  const statusColor = (s: string) => ({ active: '#22c55e', inactive: '#94a3b8', error: '#ef4444' }[s] || '#94a3b8')
  if (isLoading) return <div>Loading...</div>
  return (
    <div>
      <h1 style={{ fontSize: 28, fontWeight: 700, color: '#0f172a', marginBottom: 24 }}>Agents</h1>
      <div style={{ background: '#fff', borderRadius: 12, boxShadow: '0 1px 4px rgba(0,0,0,.06)', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f8fafc' }}>
              {['ID', 'Name', 'Status', 'Last Seen', 'Created'].map(h => (
                <th key={h} style={{ padding: '12px 16px', textAlign: 'left', fontSize: 12, fontWeight: 600, color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {agents.length === 0 ? (
              <tr><td colSpan={5} style={{ padding: 32, textAlign: 'center', color: '#94a3b8' }}>No agents registered</td></tr>
            ) : agents.map((a: any) => (
              <tr key={a.id} style={{ borderTop: '1px solid #f1f5f9' }}>
                <td style={{ padding: '12px 16px', fontSize: 13, color: '#64748b' }}>#{a.id}</td>
                <td style={{ padding: '12px 16px', fontWeight: 600, color: '#0f172a' }}>{a.name}</td>
                <td style={{ padding: '12px 16px' }}>
                  <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 12, fontWeight: 600, color: statusColor(a.status) }}>
                    <span style={{ width: 8, height: 8, borderRadius: '50%', background: statusColor(a.status) }} />
                    {a.status}
                  </span>
                </td>
                <td style={{ padding: '12px 16px', fontSize: 13, color: '#64748b' }}>{a.last_seen ? new Date(a.last_seen).toLocaleString() : '—'}</td>
                <td style={{ padding: '12px 16px', fontSize: 13, color: '#64748b' }}>{new Date(a.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
