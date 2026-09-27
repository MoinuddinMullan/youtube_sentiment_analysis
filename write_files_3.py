import os

files = {
    r"frontend\src\components\ui\ProgressBar.jsx": r"""import styles from './ProgressBar.module.css'

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
""",
    r"frontend\src\components\ui\ProgressBar.module.css": r""".wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-on-surface-variant);
}

.track {
  height: 8px;
  background: var(--color-surface);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}
""",
    r"frontend\src\components\ui\KpiCard.jsx": r"""import styles from './KpiCard.module.css'
import clsx from 'clsx'

export default function KpiCard({ title, value, icon, trend, highlightColor }) {
  return (
    <div className={clsx(styles.card, 'neo-raised')}>
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
""",
    r"frontend\src\components\ui\KpiCard.module.css": r""".card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  transition: var(--transition-base);
}

.card:hover {
  transform: translateY(-2px);
}

.iconWrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: var(--color-surface);
  box-shadow: var(--shadow-raised-sm);
}

.iconWrapper span {
  font-size: 24px;
}

.content {
  flex: 1;
}

.title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-on-surface-variant);
  margin-bottom: 0.5rem;
}

.valueRow {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}

.value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-on-surface);
}

.trend {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-full);
}

.trend span {
  font-size: 14px;
}

.positive {
  color: var(--color-primary);
  background: var(--color-primary-dim);
}

.negative {
  color: var(--color-error);
  background: var(--color-error-container);
}
""",
    r"frontend\src\components\ui\Toast.jsx": r"""// This is a placeholder if a custom wrapper was needed, 
// but we're using react-hot-toast directly in main.jsx
export default function Toast() { return null }
""",
    r"frontend\src\components\layout\Navbar.jsx": r"""import { NavLink } from 'react-router-dom'
import { APP_NAME } from '../../utils/constants'
import styles from './Navbar.module.css'
import clsx from 'clsx'

export default function Navbar() {
  const links = [
    { path: '/dashboard', label: 'Dashboard', icon: 'space_dashboard' },
    { path: '/import', label: 'Import CSV', icon: 'upload_file' },
    { path: '/comments', label: 'Explore Comments', icon: 'forum' }
  ]

  return (
    <nav className={clsx(styles.navbar, 'neo-raised')}>
      <div className={clsx(styles.container, 'container')}>
        <div className={styles.brand}>
          <div className={clsx(styles.logo, 'neo-raised-sm')}>
            <span className="material-symbols-outlined">analytics</span>
          </div>
          <h1>{APP_NAME}</h1>
        </div>
        
        <div className={styles.links}>
          {links.map(link => (
            <NavLink 
              key={link.path} 
              to={link.path}
              className={({ isActive }) => 
                clsx(styles.link, isActive && styles.active, isActive ? 'neo-inset' : 'neo-raised-sm')
              }
            >
              <span className="material-symbols-outlined">{link.icon}</span>
              {link.label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  )
}
""",
    r"frontend\src\components\layout\Navbar.module.css": r""".navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  background: var(--color-surface);
  z-index: 100;
  display: flex;
  align-items: center;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
}

.brand h1 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-on-surface);
  letter-spacing: -0.02em;
}

.links {
  display: flex;
  gap: 1rem;
}

.link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-on-surface-variant);
  transition: var(--transition-base);
  background: var(--color-surface);
}

.link:hover:not(.active) {
  color: var(--color-primary);
}

.active {
  color: var(--color-primary);
}

.link span {
  font-size: 18px;
}
""",
    r"frontend\src\components\layout\Footer.jsx": r"""import { APP_NAME } from '../../utils/constants'
import styles from './Footer.module.css'

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className="container">
        <p>&copy; {new Date().getFullYear()} {APP_NAME}. All rights reserved.</p>
      </div>
    </footer>
  )
}
""",
    r"frontend\src\components\layout\Footer.module.css": r""".footer {
  padding: 2rem 0;
  text-align: center;
  color: var(--color-on-surface-variant);
  font-size: 0.875rem;
  margin-top: auto;
}
"""
}

base_dir = r"d:\moin\youtube_sentiment_analysis"

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 3 files written.")
