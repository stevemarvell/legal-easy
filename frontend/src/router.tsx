import { createBrowserRouter } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard/Dashboard';
import Cases from './components/Cases';
import LegalResearch from './components/LegalResearch';
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
        element: <Cases />, // Cases component should handle documents view
      },
      {
        path: 'legal-research',
        element: <LegalResearch />,
      },
    ],
  },
]);