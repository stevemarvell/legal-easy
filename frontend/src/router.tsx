import { createBrowserRouter } from 'react-router-dom';
import Layout from './pages/Layout';
import Dashboard from './pages/Dashboard';
import Cases from './pages/Cases';
import Documents from './pages/Documents';
import Playbooks from './pages/Playbooks';
import Documentation from './pages/Documentation';
import Research from './pages/Research';
import Admin from './pages/Admin';
import ErrorBoundary from './components/ErrorBoundary';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <ErrorBoundary />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'cases',
        element: <Cases />,
      },
      {
        path: 'cases/:caseId',
        element: <Cases />, // Cases component should handle individual case view
      },
      {
        path: 'cases/:caseId/documents',
        element: <Documents />, // Dedicated Documents page
      },
      {
        path: 'playbooks',
        element: <Playbooks />,
      },
      {
        path: 'playbooks/:caseType',
        element: <Playbooks />, // Playbooks component handles individual playbook view
      },
      {
        path: 'docs',
        element: <Documentation />,
      },
      {
        path: 'docs/:section',
        element: <Documentation />,
      },
      {
        path: 'research',
        element: <Research />,
      },
      {
        path: 'admin',
        element: <Admin />,
      },
    ],
  },
]);