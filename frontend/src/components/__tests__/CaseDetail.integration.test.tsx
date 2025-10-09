import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import CaseDetail from '../CaseDetail';

// Mock useParams
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ caseId: 'case-001' })
  };
});

// Mock fetch
global.fetch = vi.fn();

const mockCase = {
  id: 'case-001',
  title: 'Test Employment Case',
  case_type: 'Employment Dispute',
  client_name: 'John Doe',
  status: 'Active',
  created_date: '2024-01-15T09:00:00Z',
  summary: 'Test case summary',
  key_parties: ['John Doe (Claimant)', 'ABC Corp (Respondent)'],
  documents: ['doc-001', 'doc-002'],
  playbook_id: 'employment-dispute'
};

const mockPlaybook = {
  id: 'employment-dispute',
  case_type: 'Employment Dispute',
  name: 'Employment Law Playbook',
  description: 'Test playbook',
  rules: [
    {
      id: 'rule-001',
      condition: 'termination_within_protected_period',
      action: 'investigate_retaliation_claim',
      weight: 0.9,
      description: 'Test rule description',
      enabled: true,
      priority: 0.9
    }
  ],
  decision_tree: {},
  monetary_ranges: {
    high: {
      range: [200000, 1000000],
      description: 'High damages',
      factors: ['Full compensatory damages']
    }
  },
  escalation_paths: ['Internal HR complaint']
};

const mockAppliedRules = {
  case_id: 'case-001',
  playbook_id: 'employment-dispute',
  applied_rules: ['rule-001'],
  recommendations: ['investigate_retaliation_claim'],
  case_strength: 'Strong',
  reasoning: 'Test reasoning for strong case'
};

describe('CaseDetail Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('integrates PlaybookViewer correctly in playbook tab', async () => {
    // Mock case fetch
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockCase
    });

    render(
      <BrowserRouter>
        <CaseDetail />
      </BrowserRouter>
    );

    // Wait for case to load
    await waitFor(() => {
      expect(screen.getByText('Test Employment Case')).toBeInTheDocument();
    });

    // Check that playbook tab exists
    expect(screen.getByText('Playbook')).toBeInTheDocument();

    // Mock playbook and applied rules fetches for when tab is clicked
    (fetch as any)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockPlaybook
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAppliedRules
      });

    // Click on playbook tab
    fireEvent.click(screen.getByText('Playbook'));

    // Wait for playbook to load
    await waitFor(() => {
      expect(screen.getByText('Employment Law Playbook')).toBeInTheDocument();
    });

    // Check that applied rules are shown
    expect(screen.getByText('Applied to Current Case')).toBeInTheDocument();
    expect(screen.getByText('Strong')).toBeInTheDocument();
    expect(screen.getByText('Test reasoning for strong case')).toBeInTheDocument();

    // Check that rule details are shown
    expect(screen.getByText('rule-001')).toBeInTheDocument();
    expect(screen.getByText('Weight: 90%')).toBeInTheDocument();
  });

  it('displays case information correctly', async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockCase
    });

    render(
      <BrowserRouter>
        <CaseDetail />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Employment Case')).toBeInTheDocument();
    });

    // Check case metadata
    expect(screen.getByText('case-001')).toBeInTheDocument();
    expect(screen.getByText('Employment Dispute')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Active')).toBeInTheDocument();

    // Check case summary
    expect(screen.getByText('Test case summary')).toBeInTheDocument();

    // Check key parties
    expect(screen.getByText('John Doe (Claimant)')).toBeInTheDocument();
    expect(screen.getByText('ABC Corp (Respondent)')).toBeInTheDocument();

    // Check documents
    expect(screen.getByText('Documents (2)')).toBeInTheDocument();
  });
});