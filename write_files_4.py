import os

files = {
    r"frontend\src\components\charts\DonutChart.jsx": r"""import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
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
""",
    r"frontend\src\components\charts\BarChart.jsx": r"""import { BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
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
""",
    r"frontend\src\components\charts\WaveformChart.jsx": r"""// Placeholder if we wanted a waveform chart, omitted actual implementation for now.
export default function WaveformChart() { return null }
""",
    r"frontend\src\components\charts\Charts.module.css": r""".chartContainer {
  width: 100%;
  height: 250px;
}

.empty {
  width: 100%;
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-on-surface-variant);
  font-size: 0.875rem;
}
""",
    r"frontend\src\components\upload\FileUpload.jsx": r"""import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import clsx from 'clsx'
import styles from './FileUpload.module.css'

export default function FileUpload({ onUpload, loading }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0 && !loading) {
      onUpload(acceptedFiles[0])
    }
  }, [onUpload, loading])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv']
    },
    maxFiles: 1,
    disabled: loading
  })

  return (
    <div 
      {...getRootProps()} 
      className={clsx(
        styles.dropzone, 
        'neo-inset',
        isDragActive && styles.active,
        loading && styles.disabled
      )}
    >
      <input {...getInputProps()} />
      <div className={styles.content}>
        <span className={clsx("material-symbols-outlined", styles.icon)}>
          {loading ? 'cloud_sync' : 'cloud_upload'}
        </span>
        <h3>{loading ? 'Processing...' : 'Drag & Drop your CSV file here'}</h3>
        <p>Supports files up to 25MB with columns: comment_text</p>
        <button type="button" className={clsx(styles.btn, 'neo-raised-sm')} disabled={loading}>
          Browse Files
        </button>
      </div>
    </div>
  )
}
""",
    r"frontend\src\components\upload\FileUpload.module.css": r""".dropzone {
  padding: 4rem 2rem;
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  cursor: pointer;
  transition: var(--transition-base);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.dropzone:hover:not(.disabled) {
  background: var(--color-surface-lowest);
}

.active {
  background: var(--color-surface-lowest);
  box-shadow: var(--shadow-inset), 0 0 0 2px var(--color-primary) inset;
}

.disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.icon {
  font-size: 48px;
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.disabled .icon {
  animation: pulse 1.5s infinite;
}

h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-on-surface);
}

p {
  font-size: 0.875rem;
  color: var(--color-on-surface-variant);
  max-width: 300px;
}

.btn {
  margin-top: 1rem;
  padding: 0.75rem 2rem;
  border-radius: var(--radius-full);
  background: var(--color-surface);
  color: var(--color-primary);
  font-weight: 600;
  font-size: 0.875rem;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
"""
}

base_dir = r"d:\moin\youtube_sentiment_analysis"

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 4 files written.")
