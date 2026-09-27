import { Routes, Route, Navigate } from 'react-router-dom'
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
}