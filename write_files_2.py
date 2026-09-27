import os

files = {
    r"frontend\src\utils\constants.js": r"""export const SENTIMENT_COLORS = {
  POSITIVE: '#10b981',
  NEGATIVE: '#ef4444',
  NEUTRAL: '#64748b'
}

export const SENTIMENT_ICONS = {
  POSITIVE: 'sentiment_satisfied',
  NEGATIVE: 'sentiment_dissatisfied',
  NEUTRAL: 'sentiment_neutral'
}

export const APP_NAME = "Sentiview AI"
""",

    r"frontend\src\utils\formatters.js": r"""export const formatNumber = (num) => {
  if (num === null || num === undefined) return '0'
  return new Intl.NumberFormat('en-US').format(num)
}

export const formatPercent = (decimal) => {
  if (decimal === null || decimal === undefined) return '0%'
  return (decimal * 100).toFixed(1) + '%'
}

export const formatDate = (isoString) => {
  if (!isoString) return ''
  return new Date(isoString).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: 'numeric', minute: 'numeric'
  })
}

export const truncate = (str, len = 100) => {
  if (!str) return ''
  return str.length > len ? str.substring(0, len) + '...' : str
}
""",

    r"frontend\src\hooks\useSentiment.js": r"""import { useState } from 'react'
import { predictSingle, predictBatch } from '../api/sentimentApi'
import toast from 'react-hot-toast'

export const useSentiment = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const analyzeSingle = async (text) => {
    if (!text.trim()) return
    setLoading(true)
    try {
      const data = await predictSingle(text)
      setResult(data)
    } catch (err) {
      toast.error(err.message || "Prediction failed")
    } finally {
      setLoading(false)
    }
  }

  return { loading, result, analyzeSingle, setResult }
}
""",

    r"frontend\src\hooks\useAnalysis.js": r"""import { useState, useCallback } from 'react'
import { uploadCsv, getAnalysisDetail } from '../api/sentimentApi'
import toast from 'react-hot-toast'

export const useAnalysis = () => {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState(null)

  const uploadFile = async (file, navigate) => {
    setLoading(true)
    const toastId = toast.loading('Uploading and analyzing file... This may take a few minutes.')
    try {
      const data = await uploadCsv(file)
      toast.success('Analysis complete!', { id: toastId })
      navigate(`/analyze?id=${data.analysis_id}`)
    } catch (err) {
      toast.error(err.message || 'Upload failed', { id: toastId })
    } finally {
      setLoading(false)
    }
  }

  const fetchAnalysis = useCallback(async (id, filter = 'all', page = 1) => {
    setLoading(true)
    try {
      const data = await getAnalysisDetail(id, filter, page)
      setAnalysis(data)
    } catch (err) {
      toast.error('Failed to load analysis')
    } finally {
      setLoading(false)
    }
  }, [])

  return { loading, analysis, uploadFile, fetchAnalysis }
}
""",

    r"frontend\src\hooks\useComments.js": r"""import { useState } from 'react'

export const useComments = (initialComments = []) => {
  const [comments, setComments] = useState(initialComments)

  // Could add pagination/filtering logic here later if needed client-side

  return { comments, setComments }
}
""",
    r"frontend\src\components\ui\LoadingSpinner.jsx": r"""import styles from './LoadingSpinner.module.css'

export default function LoadingSpinner({ size = 'medium', text }) {
  return (
    <div className={styles.container}>
      <div className={`${styles.spinner} ${styles[size]}`}></div>
      {text && <p className={styles.text}>{text}</p>}
    </div>
  )
}
""",
    r"frontend\src\components\ui\LoadingSpinner.module.css": r""".container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
}

.spinner {
  border: 3px solid var(--color-surface-dim);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.small { width: 24px; height: 24px; border-width: 2px; }
.medium { width: 40px; height: 40px; }
.large { width: 64px; height: 64px; border-width: 4px; }

.text {
  color: var(--color-on-surface-variant);
  font-size: 0.875rem;
  font-weight: 500;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
""",
    r"frontend\src\components\ui\SentimentBadge.jsx": r"""import { SENTIMENT_COLORS, SENTIMENT_ICONS } from '../../utils/constants'
import styles from './SentimentBadge.module.css'

export default function SentimentBadge({ sentiment }) {
  if (!sentiment) return null
  const upper = sentiment.toUpperCase()
  const color = SENTIMENT_COLORS[upper] || SENTIMENT_COLORS.NEUTRAL
  const icon = SENTIMENT_ICONS[upper] || SENTIMENT_ICONS.NEUTRAL

  return (
    <div className={`${styles.badge} neo-inset`} style={{ '--badge-color': color }}>
      <span className="material-symbols-outlined">{icon}</span>
      <span>{sentiment}</span>
    </div>
  )
}
""",
    r"frontend\src\components\ui\SentimentBadge.module.css": r""".badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: capitalize;
  color: var(--badge-color);
  background: var(--color-surface);
}

.badge span.material-symbols-outlined {
  font-size: 14px;
}
"""
}

base_dir = r"d:\moin\youtube_sentiment_analysis"

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 2 files written.")
