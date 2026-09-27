import clsx from 'clsx'
import { formatNumber, truncate } from '../../utils/formatters'
import SentimentBadge from '../ui/SentimentBadge'
import styles from './Comments.module.css'

export default function CommentTable({ comments }) {
  if (!comments || comments.length === 0) {
    return <div className={styles.empty}>No comments found.</div>
  }

  return (
    <div className={clsx(styles.tableWrapper, 'ga-card ga-card--panel')}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Author</th>
            <th>Comment</th>
            <th>Likes</th>
            <th>Sentiment</th>
            <th>Confidence</th>
          </tr>
        </thead>
        <tbody>
          {comments.map((c, i) => (
            <tr key={c.comment_id || i}>
              <td>{c.author || 'Anonymous'}</td>
              <td className={styles.textCell}>{truncate(c.commentText ?? c.comment_text, 80)}</td>
              <td>{formatNumber(c.like_count)}</td>
              <td>
                <SentimentBadge sentiment={c.predicted_sentiment || c.sentiment} />
              </td>
              <td>{c.confidence ? `${(c.confidence * 100).toFixed(1)}%` : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
