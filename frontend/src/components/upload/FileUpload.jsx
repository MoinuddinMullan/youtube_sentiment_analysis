import clsx from 'clsx'
import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import styles from './FileUpload.module.css'

export default function FileUpload({ onUpload, loading }) {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0 && !loading) {
      onUpload(acceptedFiles[0])
    }
  }, [onUpload, loading])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv']
    },
    maxFiles: 1,
    disabled: loading
  })

  return (
    <div 
      {...getRootProps()} 
      className={clsx(
        styles.dropzone, 
        'ga-card ga-card--stat',
        isDragActive && styles.active,
        loading && styles.disabled
      )}
    >
      <input {...getInputProps()} />
      <div className={styles.content}>
        <span className={clsx("material-symbols-outlined", styles.icon)}>
          {loading ? 'cloud_sync' : 'cloud_upload'}
        </span>
        <h3>{loading ? 'Processing...' : 'Drag & Drop your CSV file here'}</h3>
        <p>Supports files up to 25MB with columns: comment_text</p>
        <button type="button" className={clsx(styles.btn, 'neo-raised-sm')} disabled={loading}>
          Browse Files
        </button>
      </div>
    </div>
  )
}
