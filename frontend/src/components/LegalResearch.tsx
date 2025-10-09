import './LegalResearch.css';

const LegalResearch = () => {
  return (
    <div className="legal-research">
      <div className="page-header">
        <div className="container">
          <h1>Legal Research</h1>
          <p>Extract valuable insights from large volumes of legal documentation</p>
        </div>
      </div>

      <div className="research-content">
        <div className="container">
          <div className="search-section">
            <div className="search-box">
              <input 
                type="text" 
                placeholder="Search legal documents, cases, or ask a question..."
                className="search-input"
              />
              <button className="search-button">Search</button>
            </div>
          </div>

          <div className="research-tools">
            <div className="tool-card">
              <div className="tool-icon">📄</div>
              <h3>Document Analysis</h3>
              <p>Upload and analyze legal documents with AI-powered extraction</p>
              <button className="tool-button">Upload Documents</button>
            </div>

            <div className="tool-card">
              <div className="tool-icon">🔍</div>
              <h3>Case Law Search</h3>
              <p>Search through precedents and case law with intelligent matching</p>
              <button className="tool-button">Search Cases</button>
            </div>

            <div className="tool-card">
              <div className="tool-icon">📊</div>
              <h3>Legal Analytics</h3>
              <p>Generate insights and reports from your legal data</p>
              <button className="tool-button">View Analytics</button>
            </div>
          </div>

          <div className="intelligence-workflow">
            <h2>Shift Intelligence Workflow</h2>
            <div className="workflow-grid">
              <div className="workflow-item">
                <div className="workflow-icon">📥</div>
                <h4>Inputs</h4>
                <p>Digital Documents, Scanned Documents, Forms, Images, Databases</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">⚙️</div>
                <h4>Processing</h4>
                <p>Multi-modal models read, clean and convert into usable formats</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">🏷️</div>
                <h4>Classification</h4>
                <p>Documents are vectorised and classified according to content</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">🔗</div>
                <h4>Versioning</h4>
                <p>Relationship mapping across documents links and visualised connections</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">📤</div>
                <h4>Extractions</h4>
                <p>AI answers questions on each document, extracting verbatim and using advanced reasoning</p>
              </div>
              <div className="workflow-item">
                <div className="workflow-icon">✅</div>
                <h4>Validation</h4>
                <p>Extracted data is validated using AI and external data sources for quality</p>
              </div>
            </div>
          </div>

          <div className="recent-research">
            <h3>Recent Research</h3>
            <div className="research-list">
              <div className="research-item">
                <h4>Employment Law Precedents Analysis</h4>
                <p>Analysis of recent employment law cases and their implications</p>
                <span className="research-date">2 hours ago</span>
              </div>
              <div className="research-item">
                <h4>Contract Clause Extraction</h4>
                <p>Extracted key clauses from 15 service agreements</p>
                <span className="research-date">1 day ago</span>
              </div>
              <div className="research-item">
                <h4>Regulatory Compliance Review</h4>
                <p>Comprehensive review of new data protection regulations</p>
                <span className="research-date">3 days ago</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LegalResearch;