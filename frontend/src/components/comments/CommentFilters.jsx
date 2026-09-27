import styles from './Comments.module.css'
import clsx from 'clsx'

export default function CommentFilters({ currentFilter, onFilterChange }) {
  const filters = [
    { value: 'all', label: 'All Comments' },
    { value: 'positive', label: 'Positive' },
    { value: 'negative', label: 'Negative' },
    { value: 'neutral', label: 'Neutral' }
  ]

  return (
    <div className={styles.filters}>
      {filters.map(f => (
        <button
          key={f.value}
          className={clsx(
            styles.filterBtn,
            currentFilter === f.value ? 'neo-inset active' : 'neo-raised-sm'
          )}
          onClick={() => onFilterChange(f.value)}
          style={{
            color: currentFilter === f.value ? 'var(--color-primary)' : 'var(--color-on-surface-variant)'
          }}
        >
          {f.label}
        </button>
      ))}
    </div>
  )
}
