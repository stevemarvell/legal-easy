import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import { Case } from '../types/api';
import './Dashboard.css';

interface CaseStatistics {
  total_cases: number;
  active_cases: number;
  resolved_cases: number;
  under_review_cases: number;
  recent_activity_count: number;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [statistics, setStatistics] = useState<CaseStatistics | null>(null);
  const [recentCases, setRecentCases] = useState<Case[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch case statistics
        const statsResponse = await apiClient.get<CaseStatistics>('/api/cases/statistics');
        setStatistics(statsResponse.data);

        // Fetch recent cases (all cases for now, we'll show the most recent ones)
        const casesResponse = await apiClient.get<Case[]>('/api/cases');
        const sortedCases = casesResponse.data
          .sort((a, b) => new Date(b.updated_at || b.created_at).getTime() - new Date(a.updated_at || a.created_at).getTime())
          .slice(0, 5); // Show 5 most recent cases
        setRecentCases(sortedCases);
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/legal-research?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleCaseClick = (caseId: string) => {
    navigate(`/cases/${caseId}`);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return '#10b981'; // green
      case 'under review':
        return '#f59e0b'; // amber
      case 'resolved':
        return '#6b7280'; // gray
      case 'pending':
        return '#3b82f6'; // blue
      default:
        return '#6b7280';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
      case 'critical':
        return '#ef4444'; // red
      case 'medium':
        return '#f59e0b'; // amber
      case 'low':
        return '#10b981'; // green
      default:
        return '#6b7280';
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="dashboard-loading">
          <div className="loading-spinner" data-testid="loading-spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="dashboard-error">
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Demo Environment Banner */}
      <div className="demo-banner">
        <div className="demo-content">
          <span className="demo-badge">DEMO</span>
          <p>Shift Legal AI Demo - Explore implemented features with sample legal case data</p>
        </div>
      </div>

      {/* Header Section */}
      <div className="dashboard-header">
        <div className="container">
          <h1 className="dashboard-title">Shift Legal AI Dashboard</h1>
          <p className="dashboard-subtitle">
            Intelligent case management and legal research platform
          </p>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="statistics-section">
        <div className="container">
          <div className="statistics-grid">
            <div className="stat-card">
              <div className="stat-icon">📊</div>
              <div className="stat-content">
                <h3 className="stat-number">{statistics?.total_cases || 0}</h3>
                <p className="stat-label">Total Cases</p>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">⚡</div>
              <div className="stat-content">
                <h3 className="stat-number">{statistics?.active_cases || 0}</h3>
                <p className="stat-label">Active Cases</p>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">👁️</div>
              <div className="stat-content">
                <h3 className="stat-number">{statistics?.under_review_cases || 0}</h3>
                <p className="stat-label">Under Review</p>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">✅</div>
              <div className="stat-content">
                <h3 className="stat-number">{statistics?.resolved_cases || 0}</h3>
                <p className="stat-label">Resolved</p>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">📈</div>
              <div className="stat-content">
                <h3 className="stat-number">{statistics?.recent_activity_count || 0}</h3>
                <p className="stat-label">Recent Activity</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Legal Research Search */}
      <div className="search-section">
        <div className="container">
          <div className="search-card">
            <h2 className="search-title">Legal Research</h2>
            <p className="search-subtitle">
              Search through legal precedents, statutes, and case law with semantic search
            </p>
            <form onSubmit={handleSearchSubmit} className="search-form">
              <div className="search-input-group">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search legal documents, precedents, statutes..."
                  className="search-input"
                />
                <button type="submit" className="search-button" disabled={!searchQuery.trim()}>
                  <span className="search-icon">🔍</span>
                  Search
                </button>
              </div>
            </form>
            <div className="search-suggestions">
              <p>Try searching for:</p>
              <div className="suggestion-tags">
                <button 
                  className="suggestion-tag"
                  onClick={() => setSearchQuery('employment termination')}
                >
                  employment termination
                </button>
                <button 
                  className="suggestion-tag"
                  onClick={() => setSearchQuery('contract breach')}
                >
                  contract breach
                </button>
                <button 
                  className="suggestion-tag"
                  onClick={() => setSearchQuery('intellectual property')}
                >
                  intellectual property
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Cases */}
      <div className="recent-cases-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Recent Cases</h2>
            <button 
              className="view-all-button"
              onClick={() => navigate('/cases')}
            >
              View All Cases
            </button>
          </div>
          
          <div className="cases-grid">
            {recentCases.map((case_) => (
              <div 
                key={case_.id} 
                className="case-card"
                onClick={() => handleCaseClick(case_.id)}
              >
                <div className="case-header">
                  <h3 className="case-title">{case_.title}</h3>
                  <div className="case-badges">
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(case_.status) }}
                    >
                      {case_.status}
                    </span>
                    {case_.priority && (
                      <span 
                        className="priority-badge"
                        style={{ backgroundColor: getPriorityColor(case_.priority) }}
                      >
                        {case_.priority}
                      </span>
                    )}
                  </div>
                </div>
                
                <p className="case-description">{case_.description}</p>
                
                <div className="case-meta">
                  <div className="case-type">
                    <span className="meta-label">Type:</span>
                    <span className="meta-value">{case_.case_type}</span>
                  </div>
                  <div className="case-date">
                    <span className="meta-label">Updated:</span>
                    <span className="meta-value">
                      {new Date(case_.updated_at || case_.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                
                <div className="case-actions">
                  <button 
                    className="action-button primary"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleCaseClick(case_.id);
                    }}
                  >
                    View Details
                  </button>
                  <button 
                    className="action-button secondary"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/cases/${case_.id}/documents`);
                    }}
                  >
                    Documents
                  </button>
                </div>
              </div>
            ))}
          </div>
          
          {recentCases.length === 0 && (
            <div className="empty-state">
              <p>No recent cases found.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;