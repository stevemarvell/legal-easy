import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Case } from '../types/api';
import './CaseList.css';

interface CaseListProps {
  onCaseSelect?: (caseId: string) => void;
}

const CaseList = ({ onCaseSelect }: CaseListProps) => {
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterType, setFilterType] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchCases();
  }, []);

  const fetchCases = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/cases');
      if (!response.ok) {
        throw new Error('Failed to fetch cases');
      }
      const data = await response.json();
      setCases(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch cases');
    } finally {
      setLoading(false);
    }
  };

  const filteredCases = cases.filter(case_ => {
    const matchesType = filterType === 'all' || case_.case_type === filterType;
    const matchesSearch = case_.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (case_.summary || case_.description || '').toLowerCase().includes(searchTerm.toLowerCase());
    return matchesType && matchesSearch;
  });

  const uniqueCaseTypes = Array.from(new Set(cases.map(case_ => case_.case_type)));

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active': return 'status-active';
      case 'pending': return 'status-pending';
      case 'resolved': return 'status-resolved';
      case 'closed': return 'status-closed';
      default: return 'status-default';
    }
  };

  const getPriorityColor = (priority?: string) => {
    if (!priority) return 'priority-default';
    switch (priority.toLowerCase()) {
      case 'critical': return 'priority-critical';
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return 'priority-default';
    }
  };

  if (loading) {
    return (
      <div className="case-list-loading">
        <div className="loading-spinner"></div>
        <p>Loading cases...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="case-list-error">
        <p>Error: {error}</p>
        <button onClick={fetchCases} className="btn-retry">Retry</button>
      </div>
    );
  }

  return (
    <div className="case-list">
      <div className="case-list-header">
        <h1>Legal Cases</h1>
        <p>Manage and analyze legal cases with AI-powered insights</p>
      </div>

      <div className="case-list-filters">
        <div className="search-filter">
          <input
            type="text"
            placeholder="Search cases..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="type-filter">
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Case Types</option>
            {uniqueCaseTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="case-list-stats">
        <div className="stat-item">
          <span className="stat-number">{cases.length}</span>
          <span className="stat-label">Total Cases</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">{cases.filter(c => c.status === 'Active').length}</span>
          <span className="stat-label">Active</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">{cases.filter(c => c.status === 'Under Review').length}</span>
          <span className="stat-label">Under Review</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">{cases.filter(c => c.status === 'Resolved').length}</span>
          <span className="stat-label">Resolved</span>
        </div>
      </div>

      <div className="cases-grid">
        {filteredCases.map((case_) => (
          <div key={case_.id} className="case-card">
            <div className="case-card-header">
              <h3 className="case-title">{case_.title}</h3>
              <div className="case-badges">
                <span className={`status-badge ${getStatusColor(case_.status)}`}>
                  {case_.status}
                </span>
                <span className={`priority-badge ${getPriorityColor(case_.priority)}`}>
                  {case_.priority}
                </span>
              </div>
            </div>

            <div className="case-card-body">
              <p className="case-description">{case_.summary || case_.description || 'No description available'}</p>
              
              <div className="case-meta">
                <div className="meta-item">
                  <span className="meta-label">Case ID:</span>
                  <span className="meta-value">{case_.id}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Type:</span>
                  <span className="meta-value">{case_.case_type}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Created:</span>
                  <span className="meta-value">
                    {new Date(case_.created_date || case_.created_at || '').toLocaleDateString()}
                  </span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Documents:</span>
                  <span className="meta-value">{case_.documents?.length || 0}</span>
                </div>
              </div>
            </div>

            <div className="case-card-actions">
              <Link 
                to={`/cases/${case_.id}`} 
                className="btn-primary"
                onClick={() => onCaseSelect?.(case_.id)}
              >
                View Details
              </Link>
              <Link 
                to={`/cases/${case_.id}/documents`} 
                className="btn-secondary"
              >
                Documents
              </Link>
            </div>
          </div>
        ))}
      </div>

      {filteredCases.length === 0 && (
        <div className="no-cases">
          <p>No cases found matching your criteria.</p>
        </div>
      )}
    </div>
  );
};

export default CaseList;