import React from 'react'
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
)