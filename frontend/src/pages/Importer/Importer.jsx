import clsx from 'clsx'
import { useNavigate } from 'react-router-dom'
import SentimentBadge from '../../components/ui/SentimentBadge'
import FileUpload from '../../components/upload/FileUpload'
import { useAnalysis } from '../../hooks/useAnalysis'
import { useSentiment } from '../../hooks/useSentiment'
import styles from './Importer.module.css'

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
          
          <form onSubmit={handleManualPredict} className={clsx(styles.form, 'ga-card ga-card--stat')}>
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
