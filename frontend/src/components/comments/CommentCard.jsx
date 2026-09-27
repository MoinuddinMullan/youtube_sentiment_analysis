import clsx from 'clsx'
import { formatNumber, truncate } from '../../utils/formatters'
import SentimentBadge from '../ui/SentimentBadge'
import styles from './Comments.module.css'

export default function CommentCard({ comment }) {
  return (
    <div className={clsx(styles.card, 'ga-card ga-card--panel')}>
      <div className={styles.header}>
        <div className={styles.author}>
          <div className={styles.avatar}>
            {comment.author ? comment.author.charAt(0).toUpperCase() : 'A'}
          </div>
          <span className={styles.authorName}>{comment.author || 'Anonymous'}</span>
        </div>
        <SentimentBadge sentiment={comment.predicted_sentiment || comment.sentiment} />
      </div>
      
      <p className={styles.text}>{truncate(comment.commentText ?? comment.comment_text, 150)}</p>
      
      <div className={styles.footer}>
        <div className={styles.stat}>
          <span className="material-symbols-outlined">thumb_up</span>
          {formatNumber(comment.like_count)}
        </div>
        {comment.confidence && (
          <div className={styles.confidence}>
            Conf: {(comment.confidence * 100).toFixed(1)}%
          </div>
        )}
      </div>
    </div>
  )
}
