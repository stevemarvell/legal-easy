import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Shift AI activates efficiency and productivity opportunities in legal enterprises
          </h1>
          <p className="hero-subtitle">
            Fusing the power of your expertise and Agentic AI to do more faster, better and safer.
          </p>
        </div>
      </div>

      <div className="features-section">
        <div className="container">
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Shift</h3>
              <p>How you work by unlocking the power of Agentic AI.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Alt</h3>
              <p>The quality of your decisions with the power of possible.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⏰</div>
              <h3>Esc</h3>
              <p>Time sinks and spiralling costs with smarter working.</p>
            </div>
          </div>
        </div>
      </div>

      <div className="products-section">
        <div className="container">
          <h2 className="section-title">You're in Shift</h2>
          <p className="section-subtitle">
            Shift AI is a suite of Agentic AI tools that supercharge how enterprises 
            interrogate large volumes of data and manage legal disputes to a smarter resolution.
          </p>
          
          <div className="products-grid">
            <div className="product-card">
              <h3>Shift Disputes</h3>
              <p>
                AI-powered platform to assess legal cases using evidence and playbooks, 
                recommending case strategy and drafting relevant documentation.
              </p>
              <ul>
                <li>Ensures efficient and consistent assessment of claims</li>
                <li>Reviews evidence quickly to assess relevance and validity</li>
                <li>Suggests optimal remedial actions based on case facts</li>
                <li>Recommends monetary values to be assigned to claims</li>
              </ul>
              <button className="cta-button">Explore Cases</button>
            </div>
            
            <div className="product-card">
              <h3>Shift Intelligence</h3>
              <p>
                AI-powered platform to extract valuable data and insights from large volumes 
                of documentation, enabling smart decision-making and operational savings.
              </p>
              <ul>
                <li>Extracts key data across multiple documents and formats</li>
                <li>Simplifies large volumes of information</li>
                <li>Presents data in easily consumable formats</li>
                <li>Identifies issues, risks and next steps</li>
              </ul>
              <button className="cta-button">Start Research</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;