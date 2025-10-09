import './Cases.css';

const Cases = () => {
  return (
    <div className="cases">
      <div className="page-header">
        <div className="container">
          <h1>Case Management</h1>
          <p>Manage and analyze legal cases with AI-powered insights</p>
        </div>
      </div>

      <div className="cases-content">
        <div className="container">
          <div className="cases-grid">
            <div className="case-card">
              <div className="case-header">
                <h3>Employment Dispute - Sarah Chen</h3>
                <span className="case-status active">Active</span>
              </div>
              <div className="case-details">
                <p><strong>Case ID:</strong> CASE-001</p>
                <p><strong>Type:</strong> Employment Law</p>
                <p><strong>Priority:</strong> High</p>
                <p><strong>Documents:</strong> 3</p>
              </div>
              <div className="case-actions">
                <button className="btn-primary">View Details</button>
                <button className="btn-secondary">Generate Report</button>
              </div>
            </div>

            <div className="case-card">
              <div className="case-header">
                <h3>Software License Violation</h3>
                <span className="case-status pending">Under Review</span>
              </div>
              <div className="case-details">
                <p><strong>Case ID:</strong> CASE-002</p>
                <p><strong>Type:</strong> Intellectual Property</p>
                <p><strong>Priority:</strong> Medium</p>
                <p><strong>Documents:</strong> 4</p>
              </div>
              <div className="case-actions">
                <button className="btn-primary">View Details</button>
                <button className="btn-secondary">Generate Report</button>
              </div>
            </div>

            <div className="case-card">
              <div className="case-header">
                <h3>Contract Dispute - TechCorp</h3>
                <span className="case-status resolved">Resolved</span>
              </div>
              <div className="case-details">
                <p><strong>Case ID:</strong> CASE-003</p>
                <p><strong>Type:</strong> Contract Law</p>
                <p><strong>Priority:</strong> Low</p>
                <p><strong>Documents:</strong> 3</p>
              </div>
              <div className="case-actions">
                <button className="btn-primary">View Details</button>
                <button className="btn-secondary">Generate Report</button>
              </div>
            </div>
          </div>

          <div className="workflow-section">
            <h2>AI-Powered Case Workflow</h2>
            <div className="workflow-steps">
              <div className="workflow-step">
                <div className="step-number">1</div>
                <h4>Case Inputs</h4>
                <p>Case Evidence and Outline, Resolution Playbook, Case History</p>
              </div>
              <div className="workflow-step">
                <div className="step-number">2</div>
                <h4>Case Chronology</h4>
                <p>AI generated timeline with evidence referencing</p>
              </div>
              <div className="workflow-step">
                <div className="step-number">3</div>
                <h4>Evidence Insights</h4>
                <p>AI distills volumes of evidence into pertinent insights</p>
              </div>
              <div className="workflow-step">
                <div className="step-number">4</div>
                <h4>Validity Assessment</h4>
                <p>AI assesses each case based on playbook and processing</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cases;