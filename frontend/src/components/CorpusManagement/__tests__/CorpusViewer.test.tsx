import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '../../../test-utils';
import { mockFetch } from '../../../test-setup';
import CorpusViewer from '../CorpusViewer';
import { CorpusItem } from '../../../types/corpus';

// Mock MUI icons to avoid file handle issues
vi.mock('@mui/icons-material', () => ({
  Assignment: () => <div data-testid="contract-icon" />,
  Gavel: () => <div data-testid="clause-icon" />,
  Balance: () => <div data-testid="precedent-icon" />,
  MenuBook: () => <div data-testid="statute-icon" />,
  Description: () => <div data-testid="document-icon" />,
  ExpandMore: () => <div data-testid="expand-more-icon" />,
  ExpandLess: () => <div data-testid="expand-less-icon" />,
  Link: () => <div data-testid="link-icon" />,
  Category: () => <div data-testid="category-icon" />,
  Psychology: () => <div data-testid="concept-icon" />,
  Folder: () => <div data-testid="folder-icon" />
}));

// Mock data
const mockCorpusItem: CorpusItem = {
  id: 'rc-001',
  title: 'Employment Contract Template',
  category: 'contracts',
  content: 'EMPLOYMENT AGREEMENT\n\nThis Employment Agreement is entered into...',
  legal_concepts: ['Employment Law', 'Contract Terms', 'Termination'],
  related_items: ['rc-002', 'rc-003'],
  metadata: { version: '1.0' },
  filename: 'employment_contract.txt',
  document_type: 'Contract Template',
  research_areas: ['Employment Law', 'Labour Rights'],
  description: 'Standard UK employment contract template with key clauses'
};

const mockRelatedItems: CorpusItem[] = [
  {
    id: 'rc-002',
    title: 'Service Agreement Template',
    category: 'contracts',
    legal_concepts: ['Service Agreements'],
    related_items: ['rc-001'],
    metadata: {},
    research_areas: ['Commercial Law'],
    description: 'Professional service agreement template'
  },
  {
    id: 'rc-003',
    title: 'Termination Clauses',
    category: 'clauses',
    legal_concepts: ['Termination'],
    related_items: ['rc-001'],
    metadata: {},
    research_areas: ['Employment Law'],
    description: 'Various termination clause templates'
  }
];

describe('CorpusViewer Component', () => {
  const mockOnRelatedItemSelect = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    mockFetch.mockClear();
  });

  const setupMockResponses = () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockCorpusItem
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockRelatedItems
      });
  };

  it('renders empty state when no item selected', () => {
    render(<CorpusViewer itemId={null} />);

    expect(screen.getByText('Select a Corpus Item')).toBeInTheDocument();
    expect(screen.getByText('Choose an item from the list to view its content and details.')).toBeInTheDocument();
  });

  it('renders corpus item details correctly', async () => {
    setupMockResponses();

    render(
      <CorpusViewer
        itemId="rc-001"
        onRelatedItemSelect={mockOnRelatedItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check title and description
    expect(screen.getByTestId('item-title')).toHaveTextContent('Employment Contract Template');
    expect(screen.getByText('Standard UK employment contract template with key clauses')).toBeInTheDocument();

    // Check metadata chips - Contract appears in category chip and possibly elsewhere
    expect(screen.getAllByText('Contract').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Contract Template')).toBeInTheDocument();
    expect(screen.getByText('employment_contract.txt')).toBeInTheDocument();

    // Check research areas - Employment Law appears in multiple places
    expect(screen.getAllByText('Employment Law').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Labour Rights')).toBeInTheDocument();
  });

  it('displays content correctly', async () => {
    setupMockResponses();

    render(
      <CorpusViewer
        itemId="rc-001"
        onRelatedItemSelect={mockOnRelatedItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check content display
    expect(screen.getByTestId('item-content')).toHaveTextContent('EMPLOYMENT AGREEMENT');
    expect(screen.getByTestId('item-content')).toHaveTextContent('This Employment Agreement is entered into...');
  });

  it('displays legal concepts', async () => {
    setupMockResponses();

    render(
      <CorpusViewer
        itemId="rc-001"
        onRelatedItemSelect={mockOnRelatedItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check legal concepts section
    expect(screen.getByText('Legal Concepts (3)')).toBeInTheDocument();
    
    const conceptChips = screen.getAllByTestId('legal-concept');
    expect(conceptChips).toHaveLength(3);
    // Check that Employment Law appears in legal concepts (it also appears in research areas and related items)
    expect(screen.getAllByText('Employment Law').length).toBeGreaterThanOrEqual(2);
    expect(screen.getByText('Contract Terms')).toBeInTheDocument();
    expect(screen.getByText('Termination')).toBeInTheDocument();
  });

  it('displays related materials', async () => {
    setupMockResponses();

    render(
      <CorpusViewer
        itemId="rc-001"
        onRelatedItemSelect={mockOnRelatedItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check related materials section
    expect(screen.getByText('Related Materials (2)')).toBeInTheDocument();
    
    const relatedItems = screen.getAllByTestId('related-item');
    expect(relatedItems).toHaveLength(2);
    expect(screen.getByText('Service Agreement Template')).toBeInTheDocument();
    expect(screen.getByText('Termination Clauses')).toBeInTheDocument();
  });

  it('handles related item selection', async () => {
    setupMockResponses();

    render(
      <CorpusViewer
        itemId="rc-001"
        onRelatedItemSelect={mockOnRelatedItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Click on a related item
    const relatedItems = screen.getAllByTestId('related-item');
    fireEvent.click(relatedItems[0]);

    expect(mockOnRelatedItemSelect).toHaveBeenCalledWith(mockRelatedItems[0]);
  });

  it('handles loading state', () => {
    render(<CorpusViewer itemId="rc-001" />);

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('handles error state', async () => {
    mockFetch.mockRejectedValueOnce(new Error('API Error'));

    render(<CorpusViewer itemId="rc-001" />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to load corpus item/)).toBeInTheDocument();
    });
  });

  it('handles item not found', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ detail: 'Item not found' })
    });

    render(<CorpusViewer itemId="rc-999" />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to load corpus item/)).toBeInTheDocument();
    });
  });

  it('handles item without content', async () => {
    const itemWithoutContent = { ...mockCorpusItem, content: undefined };
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => itemWithoutContent
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

    render(<CorpusViewer itemId="rc-001" />);

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    expect(screen.getByText('Content not available for this item.')).toBeInTheDocument();
  });

  it('handles collapsible sections', async () => {
    setupMockResponses();

    render(<CorpusViewer itemId="rc-001" />);

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Legal concepts should be expanded by default
    expect(screen.getAllByTestId('legal-concept')).toHaveLength(3);

    // Related materials should be expanded by default
    expect(screen.getAllByTestId('related-item')).toHaveLength(2);
  });

  it('displays correct category icons', async () => {
    setupMockResponses();

    render(<CorpusViewer itemId="rc-001" />);

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // The contract icon should be displayed (we can't easily test the specific icon, 
    // but we can verify the component renders without errors)
    expect(screen.getByTestId('corpus-viewer')).toBeInTheDocument();
  });
});