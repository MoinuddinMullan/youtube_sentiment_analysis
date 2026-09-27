import { useState } from 'react'
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
