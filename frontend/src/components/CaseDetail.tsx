import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Case } from '../types/api';
import PlaybookViewer from './PlaybookViewer';
import CaseAssessment from './CaseAssessment';
import Button from './Button';
import './CaseDetail.css';

const CaseDetail = () => {
  const { caseId } = useParams<{ caseId: string }>();
  const [case_, setCase] = useState<Case | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'info' | 'playbook' | 'assessment'>('info');

  useEffect(() => {
    if (caseId) {
      fetchCaseData();
    }
  }, [caseId]);

  const fetchCaseData = async () => {
    if (!caseId) return;

    try {
      setLoading(true);
      setError(null);

      // Fetch case details
      const caseResponse = await fetch(`http://localhost:8000/api/cases/${caseId}`);
      if (!caseResponse.ok) {
        throw new Error('Failed to fetch case details');
      }
      const caseData = await caseResponse.json();
      setCase(caseData);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch case data');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active': return 'status-active';
      case 'under review': return 'status-pending';
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
      <div className="case-detail-loading">
        <div className="loading-spinner"></div>
        <p>Loading case details...</p>
      </div>
    );
  }

  if (error || !case_) {
    return (
      <div className="case-detail-error">
        <p>Error: {error || 'Case not found'}</p>
        <Link to="/cases" className="btn-back">Back to Cases</Link>
      </div>
    );
  }

  return (
    <div className="case-detail">
      <div className="case-detail-header">
        <div className="header-navigation">
          <Link to="/cases" className="back-link">← Back to Cases</Link>
        </div>
        
        <div className="header-content">
          <div className="case-title-section">
            <h1 className="case-title">{case_.title}</h1>
            <div className="case-badges">
              <span className={`status-badge ${getStatusColor(case_.status)}`}>
                {case_.status}
              </span>
              {case_.priority && (
                <span className={`priority-badge ${getPriorityColor(case_.priority)}`}>
                  {case_.priority}
                </span>
              )}
            </div>
          </div>
          
          <div className="case-meta-grid">
            <div className="meta-item">
              <span className="meta-label">Case ID</span>
              <span className="meta-value">{case_.id}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Case Type</span>
              <span className="meta-value">{case_.case_type}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Created</span>
              <span className="meta-value">
                {new Date(case_.created_date).toLocaleDateString()}
              </span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Client</span>
              <span className="meta-value">{case_.client_name}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="case-detail-tabs">
        <button
          className={`tab-button ${activeTab === 'info' ? 'active' : ''}`}
          onClick={() => setActiveTab('info')}
          data-testid="info-tab"
        >
          Case Information
        </button>
        <button
          className={`tab-button ${activeTab === 'playbook' ? 'active' : ''}`}
          onClick={() => setActiveTab('playbook')}
          data-testid="playbook-tab"
        >
          Playbook
        </button>
        <button
          className={`tab-button ${activeTab === 'assessment' ? 'active' : ''}`}
          onClick={() => setActiveTab('assessment')}
          data-testid="assessment-tab"
        >
          AI Assessment
        </button>
      </div>

      <div className="case-detail-content">
        {activeTab === 'info' && (
          <div className="tab-content">
            <div className="info-section">
              <h3>Case Summary</h3>
              <p className="case-description">{case_.summary}</p>
            </div>

            <div className="info-section">
              <h3>Key Parties</h3>
              <div className="parties-list">
                {case_.key_parties && case_.key_parties.length > 0 ? (
                  case_.key_parties.map((party, index) => (
                    <div key={index} className="party-item">
                      <span className="party-name">{party}</span>
                    </div>
                  ))
                ) : (
                  <p className="no-parties">No parties listed.</p>
                )}
              </div>
            </div>

            <div className="info-section">
              <h3>Documents ({case_.documents?.length || 0})</h3>
              <div className="documents-list">
                {case_.documents && case_.documents.length > 0 ? (
                  case_.documents.map((docId) => (
                    <div key={docId} className="document-item">
                      <div className="document-info">
                        <span className="document-name">Document {docId}</span>
                        <span className="document-meta">
                          Legal Document
                        </span>
                      </div>
                      <span className="analysis-status completed">
                        Analyzed
                      </span>
                    </div>
                  ))
                ) : (
                  <p className="no-documents">No documents uploaded yet.</p>
                )}
              </div>
              <Link to={`/cases/${caseId}/documents`} className="btn-secondary">
                View Documents
              </Link>
            </div>
          </div>
        )}

        {activeTab === 'playbook' && (
          <div className="tab-content">
            <PlaybookViewer 
              caseType={case_.case_type} 
              caseId={caseId}
              showAppliedRules={true}
            />
          </div>
        )}

        {activeTab === 'assessment' && (
          <div className="tab-content">
            <CaseAssessment 
              caseId={caseId!} 
              onRefresh={fetchCaseData}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default CaseDetail;