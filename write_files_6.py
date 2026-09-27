import os

files = {
    r"frontend\src\pages\Dashboard\Dashboard.jsx": r"""import { useState, useEffect } from 'react'
import { getOverviewStats } from '../../api/sentimentApi'
import KpiCard from '../../components/ui/KpiCard'
import DonutChart from '../../components/charts/DonutChart'
import LoadingSpinner from '../../components/ui/LoadingSpinner'
import { Link } from 'react-router-dom'
import styles from './Dashboard.module.css'
import clsx from 'clsx'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getOverviewStats()
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className={styles.center}><LoadingSpinner size="large" /></div>
  
  // Fake data if api fails
  const data = stats || {
    totalAnalyses: 0,
    totalCommentsAnalyzed: 0,
    averageSentiment: 'N/A',
    sentimentDistribution: []
  }

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
          value={data.totalAnalyses} 
          icon="analytics" 
          highlightColor="var(--color-primary)" 
        />
        <KpiCard 
          title="Comments Analyzed" 
          value={data.totalCommentsAnalyzed} 
          icon="forum" 
          highlightColor="var(--color-tertiary)" 
        />
        <KpiCard 
          title="Avg Sentiment" 
          value={data.averageSentiment || 'Neutral'} 
          icon="mood" 
          highlightColor="#10b981" 
        />
      </div>

      <div className={styles.charts}>
        <div className={clsx(styles.chartCard, 'neo-raised')}>
          <h3>Global Sentiment Distribution</h3>
          <DonutChart data={data.sentimentDistribution} />
        </div>
        
        <div className={clsx(styles.quickActions, 'neo-raised')}>
          <h3>Quick Actions</h3>
          <div className={styles.actionList}>
            <Link to="/import" className={clsx(styles.quickBtn, 'neo-inset')}>
              <span className="material-symbols-outlined">upload_file</span>
              Upload CSV
            </Link>
            <Link to="/insights" className={clsx(styles.quickBtn, 'neo-inset')}>
              <span className="material-symbols-outlined">insights</span>
              View Insights
            </Link>
            <Link to="/comments" className={clsx(styles.quickBtn, 'neo-inset')}>
              <span className="material-symbols-outlined">search</span>
              Explore Comments
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
""",
    r"frontend\src\pages\Dashboard\Dashboard.module.css": r""".dashboard {
  padding: 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
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

.actionBtn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  transition: transform 0.2s;
}

.actionBtn:hover {
  transform: translateY(-2px);
}

.kpiGrid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.charts {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.chartCard, .quickActions {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.chartCard h3, .quickActions h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-on-surface);
}

.actionList {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 1;
}

.quickBtn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: var(--radius-md);
  font-weight: 600;
  color: var(--color-on-surface-variant);
  transition: color 0.2s;
}

.quickBtn:hover {
  color: var(--color-primary);
}

.center {
  height: calc(100vh - 80px - 80px); /* rough height without nav/footer */
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .charts {
    grid-template-columns: 1fr;
  }
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
""",
    r"frontend\src\pages\Importer\Importer.jsx": r"""import { useNavigate } from 'react-router-dom'
import { useAnalysis } from '../../hooks/useAnalysis'
import { useSentiment } from '../../hooks/useSentiment'
import FileUpload from '../../components/upload/FileUpload'
import SentimentBadge from '../../components/ui/SentimentBadge'
import styles from './Importer.module.css'
import clsx from 'clsx'

export default function Importer() {
  const navigate = useNavigate()
  const { uploadFile, loading: uploading } = useAnalysis()
  const { analyzeSingle, result, loading: predicting } = useSentiment()

  const handleManualPredict = (e) => {
    e.preventDefault()
    const text = new FormData(e.target).get('text')
    analyzeSingle(text)
  }

  return (
    <div className={clsx('container', styles.importer)}>
      <div className={styles.grid}>
        
        {/* Bulk Upload Section */}
        <section className={styles.section}>
          <div className={styles.header}>
            <h2>Bulk Analysis</h2>
            <p>Upload a CSV file containing YouTube comments.</p>
          </div>
          <FileUpload onUpload={(file) => uploadFile(file, navigate)} loading={uploading} />
        </section>

        {/* Single Prediction Section */}
        <section className={styles.section}>
          <div className={styles.header}>
            <h2>Quick Test</h2>
            <p>Test the model on a single comment.</p>
          </div>
          
          <form onSubmit={handleManualPredict} className={clsx(styles.form, 'neo-raised')}>
            <textarea
              name="text"
              placeholder="Type a comment here..."
              className={clsx(styles.textarea, 'neo-inset')}
              disabled={predicting}
              required
            ></textarea>
            <button 
              type="submit" 
              className={clsx(styles.btn, 'neo-raised-sm')}
              disabled={predicting}
            >
              {predicting ? 'Analyzing...' : 'Analyze Text'}
            </button>
            
            {result && (
              <div className={styles.result}>
                <h4>Prediction Result:</h4>
                <div className={styles.resultRow}>
                  <SentimentBadge sentiment={result.sentiment} />
                  <span>Confidence: {(result.confidence * 100).toFixed(1)}%</span>
                </div>
              </div>
            )}
          </form>
        </section>

      </div>
    </div>
  )
}
""",
    r"frontend\src\pages\Importer\Importer.module.css": r""".importer {
  padding: 2rem 0;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.header p {
  color: var(--color-on-surface-variant);
  font-size: 0.875rem;
}

.form {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.textarea {
  width: 100%;
  height: 120px;
  padding: 1rem;
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-on-surface);
  resize: none;
  font-size: 0.875rem;
}

.btn {
  align-self: flex-end;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.result {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-surface-dim);
}

.result h4 {
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
  color: var(--color-on-surface-variant);
}

.resultRow {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .grid {
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

print("Batch 6 files written.")
