import styles from './ProgressBar.module.css'

export default function ProgressBar({ label, value, color }) {
  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <span className={styles.label}>{label}</span>
        <span className={styles.value}>{value}%</span>
      </div>
      <div className={`${styles.track} neo-inset`}>
        <div 
          className={styles.fill} 
          style={{ width: `${value}%`, backgroundColor: color }}
        />
      </div>
    </div>
  )
}
