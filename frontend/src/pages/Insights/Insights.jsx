import clsx from 'clsx'
import { useEffect, useState } from 'react'
import { getHistory, getOverviewStats } from '../../api/sentimentApi'
import BarChart from '../../components/charts/BarChart'
import LoadingSpinner from '../../components/ui/LoadingSpinner'
import styles from './Insights.module.css'

export default function Insights() {
  const [trendData,     setTrendData]     = useState([])
  const [sentimentData, setSentimentData] = useState([])
  const [sourceData,    setSourceData]    = useState([])
  const [overview,      setOverview]      = useState(null)
  const [loading,       setLoading]       = useState(true)
  const [error,         setError]         = useState(null)

  useEffect(() => {
    Promise.all([getHistory(1, 100), getOverviewStats()])
      .then(([historyRes, overviewRes]) => {

        const analyses = historyRes?.data ?? []
        const ov       = overviewRes?.data ?? {}

        // ── Chart 1: Analyses Over Time ─────────────────────────────
        // Group analyses by calendar date (e.g. "Sep 26")
        const dateMap = {}
        analyses.forEach(item => {
          if (!item.createdAt) return
          const label = new Date(item.createdAt).toLocaleDateString('en-US', {
            month: 'short',
            day:   'numeric',
          })
          dateMap[label] = (dateMap[label] ?? 0) + 1
        })
        setTrendData(
          Object.entries(dateMap).map(([date, count]) => ({ date, count }))
        )

        // ── Chart 2: Average Sentiment Distribution ─────────────────
        // Uses avgPositive / avgNeutral / avgNegative from overview stats
        if (ov.avgPositive !== undefined) {
          setSentimentData([
            { label: 'Positive', value: parseFloat((ov.avgPositive ?? 0).toFixed(1)) },
            { label: 'Neutral',  value: parseFloat((ov.avgNeutral  ?? 0).toFixed(1)) },
            { label: 'Negative', value: parseFloat((ov.avgNegative ?? 0).toFixed(1)) },
          ])
        }

        // ── Chart 3: Analysis Source Breakdown ──────────────────────
        // Group analyses by sourceType
        const srcMap = {}
        analyses.forEach(item => {
          const label = item.sourceType === 'csv' ? 'CSV Upload' : 'Quick Test'
          srcMap[label] = (srcMap[label] ?? 0) + 1
        })
        setSourceData(
          Object.entries(srcMap).map(([label, count]) => ({ label, count }))
        )

        setOverview(ov)
      })
      .catch(err => {
        console.error('Insights fetch failed:', err)
        setError('Could not load insights data.')
      })
      .finally(() => setLoading(false))
  }, [])

  // ── Loading ────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className={styles.center}>
        <LoadingSpinner size="large" />
      </div>
    )
  }

  // ── Error ──────────────────────────────────────────────────────────
  if (error) {
    return <div className={styles.center} role="alert">{error}</div>
  }

  return (
    <div className={clsx('container', styles.insights)}>

      {/* ── Page header ── */}
      <div className={styles.header}>
        <h2>Sentiment Insights</h2>
        <p>Deep dive into your data trends</p>
      </div>

      {/* ── KPI summary row ── */}
      {overview && (
        <div className={styles.kpiRow}>
          <div className={clsx(styles.kpi, 'ga-card ga-card--stat')}>
            <span className={styles.kpiIcon}>
              <span className="material-symbols-outlined">analytics</span>
            </span>
            <span className={styles.kpiValue}>
              {overview.totalAnalyses ?? 0}
            </span>
            <span className={styles.kpiLabel}>Total Analyses</span>
          </div>

          <div className={clsx(styles.kpi, 'ga-card ga-card--stat')}>
            <span className={styles.kpiIcon}>
              <span className="material-symbols-outlined">forum</span>
            </span>
            <span className={styles.kpiValue}>
              {(overview.totalComments ?? 0).toLocaleString()}
            </span>
            <span className={styles.kpiLabel}>Comments Analyzed</span>
          </div>

          <div className={clsx(styles.kpi, 'ga-card ga-card--stat')}>
            <span className={styles.kpiIcon}>
              <span className="material-symbols-outlined">psychology</span>
            </span>
            <span className={styles.kpiValue}>
              {overview.avgConfidence !== undefined
                ? `${(overview.avgConfidence * 100).toFixed(1)}%`
                : '—'}
            </span>
            <span className={styles.kpiLabel}>Avg Confidence</span>
          </div>
        </div>
      )}

      {/* ── Chart 1: Analyses Over Time ── */}
      <div className={clsx(styles.chartSection, 'ga-card ga-card--panel')}>
        <div className={styles.chartHeader}>
          <h3>Analyses Over Time</h3>
          <span className={styles.subtitle}>
            Number of analyses performed per day
          </span>
        </div>
        <div className={styles.chartWrapper}>
          <BarChart
            data={trendData}
            xAxisKey="date"
            barKey="count"
          />
        </div>
      </div>

      {/* ── Chart 2: Average Sentiment Distribution ── */}
      {sentimentData.length > 0 && (
        <div className={clsx(styles.chartSection, 'ga-card ga-card--panel')}>
          <div className={styles.chartHeader}>
            <h3>Average Sentiment Distribution</h3>
            <span className={styles.subtitle}>
              Average sentiment percentage across all analyses
            </span>
          </div>
          <div className={styles.chartWrapper}>
            <BarChart
              data={sentimentData}
              xAxisKey="label"
              barKey="value"
              color="var(--blue)"
            />
          </div>
        </div>
      )}

      {/* ── Chart 3: Source Type Breakdown ── */}
      {sourceData.length > 0 && (
        <div className={clsx(styles.chartSection, 'ga-card ga-card--panel')}>
          <div className={styles.chartHeader}>
            <h3>Analysis Source Breakdown</h3>
            <span className={styles.subtitle}>
              CSV bulk uploads vs quick single-comment tests
            </span>
          </div>
          <div className={styles.chartWrapper}>
            <BarChart
              data={sourceData}
              xAxisKey="label"
              barKey="count"
              color="var(--indigo)"
            />
          </div>
        </div>
      )}

    </div>
  )
}
