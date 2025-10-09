import { useState, useEffect } from 'react';
import { CaseAssessment as CaseAssessmentType } from '../types/api';


interface CaseAssessmentProps {
  caseId: string;
  onRefresh?: () => void;
}

const CaseAssessment = ({ caseId, onRefresh }: CaseAssessmentProps) => {
  const [assessment, setAssessment] = useState<CaseAssessmentType | null>(null);
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

  const getCaseStrengthColor = (strength: string) => {
    switch (strength.toLowerCase()) {
      case 'strong': return 'strength-strong';
      case 'moderate': return 'strength-moderate';
      case 'weak': return 'strength-weak';
      default: return 'strength-default';
    }
  };

  const getCaseStrengthIcon = (strength: string) => {
    switch (strength.toLowerCase()) {
      case 'strong': return '💪';
      case 'moderate': return '⚖️';
      case 'weak': return '⚠️';
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
        {assessment.case_strength && (
          <div className="strength-indicator">
            <span className={`strength-badge ${getCaseStrengthColor(assessment.case_strength)}`}>
              <span className="strength-icon">{getCaseStrengthIcon(assessment.case_strength)}</span>
              <span className="strength-text">{assessment.case_strength} Case</span>
            </span>
          </div>
        )}
      </div>

      <div className="assessment-content">
        {assessment.reasoning && (
          <div className="assessment-section summary-section">
            <h4>Assessment Summary</h4>
            <div className="summary-content">
              <p>{assessment.reasoning}</p>
            </div>
          </div>
        )}

        {assessment.key_issues && assessment.key_issues.length > 0 && (
          <div className="assessment-section issues-section">
            <h4>Key Issues Identified</h4>
            <div className="issues-list">
              {assessment.key_issues.map((issue, index) => (
                <div key={index} className="issue-item">
                  <div className="issue-icon">⚖️</div>
                  <div className="issue-text">{issue}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {assessment.recommended_actions && assessment.recommended_actions.length > 0 && (
          <div className="assessment-section recommendations-section">
            <h4>Recommended Actions</h4>
            <div className="recommendations-list">
              {assessment.recommended_actions.map((action, index) => (
                <div key={index} className="recommendation-item">
                  <div className="recommendation-number">{index + 1}</div>
                  <div className="recommendation-content">
                    <div className="recommendation-text">{action}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="assessment-metrics">
          {assessment.monetary_assessment && (
            <div className="metric-card value-metric">
              <div className="metric-header">
                <h5>Monetary Assessment Range</h5>
                <div className="metric-icon">💰</div>
              </div>
              <div className="metric-value">
                <span className="value-range">
                  {formatCurrency(assessment.monetary_assessment[0])} - {formatCurrency(assessment.monetary_assessment[1])}
                </span>
              </div>
              <div className="metric-description">
                Estimated range based on case strength and comparable outcomes
              </div>
            </div>
          )}

          {assessment.case_strength && (
            <div className="metric-card strength-metric">
              <div className="metric-header">
                <h5>Case Strength</h5>
                <div className="metric-icon">{getCaseStrengthIcon(assessment.case_strength)}</div>
              </div>
              <div className="metric-value">
                <span className={`strength-level ${getCaseStrengthColor(assessment.case_strength)}`}>
                  {assessment.case_strength}
                </span>
              </div>
              <div className="metric-description">
                Overall assessment based on {assessment.playbook_used}
              </div>
            </div>
          )}
        </div>

        {assessment.applied_rules && assessment.applied_rules.length > 0 && (
          <div className="assessment-section rules-section">
            <h4>Applied Playbook Rules</h4>
            <div className="rules-info">
              <p className="playbook-name">
                <strong>Playbook Used:</strong> {assessment.playbook_used}
              </p>
              <div className="applied-rules-list">
                {assessment.applied_rules.map((ruleId, index) => (
                  <span key={index} className="rule-tag">
                    {ruleId}
                  </span>
                ))}
              </div>
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