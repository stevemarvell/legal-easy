import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '../../test-utils';
import { apiClient } from '../../services/api';
import Dashboard from '../Dashboard';

// Mock the API client
vi.mock('../../services/api', () => ({
  apiClient: {
    get: vi.fn(),
  },
}));

// Mock react-router-dom navigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('Dashboard Component', () => {
  const mockStatistics = {
    total_cases: 6,
    active_cases: 3,
    resolved_cases: 1,
    under_review_cases: 2,
    recent_activity_count: 4,
  };

  const mockCases = [
    {
      id: 'case-001',
      title: 'Employment Dispute - Sarah Chen',
      description: 'Unfair dismissal case involving safety violations',
      status: 'active',
      priority: 'high',
      case_type: 'Employment Law',
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-20T14:30:00Z',
    },
    {
      id: 'case-002',
      title: 'Software License Violation',
      description: 'Intellectual property dispute over software licensing',
      status: 'pending',
      priority: 'medium',
      case_type: 'Intellectual Property',
      created_at: '2024-01-10T09:00:00Z',
      updated_at: '2024-01-18T16:45:00Z',
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    // Mock successful API responses by default
    (apiClient.get as any).mockImplementation((endpoint: string) => {
      if (endpoint === '/api/cases/statistics') {
        return Promise.resolve({ data: mockStatistics });
      }
      if (endpoint === '/api/cases') {
        return Promise.resolve({ data: mockCases });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('Initial Render and Loading', () => {
    it('shows loading state initially', () => {
      render(<Dashboard />);
      
      expect(screen.getByText('Loading dashboard...')).toBeInTheDocument();
      expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
    });

    it('displays demo banner', async () => {
      render(<Dashboard />);
      
      await waitFor(() => {
        expect(screen.getByText('DEMO')).toBeInTheDocument();
        expect(screen.getByText(/Shift Legal AI Demo - Explore implemented features/)).toBeInTheDocument();
      });
    });
  });

  describe('Case Statistics Display', () => {
    it('displays case statistics cards correctly', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        expect(screen.getByText('6')).toBeInTheDocument(); // Total cases
        expect(screen.getByText('3')).toBeInTheDocument(); // Active cases
        expect(screen.getByText('2')).toBeInTheDocument(); // Under review
        expect(screen.getByText('1')).toBeInTheDocument(); // Resolved
        expect(screen.getByText('4')).toBeInTheDocument(); // Recent activity
      });

      expect(screen.getByText('Total Cases')).toBeInTheDocument();
      expect(screen.getByText('Active Cases')).toBeInTheDocument();
      expect(screen.getByText('Under Review')).toBeInTheDocument();
      expect(screen.getByText('Resolved')).toBeInTheDocument();
      expect(screen.getByText('Recent Activity')).toBeInTheDocument();
    });

    it('handles statistics API error gracefully', async () => {
      (apiClient.get as any).mockImplementation((endpoint: string) => {
        if (endpoint === '/api/cases/statistics') {
          return Promise.reject(new Error('Statistics API failed'));
        }
        if (endpoint === '/api/cases') {
          return Promise.resolve({ data: mockCases });
        }
        return Promise.reject(new Error('Unknown endpoint'));
      });

      render(<Dashboard />);

      await waitFor(() => {
        expect(screen.getByText(/Failed to load dashboard data/)).toBeInTheDocument();
      });
    });
  });

  describe('Legal Research Search Interface', () => {
    it('renders search interface correctly', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        expect(screen.getByText('Legal Research')).toBeInTheDocument();
        expect(screen.getByPlaceholderText(/Search legal documents, precedents, statutes/)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument();
      });
    });

    it('shows search suggestions', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        expect(screen.getByText('Try searching for:')).toBeInTheDocument();
        expect(screen.getByText('employment termination')).toBeInTheDocument();
        expect(screen.getByText('contract breach')).toBeInTheDocument();
        expect(screen.getByText('intellectual property')).toBeInTheDocument();
      });
    });

    it('handles search form submission', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText(/Search legal documents, precedents, statutes/);
        const searchButton = screen.getByRole('button', { name: /search/i });

        fireEvent.change(searchInput, { target: { value: 'employment law' } });
        fireEvent.click(searchButton);

        expect(mockNavigate).toHaveBeenCalledWith('/legal-research?q=employment%20law');
      });
    });

    it('handles search form submission with Enter key', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText(/Search legal documents, precedents, statutes/);

        fireEvent.change(searchInput, { target: { value: 'contract dispute' } });
        fireEvent.submit(searchInput.closest('form')!);

        expect(mockNavigate).toHaveBeenCalledWith('/legal-research?q=contract%20dispute');
      });
    });

    it('does not submit empty search', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const searchButton = screen.getByRole('button', { name: /search/i });
        
        fireEvent.click(searchButton);

        expect(mockNavigate).not.toHaveBeenCalled();
      });
    });

    it('handles suggestion tag clicks', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const suggestionTag = screen.getByText('employment termination');
        
        fireEvent.click(suggestionTag);

        const searchInput = screen.getByPlaceholderText(/Search legal documents, precedents, statutes/) as HTMLInputElement;
        expect(searchInput.value).toBe('employment termination');
      });
    });
  });

  describe('Recent Cases Display', () => {
    it('displays recent cases correctly', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        expect(screen.getByText('Recent Cases')).toBeInTheDocument();
        expect(screen.getByText('Employment Dispute - Sarah Chen')).toBeInTheDocument();
        expect(screen.getByText('Software License Violation')).toBeInTheDocument();
      });
    });

    it('shows case details and metadata', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        // Check case status badges
        expect(screen.getByText('active')).toBeInTheDocument();
        expect(screen.getByText('pending')).toBeInTheDocument();

        // Check case types
        expect(screen.getByText('Employment Law')).toBeInTheDocument();
        expect(screen.getByText('Intellectual Property')).toBeInTheDocument();

        // Check priority badges
        expect(screen.getByText('high')).toBeInTheDocument();
        expect(screen.getByText('medium')).toBeInTheDocument();
      });
    });

    it('handles case card clicks for navigation', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const caseCard = screen.getByText('Employment Dispute - Sarah Chen').closest('.case-card');
        expect(caseCard).toBeInTheDocument();

        fireEvent.click(caseCard!);

        expect(mockNavigate).toHaveBeenCalledWith('/cases/case-001');
      });
    });

    it('handles View Details button clicks', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const viewDetailsButtons = screen.getAllByText('View Details');
        
        fireEvent.click(viewDetailsButtons[0]);

        expect(mockNavigate).toHaveBeenCalledWith('/cases/case-001');
      });
    });

    it('handles Documents button clicks', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const documentsButtons = screen.getAllByText('Documents');
        
        fireEvent.click(documentsButtons[0]);

        expect(mockNavigate).toHaveBeenCalledWith('/cases/case-001/documents');
      });
    });

    it('handles View All Cases button click', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const viewAllButton = screen.getByText('View All Cases');
        
        fireEvent.click(viewAllButton);

        expect(mockNavigate).toHaveBeenCalledWith('/cases');
      });
    });

    it('shows empty state when no cases available', async () => {
      (apiClient.get as any).mockImplementation((endpoint: string) => {
        if (endpoint === '/api/cases/statistics') {
          return Promise.resolve({ data: mockStatistics });
        }
        if (endpoint === '/api/cases') {
          return Promise.resolve({ data: [] });
        }
        return Promise.reject(new Error('Unknown endpoint'));
      });

      render(<Dashboard />);

      await waitFor(() => {
        expect(screen.getByText('No recent cases found.')).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    it('displays error message when API calls fail', async () => {
      (apiClient.get as any).mockRejectedValue(new Error('API Error'));

      render(<Dashboard />);

      await waitFor(() => {
        expect(screen.getByText(/Failed to load dashboard data/)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
      });
    });

    it('handles retry button click', async () => {
      // Mock window.location.reload
      const mockReload = vi.fn();
      Object.defineProperty(window, 'location', {
        value: { reload: mockReload },
        writable: true,
      });

      (apiClient.get as any).mockRejectedValue(new Error('API Error'));

      render(<Dashboard />);

      await waitFor(() => {
        const retryButton = screen.getByRole('button', { name: /retry/i });
        fireEvent.click(retryButton);
      });

      expect(mockReload).toHaveBeenCalled();
    });
  });

  describe('Responsive Design and Accessibility', () => {
    it('has proper heading structure', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        expect(screen.getByRole('heading', { level: 1, name: /Shift Legal AI Dashboard/ })).toBeInTheDocument();
        expect(screen.getByRole('heading', { level: 2, name: /Legal Research/ })).toBeInTheDocument();
        expect(screen.getByRole('heading', { level: 2, name: /Recent Cases/ })).toBeInTheDocument();
      });
    });

    it('has proper form labels and accessibility', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText(/Search legal documents, precedents, statutes/);
        expect(searchInput).toHaveAttribute('type', 'text');
        
        const searchForm = searchInput.closest('form');
        expect(searchForm).toBeInTheDocument();
      });
    });

    it('has proper button accessibility', async () => {
      render(<Dashboard />);

      await waitFor(() => {
        const searchButton = screen.getByRole('button', { name: /search/i });
        expect(searchButton).toHaveAttribute('type', 'submit');
        
        const actionButtons = screen.getAllByRole('button');
        actionButtons.forEach(button => {
          expect(button).toBeVisible();
        });
      });
    });
  });
});