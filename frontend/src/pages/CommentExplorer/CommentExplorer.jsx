import clsx from 'clsx'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getHistory } from '../../api/sentimentApi'
import LoadingSpinner from '../../components/ui/LoadingSpinner'
import SentimentBadge from '../../components/ui/SentimentBadge'
import { formatDate, formatNumber } from '../../utils/formatters'
import styles from './CommentExplorer.module.css'

export default function CommentExplorer() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getHistory()
      .then(response => {
        if (!response?.success || !Array.isArray(response.data)) {
          console.error('History returned no data:', response)
          setError('Unable to load analysis history.')
          return
        }
        setHistory(response.data)
      })
      .catch(error => {
        console.error('History fetch failed:', error)
        setError('Unable to load analysis history.')
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className={styles.center}><LoadingSpinner size="large" /></div>
  if (error) return <div className={styles.center} role="alert">{error}</div>

  return (
    <div className={clsx('container', styles.explorer)}>
      <div className={styles.header}>
        <h2>Analysis History</h2>
        <p>Explore past batch sentiment analyses</p>
      </div>

      {history.length === 0 ? (
        <div className={clsx(styles.empty, 'ga-card ga-card--panel')}>
          <span className="material-symbols-outlined">history_toggle_off</span>
          <h3>No analyses found</h3>
          <p>Upload a CSV file to get started.</p>
          <Link to="/import" className={styles.linkBtn}>Go to Importer</Link>
        </div>
      ) : (
        <div className={styles.grid}>
          {history.map((item, index) => (
            <Link 
              to={`/analyze?id=${item.analysisId}`} 
              key={item.analysisId}
              className={clsx(styles.historyCard, 'ga-card', `ga-card--${item.sourceType === 'csv' ? 'csv' : 'single'}`)}
              style={{ animationDelay: `${index * 80}ms` }}
            >
              <div className={styles.cardHeader}>
                <span className={styles.date}>{formatDate(item.createdAt)}</span>
                <span className={item.sourceType === 'csv' ? 'badge-csv' : 'badge-single'}>
                  {item.sourceType === 'csv' ? 'CSV' : 'SINGLE'}
                </span>
              </div>
              
              <h3 className={styles.filename}>
                {item.fileName || (item.sourceType === 'single' ? 'Single comment prediction' : 'Analysis')}
              </h3>
              
              <div className={styles.stats}>
                <div className={styles.stat}>
                  <span>Total</span>
                  <strong>{formatNumber(item.totalComments)}</strong>
                </div>
                <div className={styles.badges}>
                  {['positive', 'neutral', 'negative']
                    .filter(sentiment => item[`${sentiment}Count`] > 0)
                    .map(sentiment => (
                      <SentimentBadge key={sentiment} sentiment={sentiment} />
                    ))}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
