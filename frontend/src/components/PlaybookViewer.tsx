import { useState, useEffect } from 'react';
import { Playbook, PlaybookResult } from '../types/api';


interface PlaybookViewerProps {
  caseType: string;
  caseId?: string;
  showAppliedRules?: boolean;
}

const PlaybookViewer = ({ caseType, caseId, showAppliedRules = false }: PlaybookViewerProps) => {
  const [playbook, setPlaybook] = useState<Playbook | null>(null);
  const [appliedRules, setAppliedRules] = useState<PlaybookResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedRules, setExpandedRules] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchPlaybookData();
  }, [caseType, caseId]);

  const fetchPlaybookData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch playbook for case type
      const playbookResponse = await fetch(`http://localhost:8000/api/playbooks/${encodeURIComponent(caseType)}`);
      if (!playbookResponse.ok) {
        throw new Error('Failed to fetch playbook');
      }
      const playbookData = await playbookResponse.json();
      setPlaybook(playbookData);

      // Fetch applied rules if case ID is provided and showAppliedRules is true
      if (caseId && showAppliedRules) {
        try {
          const rulesResponse = await fetch(`http://localhost:8000/api/playbooks/cases/${caseId}/applied-rules`);
          if (rulesResponse.ok) {
            const rulesData = await rulesResponse.json();
            setAppliedRules(rulesData);
          }
        } catch (err) {
          console.warn('Could not fetch applied rules:', err);
        }
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch playbook data');
    } finally {
      setLoading(false);
    }
  };

  const toggleRuleExpansion = (ruleId: string) => {
    const newExpanded = new Set(expandedRules);
    if (newExpanded.has(ruleId)) {
      newExpanded.delete(ruleId);
    } else {
      newExpanded.add(ruleId);
    }
    setExpandedRules(newExpanded);
  };

  const isRuleApplied = (ruleId: string) => {
    return appliedRules?.applied_rules?.includes(ruleId) || false;
  };

  const getRuleWeight = (weight: number) => {
    if (weight >= 0.8) return 'weight-high';
    if (weight >= 0.5) return 'weight-medium';
    return 'weight-low';
  };

  const getStrengthColor = (strength: string) => {
    switch (strength?.toLowerCase()) {
      case 'strong': return 'strength-strong';
      case 'moderate': return 'strength-moderate';
      case 'weak': return 'strength-weak';
      default: return 'strength-default';
    }
  };

  if (loading) {
    return (
      <div className="playbook-viewer-loading">
        <div className="loading-spinner"></div>
        <p>Loading playbook...</p>
      </div>
    );
  }

  if (error || !playbook) {
    return (
      <div className="playbook-viewer-error">
        <p>Error: {error || 'Playbook not found'}</p>
        <button onClick={fetchPlaybookData} className="btn-retry">Retry</button>
      </div>
    );
  }

  return (
    <div className="playbook-viewer">
      <div className="playbook-header">
        <div className="playbook-title-section">
          <h2>{playbook.name}</h2>
          <p className="playbook-description">{playbook.description}</p>
          <div className="playbook-meta">
            <span className="case-type-badge">{caseType}</span>
            <span className="rules-count">{playbook.rules?.length || 0} Rules</span>
          </div>
        </div>
      </div>

      {showAppliedRules && appliedRules && (
        <div className="applied-rules-summary">
          <h3>Applied to Current Case</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="summary-label">Case Strength</span>
              <span className={`summary-value strength-badge ${getStrengthColor(appliedRules.case_strength || '')}`}>
                {appliedRules.case_strength || 'Unknown'}
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Applied Rules</span>
              <span className="summary-value">{appliedRules.applied_rules?.length || 0}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Recommendations</span>
              <span className="summary-value">{appliedRules.recommendations?.length || 0}</span>
            </div>
          </div>
          {appliedRules.reasoning && (
            <div className="reasoning-section">
              <h4>AI Reasoning</h4>
              <p className="reasoning-text">{appliedRules.reasoning}</p>
            </div>
          )}
        </div>
      )}

      <div className="playbook-content">
        <div className="rules-section">
          <div className="section-header">
            <h3>Decision Rules</h3>
            <p>Rules and conditions that guide case assessment and recommendations</p>
          </div>

          {playbook.rules && playbook.rules.length > 0 ? (
            <div className="rules-list">
              {playbook.rules.map((rule) => (
                <div 
                  key={rule.id} 
                  className={`rule-card ${isRuleApplied(rule.id) ? 'rule-applied' : ''} ${!rule.enabled ? 'rule-disabled' : ''}`}
                >
                  <div className="rule-header" onClick={() => toggleRuleExpansion(rule.id)}>
                    <div className="rule-title-section">
                      <div className="rule-id-section">
                        <span className="rule-id">{rule.id}</span>
                        {isRuleApplied(rule.id) && (
                          <span className="applied-indicator">Applied</span>
                        )}
                      </div>
                      <div className="rule-status-section">
                        <span className={`rule-weight ${getRuleWeight(rule.priority || 0)}`}>
                          Weight: {((rule.priority || 0) * 100).toFixed(0)}%
                        </span>
                        <span className={`rule-status ${rule.enabled ? 'enabled' : 'disabled'}`}>
                          {rule.enabled ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                    </div>
                    <div className="expand-icon">
                      {expandedRules.has(rule.id) ? '−' : '+'}
                    </div>
                  </div>

                  {expandedRules.has(rule.id) && (
                    <div className="rule-details">
                      <div className="rule-description">
                        <h5>Description</h5>
                        <p>{rule.description}</p>
                      </div>
                      <div className="rule-condition">
                        <h5>Condition</h5>
                        <p>{rule.condition}</p>
                      </div>
                      <div className="rule-action">
                        <h5>Action</h5>
                        <p>{rule.action}</p>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-rules">
              <p>No rules defined for this playbook.</p>
            </div>
          )}
        </div>

        {showAppliedRules && appliedRules?.recommendations && appliedRules.recommendations.length > 0 && (
          <div className="recommendations-section">
            <div className="section-header">
              <h3>Generated Recommendations</h3>
              <p>Actions recommended based on applied rules</p>
            </div>
            <div className="recommendations-list">
              {appliedRules.recommendations.map((recommendation, index) => (
                <div key={index} className="recommendation-item">
                  <div className="recommendation-icon">→</div>
                  <div className="recommendation-text">{recommendation}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {playbook.decision_tree && Object.keys(playbook.decision_tree).length > 0 && (
          <div className="decision-tree-section">
            <div className="section-header">
              <h3>Decision Tree</h3>
              <p>Visual representation of the decision-making process</p>
            </div>
            <div className="decision-tree">
              <pre className="tree-visualization">
                {JSON.stringify(playbook.decision_tree, null, 2)}
              </pre>
            </div>
          </div>
        )}

        {playbook.monetary_ranges && Object.keys(playbook.monetary_ranges).length > 0 && (
          <div className="monetary-section">
            <div className="section-header">
              <h3>Monetary Assessment Ranges</h3>
              <p>Expected value ranges based on case strength</p>
            </div>
            <div className="monetary-ranges">
              {Object.entries(playbook.monetary_ranges).map(([strength, data]: [string, any]) => (
                <div key={strength} className="monetary-range">
                  <div className="range-header">
                    <span className={`strength-label ${getStrengthColor(strength)}`}>
                      {strength.charAt(0).toUpperCase() + strength.slice(1)} Cases
                    </span>
                  </div>
                  <div className="range-values">
                    {data.range && (
                      <span className="range-text">
                        ${data.range[0]?.toLocaleString()} - ${data.range[1]?.toLocaleString()}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {playbook.escalation_paths && playbook.escalation_paths.length > 0 && (
          <div className="escalation-section">
            <div className="section-header">
              <h3>Escalation Paths</h3>
              <p>Recommended escalation procedures for different scenarios</p>
            </div>
            <div className="escalation-paths">
              {playbook.escalation_paths.map((path, index) => (
                <div key={index} className="escalation-path">
                  <div className="path-step">{index + 1}</div>
                  <div className="path-description">{path}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlaybookViewer;