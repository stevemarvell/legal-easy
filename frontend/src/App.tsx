import { useState } from 'react'
import './App.css'

// Auto-detect backend URL based on environment
function getBackendUrl(): string {
  // Use Vite's build-time environment variable injection
  return __BACKEND_URL__;
}

function App() {
  const [randomNumber, setRandomNumber] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const backendUrl = getBackendUrl()

  const fetchRandom = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${backendUrl}/random`)
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const data: { value: number } = await response.json()
      setRandomNumber(data.value)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="card">
        <h1>Legal Easy</h1>
        <p>Click the button to fetch a random number from the FastAPI backend.</p>
        
        <button 
          onClick={fetchRandom} 
          disabled={loading}
          className="button"
        >
          {loading ? 'Loading...' : 'Get Random Number'}
        </button>
        
        <div className="output">
          {error && <div className="error">Error: {error}</div>}
          {randomNumber !== null && !error && (
            <div className="result">{randomNumber}</div>
          )}
          {randomNumber === null && !loading && !error && '—'}
        </div>
        
        <p className="backend-info">
          Backend: {backendUrl}
        </p>
      </div>
    </div>
  )
}

export default App