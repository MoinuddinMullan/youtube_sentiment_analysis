import os

files = {
    r"frontend\src\components\comments\CommentCard.jsx": r"""import SentimentBadge from '../ui/SentimentBadge'
import { truncate, formatNumber } from '../../utils/formatters'
import styles from './Comments.module.css'
import clsx from 'clsx'

export default function CommentCard({ comment }) {
  return (
    <div className={clsx(styles.card, 'neo-raised')}>
      <div className={styles.header}>
        <div className={styles.author}>
          <div className={styles.avatar}>
            {comment.author ? comment.author.charAt(0).toUpperCase() : 'A'}
          </div>
          <span className={styles.authorName}>{comment.author || 'Anonymous'}</span>
        </div>
        <SentimentBadge sentiment={comment.predicted_sentiment || comment.sentiment} />
      </div>
      
      <p className={styles.text}>{truncate(comment.comment_text, 150)}</p>
      
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
""",
    r"frontend\src\components\comments\CommentTable.jsx": r"""import SentimentBadge from '../ui/SentimentBadge'
import { truncate, formatNumber } from '../../utils/formatters'
import styles from './Comments.module.css'
import clsx from 'clsx'

export default function CommentTable({ comments }) {
  if (!comments || comments.length === 0) {
    return <div className={styles.empty}>No comments found.</div>
  }

  return (
    <div className={clsx(styles.tableWrapper, 'neo-raised')}>
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
              <td className={styles.textCell}>{truncate(c.comment_text, 80)}</td>
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
""",
    r"frontend\src\components\comments\CommentFilters.jsx": r"""import styles from './Comments.module.css'
import clsx from 'clsx'

export default function CommentFilters({ currentFilter, onFilterChange }) {
  const filters = [
    { value: 'all', label: 'All Comments' },
    { value: 'positive', label: 'Positive' },
    { value: 'negative', label: 'Negative' },
    { value: 'neutral', label: 'Neutral' }
  ]

  return (
    <div className={styles.filters}>
      {filters.map(f => (
        <button
          key={f.value}
          className={clsx(
            styles.filterBtn,
            currentFilter === f.value ? 'neo-inset active' : 'neo-raised-sm'
          )}
          onClick={() => onFilterChange(f.value)}
          style={{
            color: currentFilter === f.value ? 'var(--color-primary)' : 'var(--color-on-surface-variant)'
          }}
        >
          {f.label}
        </button>
      ))}
    </div>
  )
}
""",
    r"frontend\src\components\comments\Comments.module.css": r""".card {
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--color-primary-dim);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
}

.authorName {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--color-on-surface);
}

.text {
  font-size: 0.875rem;
  color: var(--color-on-surface-variant);
  line-height: 1.5;
  flex: 1;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: var(--color-outline);
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat span {
  font-size: 16px;
}

.confidence {
  font-weight: 500;
}

.tableWrapper {
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.table th {
  padding: 1.25rem 1.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-on-surface-variant);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--color-surface-dim);
}

.table td {
  padding: 1.25rem 1.5rem;
  font-size: 0.875rem;
  color: var(--color-on-surface);
  border-bottom: 1px solid var(--color-surface-dim);
}

.table tr:last-child td {
  border-bottom: none;
}

.textCell {
  max-width: 300px;
}

.empty {
  padding: 3rem;
  text-align: center;
  color: var(--color-on-surface-variant);
}

.filters {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.filterBtn {
  padding: 0.5rem 1.25rem;
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 600;
  background: var(--color-surface);
  white-space: nowrap;
}
"""
}

base_dir = r"d:\moin\youtube_sentiment_analysis"

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 5 files written.")
