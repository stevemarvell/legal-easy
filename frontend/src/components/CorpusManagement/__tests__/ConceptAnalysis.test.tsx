import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '../../../test-utils';
import { mockFetch } from '../../../test-setup';
import ConceptAnalysis from '../ConceptAnalysis';
import { ConceptAnalysisResult, LegalConcept } from '../../../types/corpus';

// Mock MUI icons to avoid file handle issues
vi.mock('@mui/icons-material', () => ({
  Psychology: () => <div data-testid="concept-icon" />,
  ExpandMore: () => <div data-testid="expand-more-icon" />,
  ExpandLess: () => <div data-testid="expand-less-icon" />,
  Link: () => <div data-testid="link-icon" />,
  Category: () => <div data-testid="category-icon" />,
  TrendingUp: () => <div data-testid="trending-icon" />,
  Visibility: () => <div data-testid="view-icon" />,
  AccountTree: () => <div data-testid="relationship-icon" />
}));

// Mock data
const mockConcepts: LegalConcept[] = [
  {
    id: 'employment-law',
    name: 'Employment Law',
    definition: 'Legal framework governing employer-employee relationships and workplace rights',
    related_concepts: ['Contract Law', 'Labour Rights'],
    corpus_references: ['rc-001', 'rc-003', 'rc-007']
  },
  {
    id: 'contract-law',
    name: 'Contract Law',
    definition: 'Legal principles governing the formation, performance, and enforcement of contracts',
    related_concepts: ['Employment Law', 'Commercial Law'],
    corpus_references: ['rc-001', 'rc-002', 'rc-004']
  },
  {
    id: 'intellectual-property',
    name: 'Intellectual Property',
    definition: 'Legal rights protecting creations of the mind, including patents, copyrights, and trademarks',
    related_concepts: ['Commercial Law', 'Data Protection'],
    corpus_references: ['rc-005', 'rc-006']
  }
];

const mockConceptAnalysis: ConceptAnalysisResult = {
  concepts: mockConcepts,
  total_concepts: 3,
  categories_analyzed: ['contracts', 'clauses', 'precedents', 'statutes'],
  research_areas: ['Employment Law', 'Contract Law', 'Intellectual Property', 'Commercial Law']
};

describe('ConceptAnalysis Component', () => {
  const mockOnConceptSelect = vi.fn();
  const mockOnCorpusItemSelect = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    mockFetch.mockClear();
  });

  const setupMockResponse = () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockConceptAnalysis
    });
  };

  it('renders concept analysis correctly', async () => {
    setupMockResponse();

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    expect(screen.getByText('Legal Concept Analysis')).toBeInTheDocument();
    expect(screen.getByText('Legal Concepts (3)')).toBeInTheDocument();
  });

  it('displays summary statistics correctly', async () => {
    setupMockResponse();

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check statistics
    expect(screen.getByText('3')).toBeInTheDocument(); // Total concepts
    expect(screen.getByText('Total Concepts')).toBeInTheDocument();
    expect(screen.getAllByText('4').length).toBeGreaterThanOrEqual(1); // Research areas and categories both show 4
    expect(screen.getByText('Research Areas')).toBeInTheDocument();
    expect(screen.getByText('Categories')).toBeInTheDocument();
    expect(screen.getByText('Total References')).toBeInTheDocument();
  });

  it('displays research areas and categories', async () => {
    setupMockResponse();

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check research areas
    expect(screen.getByText('Research Areas:')).toBeInTheDocument();
    expect(screen.getAllByText('Employment Law').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Contract Law').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Intellectual Property').length).toBeGreaterThanOrEqual(1);

    // Check categories
    expect(screen.getByText('Categories Analyzed:')).toBeInTheDocument();
    expect(screen.getByText('Contracts')).toBeInTheDocument();
    expect(screen.getByText('Clauses')).toBeInTheDocument();
    expect(screen.getByText('Precedents')).toBeInTheDocument();
    expect(screen.getByText('Statutes')).toBeInTheDocument();
  });

  it('displays concept list with correct information', async () => {
    setupMockResponse();

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check concept items
    const conceptItems = screen.getAllByTestId('concept-item');
    expect(conceptItems).toHaveLength(3);

    expect(screen.getAllByText('Employment Law').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Contract Law').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Intellectual Property').length).toBeGreaterThanOrEqual(1);

    // Check reference counts - there might be multiple concepts with same ref count
    expect(screen.getAllByText('3 refs').length).toBeGreaterThanOrEqual(1); // Employment Law
    expect(screen.getByText('2 refs')).toBeInTheDocument(); // Intellectual Property
  });

  it('handles concept selection', async () => {
    setupMockResponse();

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Click on a concept
    const conceptItems = screen.getAllByTestId('concept-item');
    fireEvent.click(conceptItems[0]);

    expect(mockOnConceptSelect).toHaveBeenCalledWith(mockConcepts[0]);
  });

  it('expands and collapses concept details', async () => {
    setupMockResponse();

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Initially, expanded content should not be visible
    expect(screen.queryByText('Legal framework governing employer-employee relationships')).not.toBeInTheDocument();

    // Click expand button
    const expandButtons = screen.getAllByTestId('expand-concept');
    fireEvent.click(expandButtons[0]);

    // Now expanded content should be visible
    await waitFor(() => {
      expect(screen.getAllByText('Legal framework governing employer-employee relationships and workplace rights').length).toBeGreaterThanOrEqual(1);
    });

    // Check related concepts
    expect(screen.getAllByText('Related Concepts:').length).toBeGreaterThanOrEqual(1);
    const relatedConcepts = screen.getAllByTestId('related-concept');
    expect(relatedConcepts.length).toBeGreaterThanOrEqual(2);

    // Check corpus references - there might be multiple concepts with same ref count
    expect(screen.getAllByText('Corpus References (3):').length).toBeGreaterThanOrEqual(1);
    const corpusReferences = screen.getAllByTestId('corpus-reference');
    expect(corpusReferences.length).toBeGreaterThanOrEqual(3);
  });

  it('handles corpus reference clicks', async () => {
    setupMockResponse();

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Expand first concept
    const expandButtons = screen.getAllByTestId('expand-concept');
    fireEvent.click(expandButtons[0]);

    await waitFor(() => {
      // There might be more corpus references from multiple concepts
      expect(screen.getAllByTestId('corpus-reference').length).toBeGreaterThanOrEqual(3);
    });

    // Click on a corpus reference
    const corpusReferences = screen.getAllByTestId('corpus-reference');
    fireEvent.click(corpusReferences[0]);

    expect(mockOnCorpusItemSelect).toHaveBeenCalledWith('rc-001');
  });

  it('highlights selected concept', async () => {
    setupMockResponse();

    render(
      <ConceptAnalysis
        selectedConceptId="employment-law"
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    const conceptItems = screen.getAllByTestId('concept-item');
    expect(conceptItems[0]).toHaveClass('Mui-selected');
  });

  it('handles loading state', () => {
    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('handles error state', async () => {
    mockFetch.mockRejectedValueOnce(new Error('API Error'));

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.getByText(/Failed to load concept analysis/)).toBeInTheDocument();
    });
  });

  it('handles empty concept analysis', async () => {
    const emptyAnalysis: ConceptAnalysisResult = {
      concepts: [],
      total_concepts: 0,
      categories_analyzed: [],
      research_areas: []
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => emptyAnalysis
    });

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Legal Concepts (0)')).toBeInTheDocument();
    });
  });

  it('handles concepts with many corpus references', async () => {
    const conceptWithManyRefs: LegalConcept = {
      id: 'test-concept',
      name: 'Test Concept',
      definition: 'A test concept with many references',
      related_concepts: [],
      corpus_references: Array.from({ length: 15 }, (_, i) => `rc-${i.toString().padStart(3, '0')}`)
    };

    const analysisWithManyRefs: ConceptAnalysisResult = {
      concepts: [conceptWithManyRefs],
      total_concepts: 1,
      categories_analyzed: ['contracts'],
      research_areas: ['Test Area']
    };

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => analysisWithManyRefs
    });

    render(
      <ConceptAnalysis
        onConceptSelect={mockOnConceptSelect}
        onCorpusItemSelect={mockOnCorpusItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Expand the concept
    const expandButton = screen.getByTestId('expand-concept');
    fireEvent.click(expandButton);

    await waitFor(() => {
      // Should show only first 10 references plus a "+5 more" chip
      const corpusReferences = screen.getAllByTestId('corpus-reference');
      expect(corpusReferences).toHaveLength(10);
      expect(screen.getByText('+5 more')).toBeInTheDocument();
    });
  });
});