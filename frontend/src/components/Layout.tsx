import { Outlet, Link, useLocation } from 'react-router-dom';
import './Layout.css';

const Layout = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <div className="layout">
      <nav className="navigation">
        <div className="nav-container">
          <div className="nav-brand">
            <Link to="/" className="brand-link">
              <h1>Shift AI Legal</h1>
              <span className="demo-badge">DEMO</span>
            </Link>
          </div>
          <ul className="nav-links">
            <li>
              <Link 
                to="/" 
                className={`nav-link ${isActive('/') ? 'active' : ''}`}
              >
                Dashboard
              </Link>
            </li>
            <li>
              <Link 
                to="/cases" 
                className={`nav-link ${isActive('/cases') ? 'active' : ''}`}
              >
                Cases
              </Link>
            </li>
            <li>
              <Link 
                to="/legal-research" 
                className={`nav-link ${isActive('/legal-research') ? 'active' : ''}`}
              >
                Legal Research
              </Link>
            </li>
          </ul>
        </div>
      </nav>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;