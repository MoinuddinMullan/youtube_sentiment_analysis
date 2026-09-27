import { SENTIMENT_ICONS } from '../../utils/constants'
import styles from './SentimentBadge.module.css'

export default function SentimentBadge({ sentiment }) {
  if (!sentiment) return null
  const upper = sentiment.toUpperCase()
  const icon = SENTIMENT_ICONS[upper] || SENTIMENT_ICONS.NEUTRAL
  const sentimentClass = ['POSITIVE', 'NEUTRAL', 'NEGATIVE'].includes(upper) ? upper.toLowerCase() : 'neutral'

  return (
    <div className={`${styles.badge} sentiment-pill sentiment-pill--${sentimentClass}`}>
      <span className="material-symbols-outlined">{icon}</span>
      <span>{sentiment}</span>
    </div>
  )
}
