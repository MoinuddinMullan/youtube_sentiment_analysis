import os

files = {
    r"frontend\package.json": r"""{
  "name": "sentiview-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.24.0",
    "axios": "^1.7.2",
    "recharts": "^2.12.7",
    "react-dropzone": "^14.2.3",
    "papaparse": "^5.4.1",
    "react-hot-toast": "^2.4.1",
    "clsx": "^2.1.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.3.1"
  }
}""",

    r"frontend\vite.config.js": r"""import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})""",

    r"frontend\index.html": r"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sentiview AI — YouTube Sentiment Analysis</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>""",

    r"frontend\.env": r"""VITE_API_URL=http://localhost:8000""",

    r"frontend\src\main.jsx": r"""import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App.jsx'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: 'var(--color-background)',
            color: 'var(--color-on-surface)',
            boxShadow: 'var(--shadow-raised)',
            fontFamily: 'var(--font-family)',
            borderRadius: 'var(--radius-md)',
            fontSize: '13px'
          }
        }}
      />
    </BrowserRouter>
  </React.StrictMode>
)""",

    r"frontend\src\App.jsx": r"""import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/layout/Navbar.jsx'
import Footer from './components/layout/Footer.jsx'
import Dashboard from './pages/Dashboard/Dashboard.jsx'
import Importer from './pages/Importer/Importer.jsx'
import CommentExplorer from './pages/CommentExplorer/CommentExplorer.jsx'
import Insights from './pages/Insights/Insights.jsx'
import SingleAnalysis from './pages/SingleAnalysis/SingleAnalysis.jsx'

export default function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <main style={{ flex: 1, paddingTop: '80px' }}>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/import" element={<Importer />} />
          <Route path="/comments" element={<CommentExplorer />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="/analyze" element={<SingleAnalysis />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}""",

    r"frontend\src\styles\global.css": r"""@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

:root {
  /* Brand Colors */
  --color-primary:            #6366f1;
  --color-primary-dim:        #a5b4fc;
  --color-primary-container:  #818cf8;
  --color-tertiary:           #7c3aed;
  --color-tertiary-container: #a78bfa;
  --color-secondary:          #6c6e7e;
  --color-error:              #dc2626;
  --color-error-container:    #fee2e2;

  /* Surfaces */
  --color-background:         #e8eaf0;
  --color-surface:            #e8eaf0;
  --color-surface-container:  #e2e4ea;
  --color-surface-low:        #e5e7ed;
  --color-surface-lowest:     #f0f2f8;
  --color-surface-high:       #dcdee4;
  --color-surface-highest:    #d6d8de;
  --color-surface-variant:    #dcdee4;
  --color-surface-dim:        #d4d6dc;

  /* Text */
  --color-on-surface:         #2e3040;
  --color-on-surface-variant: #585a68;
  --color-outline:            #8a8c9a;
  --color-outline-variant:    #d0d2dc;
  --color-on-primary:         #ffffff;

  /* Inverse */
  --color-inverse-surface:    #2e3040;
  --color-inverse-on-surface: #e8eaf0;

  /* Neomorphic Shadows */
  --shadow-raised:    6px 6px 14px rgba(0,0,0,0.06), -6px -6px 14px rgba(255,255,255,0.8);
  --shadow-raised-sm: 3px 3px 8px rgba(0,0,0,0.05),  -3px -3px 8px rgba(255,255,255,0.7);
  --shadow-inset:     inset 3px 3px 6px rgba(0,0,0,0.06), inset -3px -3px 6px rgba(255,255,255,0.6);

  /* Typography */
  --font-family: 'Plus Jakarta Sans', sans-serif;

  /* Border Radius */
  --radius-sm:   0.5rem;
  --radius-md:   1rem;
  --radius-lg:   1.5rem;
  --radius-full: 9999px;

  /* Transitions */
  --transition-base: all 0.2s ease;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background-color: var(--color-background);
  font-family: var(--font-family);
  color: var(--color-on-surface);
  -webkit-font-smoothing: antialiased;
  overscroll-behavior: none;
}

/* Reusable neo shadow utility classes (apply globally) */
.neo-raised    { box-shadow: var(--shadow-raised); }
.neo-raised-sm { box-shadow: var(--shadow-raised-sm); }
.neo-inset     { box-shadow: var(--shadow-inset); }

/* Material Symbols */
.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-style: normal;
  font-weight: normal;
  display: inline-block;
  vertical-align: middle;
  line-height: 1;
  user-select: none;
}

button { cursor: pointer; border: none; outline: none; font-family: var(--font-family); }
input, textarea, select { font-family: var(--font-family); outline: none; border: none; }
a { text-decoration: none; color: inherit; }

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

@media (max-width: 768px) {
  .container { padding: 0 1rem; }
}""",

    r"frontend\src\api\sentimentApi.js": r"""import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 120000
})

API.interceptors.response.use(
  response => response,
  error => {
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
  API.get('/api/health').then(r => r.data)"""
}

base_dir = r"d:\moin\youtube_sentiment_analysis"

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 1 files written.")
