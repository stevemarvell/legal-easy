import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import PlaybookViewer from '../Playbook/PlaybookViewer';
import { it } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { beforeEach } from 'node:test';
import { describe } from 'node:test';

// Mock fetch
global.fetch = vi.fn();

const mockPlaybook = {
  id: 'employment-dispute',
  case_type: 'Employment Dispute',
  name: 'Employment Law Playbook',
  description: 'Test playbook',
  rules: [
    {
      id: 'rule-001',
      condition: 'termination_within_protected_period',
      action: 'investigate_victimisation_claim',
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
  recommendations: ['investigate_victimisation_claim'],
  case_strength: 'Strong',
  reasoning: 'Test reasoning'
};

describe('PlaybookViewer', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders playbook information correctly', async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockPlaybook
    });

    render(<PlaybookViewer caseType="Employment Dispute" />);

    await waitFor(() => {
      expect(screen.getByText('Employment Law Playbook')).toBeInTheDocument();
    });

    expect(screen.getByText('Employment Dispute')).toBeInTheDocument();
    expect(screen.getByText('1 Rules')).toBeInTheDocument();
  });

  it('shows applied rules when showAppliedRules is true', async () => {
    (fetch as any)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockPlaybook
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockAppliedRules
      });

    render(
      <PlaybookViewer 
        caseType="Employment Dispute" 
        caseId="case-001"
        showAppliedRules={true}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Applied to Current Case')).toBeInTheDocument();
    });

    expect(screen.getByText('Strong')).toBeInTheDocument();
    expect(screen.getByText('Test reasoning')).toBeInTheDocument();
  });

  it('displays rules with correct styling', async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockPlaybook
    });

    render(<PlaybookViewer caseType="Employment Dispute" />);

    await waitFor(() => {
      expect(screen.getByText('rule-001')).toBeInTheDocument();
    });

    expect(screen.getByText('Weight: 90%')).toBeInTheDocument();
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('handles loading state', () => {
    (fetch as any).mockImplementation(() => new Promise(() => {})); // Never resolves

    render(<PlaybookViewer caseType="Employment Dispute" />);

    expect(screen.getByText('Loading playbook...')).toBeInTheDocument();
  });

  it('handles error state', async () => {
    (fetch as any).mockRejectedValueOnce(new Error('Network error'));

    render(<PlaybookViewer caseType="Employment Dispute" />);

    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
    });

    expect(screen.getByText('Retry')).toBeInTheDocument();
  });
});