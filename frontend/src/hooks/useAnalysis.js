import { useCallback, useState } from 'react'
import toast from 'react-hot-toast'
import { getAnalysisDetail, uploadCsv } from '../api/sentimentApi'

export const useAnalysis = () => {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState(null)

  const uploadFile = async (file, navigate) => {
    setLoading(true)
    const toastId = toast.loading('Uploading and analyzing file... This may take a few minutes.')
    try {
      const data = await uploadCsv(file)
      toast.success('Analysis complete!', { id: toastId })
      navigate(`/analyze?id=${data.analysisId}`)
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
