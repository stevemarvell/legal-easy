import { useState } from 'react';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');

  return (
    <div className="app">
      <nav className="navigation">
        <div className="nav-brand">
          <h1>AI Legal Platform</h1>
          <span className="demo-badge">DEMO</span>
        </div>
        <ul className="nav-links">
          <li>
            <button onClick={() => setCurrentView('dashboard')}>
              Dashboard
            </button>
          </li>
          <li>
            <button onClick={() => setCurrentView('cases')}>
              Cases
            </button>
          </li>
          <li>
            <button onClick={() => setCurrentView('legal-research')}>
              Legal Research
            </button>
          </li>
        </ul>
      </nav>
      <main className="main-content">
        <div>
          <h1>Legal Platform Dashboard</h1>
          <p>Current view: {currentView}</p>
          <p>Project structure setup complete</p>
        </div>
      </main>
    </div>
  );
}

export default App;