import clsx from 'clsx'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getOverviewStats } from '../../api/sentimentApi'
import DonutChart from '../../components/charts/DonutChart'
import KpiCard from '../../components/ui/KpiCard'
import LoadingSpinner from '../../components/ui/LoadingSpinner'
import { useCountUp } from '../../hooks/useCountUp'
import styles from './Dashboard.module.css'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getOverviewStats()
      .then(response => {
        if (!response?.success || !response.data) {
          console.error('Overview stats returned no data:', response)
          setError('Unable to load overview statistics.')
          return
        }
        setStats(response.data)
      })
      .catch(error => {
        console.error('Overview fetch failed:', error)
        setError('Unable to load overview statistics.')
      })
      .finally(() => setLoading(false))
  }, [])

  const animatedAnalyses = useCountUp(stats?.totalAnalyses ?? 0, 1200, 100)
  const animatedComments = useCountUp(stats?.totalComments ?? 0, 1400, 200)
  const animatedConfidence = useCountUp(Math.round((stats?.avgConfidence ?? 0) * 1000), 1200, 300)
  const displayConfidence = (Number(animatedConfidence.replaceAll(',', '')) / 10).toFixed(1)

  if (loading) return <div className={styles.center}><LoadingSpinner size="large" /></div>
  if (error) return <div className={styles.center} role="alert">{error}</div>

  const sentimentDistribution = [
    { sentiment: 'positive', count: stats.avgPositive },
    { sentiment: 'neutral', count: stats.avgNeutral },
    { sentiment: 'negative', count: stats.avgNegative }
  ]

  return (
    <div className={clsx('container', styles.dashboard)}>
      <header className={styles.header}>
        <div>
          <h2>Overview Dashboard</h2>
          <p>System-wide sentiment metrics across all analyses</p>
        </div>
        <Link to="/import" className={clsx(styles.actionBtn, 'neo-raised')}>
          <span className="material-symbols-outlined">add</span>
          New Analysis
        </Link>
      </header>

      <div className={styles.kpiGrid}>
        <KpiCard 
          title="Total Analyses" 
          value={animatedAnalyses} 
          icon="analytics" 
          highlightColor="var(--amber)"
          animationDelay={0}
        />
        <KpiCard 
          title="Comments Analyzed" 
          value={animatedComments} 
          icon="forum" 
          highlightColor="var(--indigo)"
          animationDelay={80}
        />
        <KpiCard 
          title="Avg Confidence" 
          value={`${displayConfidence}%`} 
          icon="mood" 
          highlightColor="var(--amber-dark)"
          animationDelay={160}
        />
      </div>

      <div className={styles.charts}>
        <div className={clsx(styles.chartCard, 'ga-card ga-card--panel')}>
          <h3 className="card-title">Global Sentiment Distribution</h3>
          <DonutChart data={sentimentDistribution} />
        </div>
        
        <div className={clsx(styles.quickActions, 'ga-card ga-card--panel')}>
          <h3 className="card-title">Quick Actions</h3>
          <div className={styles.actionList}>
            <Link to="/import" className={clsx(styles.quickBtn, 'quick-action-item')}>
              <span className="material-symbols-outlined">upload_file</span>
              Upload CSV
            </Link>
            <Link to="/insights" className={clsx(styles.quickBtn, 'quick-action-item')}>
              <span className="material-symbols-outlined">insights</span>
              View Insights
            </Link>
            <Link to="/comments" className={clsx(styles.quickBtn, 'quick-action-item')}>
              <span className="material-symbols-outlined">search</span>
              Explore Comments
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
