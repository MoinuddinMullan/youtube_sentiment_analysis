import clsx from 'clsx'
import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import CommentFilters from '../../components/comments/CommentFilters'
import CommentTable from '../../components/comments/CommentTable'
import KpiCard from '../../components/ui/KpiCard'
import LoadingSpinner from '../../components/ui/LoadingSpinner'
import ProgressBar from '../../components/ui/ProgressBar'
import { useAnalysis } from '../../hooks/useAnalysis'
import { SENTIMENT_COLORS } from '../../utils/constants'
import styles from './SingleAnalysis.module.css'

export default function SingleAnalysis() {
  const [searchParams] = useSearchParams()
  const id             = searchParams.get('id')
  const navigate       = useNavigate()
  const [filter, setFilter] = useState('all')

  // rawData = full API response:
  //   { success, analysis: {...}, comments: [...], total, page, limit }
  const { analysis: rawData, loading, fetchAnalysis } = useAnalysis()

  useEffect(() => {
    if (!id) {
      navigate('/dashboard')
      return
    }
    fetchAnalysis(id, filter)
  }, [id, filter, fetchAnalysis, navigate])

  // ── Loading ──────────────────────────────────────────────────────────
  if (loading && !rawData) {
    return (
      <div className={styles.center}>
        <LoadingSpinner size="large" text="Loading Analysis..." />
      </div>
    )
  }

  // ── Guard — no analysis document returned ────────────────────────────
  if (!rawData?.analysis) {
    return (
      <div className={styles.center}>
        <p>Analysis not found.</p>
      </div>
    )
  }

  // ── Map the real API fields ──────────────────────────────────────────
  // API key is "analysis" (object) — NOT "metadata" or "summary"
  const meta     = rawData.analysis       // the MongoDB analyses document
  const comments = rawData.comments ?? [] // paginated comment_predictions array

  const total         = meta.totalComments    ?? 0
  const positiveCount = meta.positiveCount    ?? 0
  const neutralCount  = meta.neutralCount     ?? 0
  const negativeCount = meta.negativeCount    ?? 0
  const avgConfidence = meta.averageConfidence ?? 0

  // Safe percentage helper
  const getPercent = (count) =>
    total > 0 ? ((count / total) * 100).toFixed(1) : '0.0'

  // Display title: fileName for CSV, friendly label for single predictions
  const displayName =
    meta.fileName ||
    (meta.sourceType === 'single'
      ? 'Single Comment Analysis'
      : `Analysis ${meta.analysisId}`)

  return (
    <div className={clsx('container', styles.analysis)}>

      {/* ── Header ── */}
      <header className={styles.header}>
        <div>
          <button className={styles.backBtn} onClick={() => navigate(-1)}>
            <span className="material-symbols-outlined">arrow_back</span>
            Back
          </button>
          <h2>{displayName}</h2>
          <p>Analysis ID: {meta.analysisId}</p>
        </div>
      </header>

      {/* ── Summary grid ── */}
      <div className={styles.summaryGrid}>
        <div className={clsx(styles.statsCard, 'ga-card ga-card--panel')}>
          <h3>Sentiment Breakdown</h3>
          <div className={styles.bars}>
            <ProgressBar
              label="Positive"
              value={getPercent(positiveCount)}
              color={SENTIMENT_COLORS.POSITIVE}
            />
            <ProgressBar
              label="Neutral"
              value={getPercent(neutralCount)}
              color={SENTIMENT_COLORS.NEUTRAL}
            />
            <ProgressBar
              label="Negative"
              value={getPercent(negativeCount)}
              color={SENTIMENT_COLORS.NEGATIVE}
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
            title="Avg Confidence"
            value={`${(avgConfidence * 100).toFixed(1)}%`}
            icon="psychology"
            highlightColor="var(--color-tertiary)"
          />
        </div>
      </div>

      {/* ── Comments table ── */}
      <div className={styles.commentsSection}>
        <div className={styles.commentsHeader}>
          <h3>Analyzed Comments</h3>
          <CommentFilters currentFilter={filter} onFilterChange={setFilter} />
        </div>

        {loading ? (
          <div className={clsx(styles.tableLoading, 'ga-card ga-card--panel')}>
            <LoadingSpinner />
          </div>
        ) : (
          <CommentTable comments={comments} />
        )}
      </div>

    </div>
  )
}
