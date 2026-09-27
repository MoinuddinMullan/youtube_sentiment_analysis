import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import { SENTIMENT_COLORS } from '../../utils/constants'
import styles from './Charts.module.css'

export default function DonutChart({ data }) {
  if (!data || data.length === 0) return <div className={styles.empty}>No data available</div>

  const formatData = data.map(d => ({
    name: d.sentiment.toUpperCase(),
    value: d.count
  }))

  return (
    <div className={styles.chartContainer}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={formatData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={5}
            dataKey="value"
          >
            {formatData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={SENTIMENT_COLORS[entry.name]} stroke="transparent" />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{ 
              borderRadius: 'var(--radius-sm)', 
              border: 'none', 
              boxShadow: 'var(--shadow-raised-sm)',
              background: 'var(--color-surface)'
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
