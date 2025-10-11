import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '../../../test-utils';
import { mockFetch } from '../../../test-setup';
import CorpusList from '../CorpusList';
import { CorpusItem, CorpusCategory } from '../../../types/corpus';

// Mock MUI icons to avoid file handle issues
vi.mock('@mui/icons-material', () => ({
  Assignment: () => <div data-testid="contract-icon" />,
  Gavel: () => <div data-testid="clause-icon" />,
  Balance: () => <div data-testid="precedent-icon" />,
  MenuBook: () => <div data-testid="statute-icon" />,
  Description: () => <div data-testid="document-icon" />,
  Category: () => <div data-testid="category-icon" />,
  Search: () => <div data-testid="search-icon" />
}));

// Mock data
const mockCategories: Record<string, CorpusCategory> = {
  contracts: {
    name: 'Contract Templates',
    description: 'Standard UK contract templates',
    document_ids: ['rc-001', 'rc-002']
  },
  clauses: {
    name: 'Research Clauses',
    description: 'Library of standard research clauses',
    document_ids: ['rc-003', 'rc-004']
  },
  precedents: {
    name: 'Legal Precedents',
    description: 'Case law and legal precedents',
    document_ids: ['rc-005']
  },
  statutes: {
    name: 'Statutes and Regulations',
    description: 'Legislation and regulations',
    document_ids: ['rc-006']
  }
};

const mockCorpusItems: CorpusItem[] = [
  {
    id: 'rc-001',
    title: 'Employment Contract Template',
    category: 'contracts',
    legal_concepts: ['Employment Law', 'Contract Terms'],
    related_items: ['rc-002'],
    metadata: {},
    filename: 'employment_contract.txt',
    document_type: 'Contract Template',
    research_areas: ['Employment Law'],
    description: 'Standard UK employment contract template'
  },
  {
    id: 'rc-002',
    title: 'Service Agreement Template',
    category: 'contracts',
    legal_concepts: ['Service Agreements', 'Commercial Law'],
    related_items: ['rc-001'],
    metadata: {},
    filename: 'service_agreement.txt',
    document_type: 'Contract Template',
    research_areas: ['Commercial Law'],
    description: 'Professional service agreement template'
  },
  {
    id: 'rc-003',
    title: 'Termination Clauses',
    category: 'clauses',
    legal_concepts: ['Termination', 'Employment Law'],
    related_items: ['rc-001'],
    metadata: {},
    filename: 'termination_clauses.txt',
    document_type: 'Legal Clause',
    research_areas: ['Employment Law'],
    description: 'Various termination clause templates'
  }
];

describe('CorpusList Component', () => {
  const mockOnItemSelect = vi.fn();
  const mockOnCategoryChange = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    mockFetch.mockClear();
  });

  const setupMockResponses = () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockCategories
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockCorpusItems
      });
  };

  it('renders corpus list with basic functionality', async () => {
    setupMockResponses();

    render(
      <CorpusList
        onItemSelect={mockOnItemSelect}
        onCategoryChange={mockOnCategoryChange}
      />
    );

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check if basic elements are rendered
    expect(screen.getByText('Research Categories')).toBeInTheDocument();
    expect(screen.getByText('Employment Contract Template')).toBeInTheDocument();
  });

  it('handles loading state', () => {
    render(
      <CorpusList
        onItemSelect={mockOnItemSelect}
        onCategoryChange={mockOnCategoryChange}
      />
    );

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('handles error state', async () => {
    mockFetch.mockRejectedValueOnce(new Error('API Error'));

    render(
      <CorpusList
        onItemSelect={mockOnItemSelect}
        onCategoryChange={mockOnCategoryChange}
      />
    );

    await waitFor(() => {
      expect(screen.getByText(/Failed to load corpus data/)).toBeInTheDocument();
    });
  });
});