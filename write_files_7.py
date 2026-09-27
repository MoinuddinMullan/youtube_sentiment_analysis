import os

files = {
    r"frontend\src\pages\CommentExplorer\CommentExplorer.jsx": r"""import { useState, useEffect } from 'react'
import { getHistory } from '../../api/sentimentApi'
import { Link } from 'react-router-dom'
import { formatDate, formatNumber } from '../../utils/formatters'
import SentimentBadge from '../../components/ui/SentimentBadge'
import LoadingSpinner from '../../components/ui/LoadingSpinner'
import styles from './CommentExplorer.module.css'
import clsx from 'clsx'

export default function CommentExplorer() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getHistory()
      .then(data => setHistory(data.items || []))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className={styles.center}><LoadingSpinner size="large" /></div>

  return (
    <div className={clsx('container', styles.explorer)}>
      <div className={styles.header}>
        <h2>Analysis History</h2>
        <p>Explore past batch sentiment analyses</p>
      </div>

      {history.length === 0 ? (
        <div className={clsx(styles.empty, 'neo-raised')}>
          <span className="material-symbols-outlined">history_toggle_off</span>
          <h3>No analyses found</h3>
          <p>Upload a CSV file to get started.</p>
          <Link to="/import" className={styles.linkBtn}>Go to Importer</Link>
        </div>
      ) : (
        <div className={styles.grid}>
          {history.map(item => (
            <Link 
              to={`/analyze?id=${item.analysis_id}`} 
              key={item.analysis_id}
              className={clsx(styles.historyCard, 'neo-raised')}
            >
              <div className={styles.cardHeader}>
                <span className={styles.date}>{formatDate(item.created_at)}</span>
                <span className={clsx(styles.status, styles[item.status])}>
                  {item.status}
                </span>
              </div>
              
              <h3 className={styles.filename}>{item.filename}</h3>
              
              <div className={styles.stats}>
                <div className={styles.stat}>
                  <span>Total</span>
                  <strong>{formatNumber(item.total_comments)}</strong>
                </div>
                {item.sentiment_counts && (
                  <div className={styles.badges}>
                    {Object.entries(item.sentiment_counts).map(([sent, count]) => (
                      <SentimentBadge key={sent} sentiment={sent} />
                    ))}
                  </div>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
""",
    r"frontend\src\pages\CommentExplorer\CommentExplorer.module.css": r""".explorer {
  padding: 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.header p {
  color: var(--color-on-surface-variant);
  font-size: 0.875rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.historyCard {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: transform 0.2s;
}

.historyCard:hover {
  transform: translateY(-4px);
}

.cardHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  font-weight: 600;
}

.date {
  color: var(--color-on-surface-variant);
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
}
.completed { background: var(--color-primary-dim); color: var(--color-primary); }
.processing { background: #fef3c7; color: #d97706; }
.failed { background: var(--color-error-container); color: var(--color-error); }

.filename {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-on-surface);
  word-break: break-all;
}

.stats {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid var(--color-surface-dim);
}

.stat {
  display: flex;
  flex-direction: column;
  font-size: 0.75rem;
  color: var(--color-on-surface-variant);
}

.stat strong {
  font-size: 1.25rem;
  color: var(--color-on-surface);
}

.badges {
  display: flex;
  gap: 0.5rem;
}

.empty {
  padding: 4rem 2rem;
  text-align: center;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty span {
  font-size: 48px;
  color: var(--color-outline);
}

.linkBtn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: white;
  font-weight: 600;
}

.center {
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
""",
    r"frontend\src\pages\Insights\Insights.jsx": r"""import { useState, useEffect } from 'react'
import { getOverviewStats } from '../../api/sentimentApi'
import BarChart from '../../components/charts/BarChart'
import LoadingSpinner from '../../components/ui/LoadingSpinner'
import styles from './Insights.module.css'
import clsx from 'clsx'

export default function Insights() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getOverviewStats()
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className={styles.center}><LoadingSpinner size="large" /></div>

  const trendData = stats?.recentTrend || []

  return (
    <div className={clsx('container', styles.insights)}>
      <div className={styles.header}>
        <h2>Sentiment Insights</h2>
        <p>Deep dive into your data trends</p>
      </div>

      <div className={clsx(styles.chartSection, 'neo-raised')}>
        <div className={styles.chartHeader}>
          <h3>Analyses Over Time</h3>
          <span className={styles.subtitle}>Number of analyses performed in recent days</span>
        </div>
        <div className={styles.chartWrapper}>
          <BarChart data={trendData} xAxisKey="date" barKey="count" />
        </div>
      </div>
    </div>
  )
}
""",
    r"frontend\src\pages\Insights\Insights.module.css": r""".insights {
  padding: 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.header p {
  color: var(--color-on-surface-variant);
  font-size: 0.875rem;
}

.chartSection {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chartHeader h3 {
  font-size: 1.125rem;
  font-weight: 600;
}

.subtitle {
  font-size: 0.875rem;
  color: var(--color-on-surface-variant);
}

.chartWrapper {
  height: 350px;
}

.center {
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
""",
    r"frontend\src\pages\SingleAnalysis\SingleAnalysis.jsx": r"""import { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { useAnalysis } from '../../hooks/useAnalysis'
import KpiCard from '../../components/ui/KpiCard'
import ProgressBar from '../../components/ui/ProgressBar'
import CommentFilters from '../../components/comments/CommentFilters'
import CommentTable from '../../components/comments/CommentTable'
import LoadingSpinner from '../../components/ui/LoadingSpinner'
import { SENTIMENT_COLORS } from '../../utils/constants'
import { formatPercent } from '../../utils/formatters'
import styles from './SingleAnalysis.module.css'
import clsx from 'clsx'

export default function SingleAnalysis() {
  const [searchParams] = useSearchParams()
  const id = searchParams.get('id')
  const navigate = useNavigate()
  
  const { analysis, loading, fetchAnalysis } = useAnalysis()
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    if (!id) {
      navigate('/dashboard')
      return
    }
    fetchAnalysis(id, filter)
  }, [id, filter, fetchAnalysis, navigate])

  if (loading && !analysis) {
    return <div className={styles.center}><LoadingSpinner size="large" text="Loading Analysis..." /></div>
  }

  if (!analysis) {
    return <div className={styles.center}>Analysis not found</div>
  }

  const { metadata, summary, comments } = analysis
  const total = summary.total_comments
  
  const getPercent = (count) => total > 0 ? (count / total) : 0

  return (
    <div className={clsx('container', styles.analysis)}>
      <header className={styles.header}>
        <div>
          <button className={styles.backBtn} onClick={() => navigate(-1)}>
            <span className="material-symbols-outlined">arrow_back</span>
            Back
          </button>
          <h2>{metadata.filename}</h2>
          <p>Analysis ID: {metadata.analysis_id}</p>
        </div>
      </header>

      <div className={styles.summaryGrid}>
        <div className={clsx(styles.statsCard, 'neo-raised')}>
          <h3>Sentiment Breakdown</h3>
          <div className={styles.bars}>
            <ProgressBar 
              label="Positive" 
              value={(getPercent(summary.sentiment_counts.positive || 0) * 100).toFixed(1)} 
              color={SENTIMENT_COLORS.POSITIVE} 
            />
            <ProgressBar 
              label="Negative" 
              value={(getPercent(summary.sentiment_counts.negative || 0) * 100).toFixed(1)} 
              color={SENTIMENT_COLORS.NEGATIVE} 
            />
            <ProgressBar 
              label="Neutral" 
              value={(getPercent(summary.sentiment_counts.neutral || 0) * 100).toFixed(1)} 
              color={SENTIMENT_COLORS.NEUTRAL} 
            />
          </div>
        </div>

        <div className={styles.kpiCol}>
          <KpiCard 
            title="Total Comments" 
            value={total} 
            icon="forum" 
            highlightColor="var(--color-primary)" 
          />
          <KpiCard 
            title="Processing Time" 
            value={`${metadata.processing_time_sec.toFixed(2)}s`} 
            icon="timer" 
            highlightColor="var(--color-tertiary)" 
          />
        </div>
      </div>

      <div className={styles.commentsSection}>
        <div className={styles.commentsHeader}>
          <h3>Analyzed Comments</h3>
          <CommentFilters currentFilter={filter} onFilterChange={setFilter} />
        </div>
        
        {loading ? (
          <div className={styles.tableLoading}><LoadingSpinner /></div>
        ) : (
          <CommentTable comments={comments} />
        )}
      </div>
    </div>
  )
}
""",
    r"frontend\src\pages\SingleAnalysis\SingleAnalysis.module.css": r""".analysis {
  padding: 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header {
  margin-bottom: 1rem;
}

.backBtn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: var(--color-on-surface-variant);
  background: transparent;
  margin-bottom: 1rem;
  padding: 0;
}

.backBtn:hover {
  color: var(--color-primary);
}

.header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  word-break: break-all;
}

.header p {
  color: var(--color-on-surface-variant);
  font-size: 0.75rem;
  font-family: monospace;
}

.summaryGrid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.statsCard {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.statsCard h3 {
  font-size: 1.125rem;
  font-weight: 600;
}

.bars {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.kpiCol {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.commentsSection {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.commentsHeader {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.commentsHeader h3 {
  font-size: 1.25rem;
  font-weight: 600;
}

.tableLoading {
  padding: 4rem;
  display: flex;
  justify-content: center;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
}

.center {
  height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 900px) {
  .summaryGrid {
    grid-template-columns: 1fr;
  }
}
"""
}

base_dir = r"d:\moin\youtube_sentiment_analysis"

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 7 files written.")
