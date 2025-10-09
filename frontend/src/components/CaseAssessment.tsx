import { useState, useEffect } from 'react';
import { CaseAnalysis } from '../types/api';
import './CaseAssessment.css';

interface CaseAssessmentProps {
  caseId: string;
  onRefresh?: () => void;
}

const CaseAssessment = ({ caseId, onRefresh }: CaseAssessmentProps) => {
  const [assessment, setAssessment] = useState<CaseAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchAssessment();
  }, [caseId]);

  const fetchAssessment = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`http://localhost:8000/api/cases/${caseId}/assessment`);
      if (!response.ok) {
        if (response.status === 404) {
          setAssessment(null);
          return;
        }
        throw new Error('Failed to fetch case assessment');
      }
      
      const data = await response.json();
      setAssessment(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch assessment');
    } finally {
      setLoading(false);
    }
  };

  const generateAssessment = async () => {
    try {
      setGenerating(true);
      setError(null);

      // In a real implementation, this might trigger assessment generation
      // For now, we'll just refetch the assessment
      await fetchAssessment();
      onRefresh?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate assessment');
    } finally {
      setGenerating(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'high': return 'risk-high';
      case 'medium': return 'risk-medium';
      case 'low': return 'risk-low';
      default: return 'risk-default';
    }
  };

  const getRiskIcon = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'high': return '⚠️';
      case 'medium': return '⚡';
      case 'low': return '✅';
      default: return '❓';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="case-assessment-loading">
        <div className="loading-spinner"></div>
        <p>Loading case assessment...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="case-assessment-error">
        <p>Error: {error}</p>
        <button onClick={fetchAssessment} className="btn-retry">
          Retry
        </button>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="no-assessment">
        <div className="no-assessment-content">
          <div className="no-assessment-icon">🤖</div>
          <h3>No AI Assessment Available</h3>
          <p>Generate an AI-powered assessment to analyze case strength, identify key issues, and get recommended actions.</p>
          <button 
            onClick={generateAssessment} 
            className="btn-generate"
            disabled={generating}
          >
            {generating ? 'Generating...' : 'Generate AI Assessment'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="case-assessment">
      <div className="assessment-header">
        <div className="header-content">
          <h3>AI-Generated Case Assessment</h3>
          <button 
            onClick={generateAssessment} 
            className="btn-refresh"
            disabled={generating}
            title="Refresh assessment"
          >
            {generating ? '⟳' : '↻'}
          </button>
        </div>
        {assessment.risk_assessment && (
          <div className="risk-indicator">
            <span className={`risk-badge ${getRiskColor(assessment.risk_assessment)}`}>
              <span className="risk-icon">{getRiskIcon(assessment.risk_assessment)}</span>
              <span className="risk-text">{assessment.risk_assessment} Risk</span>
            </span>
          </div>
        )}
      </div>

      <div className="assessment-content">
        {assessment.summary && (
          <div className="assessment-section summary-section">
            <h4>Executive Summary</h4>
            <div className="summary-content">
              <p>{assessment.summary}</p>
            </div>
          </div>
        )}

        {assessment.key_findings && assessment.key_findings.length > 0 && (
          <div className="assessment-section findings-section">
            <h4>Key Findings</h4>
            <div className="findings-list">
              {assessment.key_findings.map((finding, index) => (
                <div key={index} className="finding-item">
                  <div className="finding-icon">🔍</div>
                  <div className="finding-text">{finding}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {assessment.recommendations && assessment.recommendations.length > 0 && (
          <div className="assessment-section recommendations-section">
            <h4>Recommended Actions</h4>
            <div className="recommendations-list">
              {assessment.recommendations.map((recommendation, index) => (
                <div key={index} className="recommendation-item">
                  <div className="recommendation-number">{index + 1}</div>
                  <div className="recommendation-content">
                    <div className="recommendation-text">{recommendation}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="assessment-metrics">
          {assessment.estimated_value && (
            <div className="metric-card value-metric">
              <div className="metric-header">
                <h5>Estimated Case Value</h5>
                <div className="metric-icon">💰</div>
              </div>
              <div className="metric-value">
                <span className="value-amount">
                  {formatCurrency(assessment.estimated_value)}
                </span>
              </div>
              <div className="metric-description">
                Based on case strength and comparable outcomes
              </div>
            </div>
          )}

          {assessment.risk_assessment && (
            <div className="metric-card risk-metric">
              <div className="metric-header">
                <h5>Risk Assessment</h5>
                <div className="metric-icon">{getRiskIcon(assessment.risk_assessment)}</div>
              </div>
              <div className="metric-value">
                <span className={`risk-level ${getRiskColor(assessment.risk_assessment)}`}>
                  {assessment.risk_assessment}
                </span>
              </div>
              <div className="metric-description">
                Overall risk level for this case
              </div>
            </div>
          )}
        </div>

        {assessment.timeline && assessment.timeline.length > 0 && (
          <div className="assessment-section timeline-section">
            <h4>Case Timeline</h4>
            <div className="timeline-container">
              {assessment.timeline.map((event, index) => (
                <div key={index} className="timeline-event">
                  <div className="timeline-marker">
                    <div className="timeline-dot"></div>
                    {index < assessment.timeline!.length - 1 && (
                      <div className="timeline-line"></div>
                    )}
                  </div>
                  <div className="timeline-content">
                    <div className="timeline-date">
                      {new Date(event.date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric'
                      })}
                    </div>
                    <div className="timeline-event-title">{event.event}</div>
                    <div className="timeline-description">{event.description}</div>
                    {event.document_reference && (
                      <div className="timeline-reference">
                        📄 Reference: {event.document_reference}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="assessment-footer">
        <div className="assessment-disclaimer">
          <p>
            <strong>Disclaimer:</strong> This AI-generated assessment is for informational purposes only 
            and should not be considered as legal advice. Please consult with qualified legal professionals 
            for case-specific guidance.
          </p>
        </div>
        <div className="assessment-actions">
          <button className="btn-export" disabled>
            Export Report
          </button>
          <button className="btn-share" disabled>
            Share Assessment
          </button>
        </div>
      </div>
    </div>
  );
};

export default CaseAssessment;