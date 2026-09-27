import clsx from 'clsx'
import styles from './KpiCard.module.css'

export default function KpiCard({ title, value, icon, trend, highlightColor, animationDelay = 0 }) {
  return (
    <div className={clsx(styles.card, 'ga-card ga-card--stat')} style={{ animationDelay: `${animationDelay}ms` }}>
      <div className={styles.iconWrapper} style={{ color: highlightColor }}>
        <span className="material-symbols-outlined">{icon}</span>
      </div>
      <div className={styles.content}>
        <h3 className={styles.title}>{title}</h3>
        <div className={styles.valueRow}>
          <span className={styles.value}>{value}</span>
          {trend && (
            <span className={clsx(styles.trend, trend > 0 ? styles.positive : styles.negative)}>
              <span className="material-symbols-outlined">
                {trend > 0 ? 'trending_up' : 'trending_down'}
              </span>
              {Math.abs(trend)}%
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
