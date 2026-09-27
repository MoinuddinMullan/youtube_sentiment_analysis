import { APP_NAME } from '../../utils/constants'
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
