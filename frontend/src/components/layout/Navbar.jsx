import { NavLink } from 'react-router-dom'
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
