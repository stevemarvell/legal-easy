import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '../../../test-utils';
import { mockFetch } from '../../../test-setup';
import RelatedMaterials from '../RelatedMaterials';
import { CorpusItem } from '../../../types/corpus';

// Mock MUI icons to avoid file handle issues
vi.mock('@mui/icons-material', () => ({
  Assignment: () => <div data-testid="contract-icon" />,
  Gavel: () => <div data-testid="clause-icon" />,
  Balance: () => <div data-testid="precedent-icon" />,
  MenuBook: () => <div data-testid="statute-icon" />,
  Description: () => <div data-testid="document-icon" />,
  Link: () => <div data-testid="link-icon" />,
  TrendingUp: () => <div data-testid="relevance-icon" />,
  Visibility: () => <div data-testid="view-icon" />,
  Category: () => <div data-testid="category-icon" />,
  Psychology: () => <div data-testid="concept-icon" />,
  Refresh: () => <div data-testid="refresh-icon" />
}));

// Mock data
const mockCurrentItem: CorpusItem = {
  id: 'rc-001',
  title: 'Employment Contract Template',
  category: 'contracts',
  legal_concepts: ['Employment Law', 'Contract Terms'],
  related_items: ['rc-002', 'rc-003'],
  metadata: {},
  research_areas: ['Employment Law', 'Labour Rights'],
  description: 'Standard UK employment contract template'
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
  },
  {
    id: 'rc-004',
    title: 'Employment Rights Guide',
    category: 'precedents',
    legal_concepts: ['Employment Law', 'Labour Rights'],
    related_items: [],
    metadata: {},
    research_areas: ['Employment Law', 'Labour Rights'],
    description: 'Guide to employment rights and obligations'
  }
];

describe('RelatedMaterials Component', () => {
  const mockOnItemSelect = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    mockFetch.mockClear();
  });

  const setupMockResponses = () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockCurrentItem
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockRelatedItems
      });
  };

  it('renders empty state when no item selected', () => {
    render(<RelatedMaterials itemId={null} />);

    expect(screen.getByText('Select an Item')).toBeInTheDocument();
    expect(screen.getByText('Choose a corpus item to view related materials.')).toBeInTheDocument();
  });

  it('renders related materials correctly', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    expect(screen.getByText('Related Materials')).toBeInTheDocument();
    expect(screen.getByText('Items (3)')).toBeInTheDocument();
  });

  it('displays current item summary', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    expect(screen.getByText('Current Item: Employment Contract Template')).toBeInTheDocument();
    expect(screen.getAllByText('Contract').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Employment Law').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Labour Rights').length).toBeGreaterThanOrEqual(1);
  });

  it('displays statistics correctly', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check statistics - there are multiple "3" elements, so use getAllByText
    expect(screen.getAllByText('3').length).toBeGreaterThanOrEqual(1); // Related Items count
    expect(screen.getByText('Related Items')).toBeInTheDocument();
    expect(screen.getByText('Categories')).toBeInTheDocument();
  });

  it('displays related items with correct information', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check related items
    const relatedItems = screen.getAllByTestId('related-item');
    expect(relatedItems).toHaveLength(3);

    expect(screen.getByText('Service Agreement Template')).toBeInTheDocument();
    expect(screen.getByText('Termination Clauses')).toBeInTheDocument();
    expect(screen.getByText('Employment Rights Guide')).toBeInTheDocument();
  });

  it('displays relationship types correctly', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Check relationship type chips
    expect(screen.getByText('Same Category')).toBeInTheDocument(); // Service Agreement (same contracts category)
    expect(screen.getAllByText('Shared: Employment Law').length).toBeGreaterThanOrEqual(1); // Termination Clauses and Employment Rights Guide
  });

  it('displays relevance scores', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Should display relevance scores (numbers will vary based on calculation)
    const relevanceScores = screen.getAllByText(/^\d$/);
    expect(relevanceScores.length).toBeGreaterThan(0);
  });

  it('handles item selection', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Click on a related item
    const relatedItems = screen.getAllByTestId('related-item');
    fireEvent.click(relatedItems[0]);

    expect(mockOnItemSelect).toHaveBeenCalledWith(mockRelatedItems[0]);
  });

  it('highlights selected item', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        selectedItemId="rc-002"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    const relatedItems = screen.getAllByTestId('related-item');
    expect(relatedItems[0]).toHaveClass('Mui-selected');
  });

  it('handles refresh functionality', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Setup additional mock for refresh
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockRelatedItems
    });

    // Click refresh button
    const refreshButton = screen.getByRole('button', { name: /refresh/i });
    fireEvent.click(refreshButton);

    // Should make another API call
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledTimes(3); // Initial 2 calls + 1 refresh call
    });
  });

  it('respects maxItems prop', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        maxItems={2}
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Should only show 2 items despite having 3 in mock data
    const relatedItems = screen.getAllByTestId('related-item');
    expect(relatedItems).toHaveLength(2);
  });

  it('can hide header when showHeader is false', async () => {
    setupMockResponses();

    render(
      <RelatedMaterials
        itemId="rc-001"
        showHeader={false}
        onItemSelect={mockOnItemSelect}
      />
    );

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Header should not be visible
    expect(screen.queryByText('Related Materials')).not.toBeInTheDocument();
    expect(screen.queryByText('Current Item:')).not.toBeInTheDocument();

    // But items should still be visible
    expect(screen.getAllByTestId('related-item')).toHaveLength(3);
  });

  it('handles loading state', () => {
    render(<RelatedMaterials itemId="rc-001" />);

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('handles error state', async () => {
    mockFetch.mockRejectedValueOnce(new Error('API Error'));

    render(<RelatedMaterials itemId="rc-001" />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to load related materials/)).toBeInTheDocument();
    });

    // Should show retry button
    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
  });

  it('handles empty related materials', async () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockCurrentItem
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

    render(<RelatedMaterials itemId="rc-001" />);

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    expect(screen.getByText('No Related Materials')).toBeInTheDocument();
    expect(screen.getByText('No related items found for this corpus item.')).toBeInTheDocument();
  });

  it('handles research areas with overflow', async () => {
    const itemWithManyAreas: CorpusItem = {
      ...mockRelatedItems[0],
      research_areas: ['Area 1', 'Area 2', 'Area 3', 'Area 4', 'Area 5']
    };

    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockCurrentItem
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [itemWithManyAreas]
      });

    render(<RelatedMaterials itemId="rc-001" />);

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    // Should show only first 2 areas plus overflow indicator
    expect(screen.getByText('Area 1')).toBeInTheDocument();
    expect(screen.getByText('Area 2')).toBeInTheDocument();
    expect(screen.getByText('+3')).toBeInTheDocument();
  });
});