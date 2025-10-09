import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '../../test-utils';
import Playbooks from '../../pages/Playbooks';
import { apiClient } from '../../services/api';
import { Playbook } from '../../types/api';

// Mock the API client
vi.mock('../../services/api', () => ({
  apiClient: {
    get: vi.fn(),
  },
}));

// Mock react-router-dom
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
    useParams: () => ({}),
  };
});

const mockPlaybooks: Playbook[] = [
  {
    id: 'employment-dispute',
    case_type: 'Employment Dispute',
    name: 'Employment Law Playbook',
    description: 'Comprehensive framework for employment dispute cases',
    rules: [
      {
        id: 'rule-001',
        condition: 'termination_within_protected_period',
        action: 'investigate_victimisation_claim',
        weight: 0.9,
        description: 'Check for potential victimisation',
      },
    ],
    decision_tree: {},
    monetary_ranges: {
      high: { range: [200000, 1000000] },
      medium: { range: [50000, 200000] },
    },
    escalation_paths: ['Internal HR complaint', 'ACAS early conciliation'],
  },
  {
    id: 'contract-breach',
    case_type: 'Contract Breach',
    name: 'Contract Law Playbook',
    description: 'Framework for contract breach cases',
    rules: [
      {
        id: 'rule-002',
        condition: 'material_breach_identified',
        action: 'assess_damages',
        weight: 0.8,
        description: 'Assess damages for material breach',
      },
    ],
    decision_tree: {},
    monetary_ranges: {
      high: { range: [100000, 500000] },
    },
    escalation_paths: ['Mediation', 'Arbitration'],
  },
];

describe('Playbooks Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    vi.mocked(apiClient.get).mockImplementation(
      () => new Promise(() => {}) // Never resolves to keep loading state
    );

    render(<Playbooks />);
    
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('renders playbooks list when data is loaded', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: mockPlaybooks });

    render(<Playbooks />);

    await waitFor(() => {
      expect(screen.getByText('Legal Playbooks')).toBeInTheDocument();
      expect(screen.getByText('Employment Law Playbook')).toBeInTheDocument();
      expect(screen.getByText('Contract Law Playbook')).toBeInTheDocument();
    });
  });

  it('displays playbook information correctly', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: mockPlaybooks });

    render(<Playbooks />);

    await waitFor(() => {
      // Check case type chips
      expect(screen.getByText('Employment Dispute')).toBeInTheDocument();
      expect(screen.getByText('Contract Breach')).toBeInTheDocument();

      // Check rule counts
      expect(screen.getByText('1 Rules')).toBeInTheDocument();

      // Check assessment ranges
      expect(screen.getByText('2 Assessment Ranges')).toBeInTheDocument();
      expect(screen.getByText('1 Assessment Ranges')).toBeInTheDocument();
    });
  });

  it('navigates to specific playbook when clicked', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: mockPlaybooks });

    render(<Playbooks />);

    await waitFor(() => {
      expect(screen.getByText('Employment Law Playbook')).toBeInTheDocument();
    });

    const playbookCard = screen.getByText('Employment Law Playbook').closest('[role="button"]');
    expect(playbookCard).toBeInTheDocument();

    fireEvent.click(playbookCard!);

    expect(mockNavigate).toHaveBeenCalledWith('/playbooks/Employment%20Dispute');
  });

  it('displays empty state when no playbooks', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] });

    render(<Playbooks />);

    await waitFor(() => {
      expect(screen.getByText('No playbooks are currently available in the system.')).toBeInTheDocument();
    });
  });

  it('displays error state when API call fails', async () => {
    vi.mocked(apiClient.get).mockRejectedValue(new Error('API Error'));

    render(<Playbooks />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load playbooks. Please try again.')).toBeInTheDocument();
    });
  });

  it('shows breadcrumb navigation', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: mockPlaybooks });

    render(<Playbooks />);

    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Playbooks')).toBeInTheDocument();
    });
  });

  it('displays help section', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: mockPlaybooks });

    render(<Playbooks />);

    await waitFor(() => {
      expect(screen.getByText('About Legal Playbooks')).toBeInTheDocument();
      expect(screen.getByText(/Legal playbooks are AI-powered frameworks/)).toBeInTheDocument();
    });
  });

  it('shows key features for each playbook', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: mockPlaybooks });

    render(<Playbooks />);

    await waitFor(() => {
      expect(screen.getByText('Key Features')).toBeInTheDocument();
      expect(screen.getByText('• Automated rule application')).toBeInTheDocument();
      expect(screen.getByText('• Case strength assessment')).toBeInTheDocument();
      expect(screen.getByText('• Strategic recommendations')).toBeInTheDocument();
    });
  });
});