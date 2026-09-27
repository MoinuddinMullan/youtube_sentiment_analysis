import { BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import styles from './Charts.module.css'

export default function BarChart({ data, xAxisKey, barKey, color = 'var(--color-primary)' }) {
  if (!data || data.length === 0) return <div className={styles.empty}>No data available</div>

  return (
    <div className={styles.chartContainer}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsBarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--color-surface-dim)" />
          <XAxis dataKey={xAxisKey} axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: 'var(--color-on-surface-variant)' }} />
          <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: 'var(--color-on-surface-variant)' }} />
          <Tooltip
            cursor={{ fill: 'var(--color-surface-dim)', opacity: 0.4 }}
            contentStyle={{ 
              borderRadius: 'var(--radius-sm)', 
              border: 'none', 
              boxShadow: 'var(--shadow-raised-sm)',
              background: 'var(--color-surface)'
            }}
          />
          <Bar dataKey={barKey} fill={color} radius={[4, 4, 0, 0]} />
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  )
}
