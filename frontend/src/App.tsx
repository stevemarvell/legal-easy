import { useState, useEffect } from 'react';
import './App.css';

interface Case {
  id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  case_type: string;
  created_at: string;
}

interface Document {
  id: string;
  filename: string;
  case_id: string;
  file_type: string;
  upload_date: string;
  analysis_status: string;
}

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [cases, setCases] = useState<Case[]>([]);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);

  useEffect(() => {
    // Load cases data when app first loads for dashboard stats
    fetchCases();
  }, []);

  useEffect(() => {
    if (currentView === 'cases') {
      fetchCases();
    }
  }, [currentView]);

  const fetchCases = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/cases');
      if (response.ok) {
        const data = await response.json();
        setCases(data);
      }
    } catch (error) {
      console.error('Error fetching cases:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchDocuments = async (caseId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/cases/${caseId}/documents`);
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const performSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/legal-research/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchQuery }),
      });
      if (response.ok) {
        const data = await response.json();
        setSearchResults(data.results || []);
      }
    } catch (error) {
      console.error('Error performing search:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderDashboard = () => (
    <div className="dashboard">
      <h1>Shift AI Legal Platform</h1>
      <p>AI-powered legal case management and research platform</p>
      
      {loading ? (
        <p>Loading dashboard data...</p>
      ) : (
        <div className="stats">
          <div className="stat-card">
            <h3>Total Cases</h3>
            <p className="stat-number">{cases.length}</p>
          </div>
          <div className="stat-card">
            <h3>Active Cases</h3>
            <p className="stat-number">{cases.filter(c => c.status === 'active').length}</p>
          </div>
          <div className="stat-card">
            <h3>Pending Cases</h3>
            <p className="stat-number">{cases.filter(c => c.status === 'pending').length}</p>
          </div>
        </div>
      )}

      {cases.length > 0 && (
        <div className="recent-cases">
          <h2>Recent Cases</h2>
          <div className="cases-preview">
            {cases.slice(0, 3).map((case_) => (
              <div key={case_.id} className="case-preview-card">
                <div className="case-header">
                  <h3>{case_.title}</h3>
                  <span className={`status ${case_.status}`}>{case_.status}</span>
                </div>
                <p>{case_.description}</p>
                <div className="case-meta">
                  <span>Type: {case_.case_type}</span>
                  <span>Priority: {case_.priority}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderCases = () => (
    <div className="cases">
      <h1>Legal Cases</h1>
      {loading ? (
        <p>Loading cases...</p>
      ) : (
        <div className="cases-grid">
          {cases.map((case_) => (
            <div key={case_.id} className="case-card">
              <div className="case-header">
                <h3>{case_.title}</h3>
                <span className={`status ${case_.status}`}>{case_.status}</span>
              </div>
              <p>{case_.description}</p>
              <div className="case-meta">
                <span>Type: {case_.case_type}</span>
                <span>Priority: {case_.priority}</span>
              </div>
              <button onClick={() => fetchDocuments(case_.id)}>
                View Documents
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderLegalResearch = () => (
    <div className="legal-research">
      <h1>Legal Research</h1>
      <div className="search-box">
        <input
          type="text"
          placeholder="Search legal documents, cases, or ask a question..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && performSearch()}
        />
        <button onClick={performSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
      
      {searchResults.length > 0 && (
        <div className="search-results">
          <h3>Search Results</h3>
          {searchResults.map((result, index) => (
            <div key={index} className="result-card">
              <h4>{result.title}</h4>
              <p>{result.content}</p>
              <div className="result-meta">
                <span>Source: {result.source}</span>
                <span>Relevance: {Math.round(result.relevance_score * 100)}%</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderContent = () => {
    switch (currentView) {
      case 'cases':
        return renderCases();
      case 'legal-research':
        return renderLegalResearch();
      default:
        return renderDashboard();
    }
  };

  return (
    <div className="app">
      <nav className="navigation">
        <div className="nav-brand">
          <h1>Shift AI</h1>
          <span className="demo-badge">DEMO</span>
        </div>
        <ul className="nav-links">
          <li>
            <button 
              onClick={() => setCurrentView('dashboard')}
              className={currentView === 'dashboard' ? 'active' : ''}
            >
              Dashboard
            </button>
          </li>
          <li>
            <button 
              onClick={() => setCurrentView('cases')}
              className={currentView === 'cases' ? 'active' : ''}
            >
              Cases
            </button>
          </li>
          <li>
            <button 
              onClick={() => setCurrentView('legal-research')}
              className={currentView === 'legal-research' ? 'active' : ''}
            >
              Legal Research
            </button>
          </li>
        </ul>
      </nav>
      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;