import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 120000
})

API.interceptors.response.use(
  response => response,
  error => {
    console.error('API request failed:', error)
    const message = error.response?.data?.detail || error.message || 'Request failed'
    return Promise.reject(new Error(message))
  }
)

export const predictSingle = (text) =>
  API.post('/api/predict', { text }).then(r => r.data)

export const predictBatch = (comments) =>
  API.post('/api/predict/batch', { comments }).then(r => r.data)

export const uploadCsv = (file, page = 1, limit = 50) => {
  const form = new FormData()
  form.append('file', file)
  return API.post(`/api/analysis/upload?page=${page}&limit=${limit}`, form, {
    timeout: 300000 // 5 min for large files
  }).then(r => r.data)
}

export const getHistory = (page = 1, limit = 20) =>
  API.get(`/api/analysis/history?page=${page}&limit=${limit}`).then(r => r.data)

export const getAnalysisDetail = (id, sentiment = 'all', page = 1, limit = 50) =>
  API.get(`/api/analysis/${id}?sentiment=${sentiment}&page=${page}&limit=${limit}`).then(r => r.data)

export const getOverviewStats = () =>
  API.get('/api/analysis/stats/overview').then(r => r.data)

export const healthCheck = () =>
  API.get('/api/health').then(r => r.data)