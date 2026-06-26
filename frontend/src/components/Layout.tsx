import { Outlet, NavLink } from 'react-router-dom'
export default function Layout() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      <nav style={{ width: 220, background: '#1e293b', color: '#fff', padding: '24px 16px' }}>
        <div style={{ fontSize: 20, fontWeight: 700, marginBottom: 32, color: '#38bdf8' }}>
          Foresight Engine
        </div>
        {[
          { to: '/', label: 'Dashboard' },
          { to: '/agents', label: 'Agents' },
          { to: '/predictions', label: 'Predictions' },
        ].map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            style={({ isActive }) => ({
              display: 'block',
              padding: '10px 12px',
              borderRadius: 6,
              color: isActive ? '#38bdf8' : '#94a3b8',
              background: isActive ? '#0f172a' : 'transparent',
              textDecoration: 'none',
              marginBottom: 4,
              fontWeight: isActive ? 600 : 400,
            })}
          >
            {label}
          </NavLink>
        ))}
      </nav>
      <main style={{ flex: 1, padding: 32, background: '#f1f5f9' }}>
        <Outlet />
      </main>
    </div>
  )
}
