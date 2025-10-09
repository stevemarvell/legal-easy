import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '../../test-utils';
import DocumentAnalysis from '../DocumentManagement/DocumentAnalysis';
import { documentService } from '../../services/documentService';
import { DocumentAnalysis as DocumentAnalysisType } from '../../types/document';

// Mock the document service
vi.mock('../../services/documentService', () => ({
  documentService: {
    getDocumentAnalysis: vi.fn(),
  },
}));

const mockAnalysis: DocumentAnalysisType = {
  document_id: 'doc-001',
  key_dates: ['2024-01-15', '2024-03-01', '2024-06-15'],
  parties_involved: ['Sarah Chen', 'TechCorp Solutions Inc.', 'Safety Department'],
  document_type: 'Employment Contract',
  summary: 'This employment agreement establishes the terms and conditions for Sarah Chen\'s position as Senior Safety Engineer at TechCorp Solutions Inc. The contract includes standard employment terms, safety reporting obligations, and termination clauses.',
  key_clauses: [
    'At-will employment clause',
    'Safety reporting obligations',
    'Confidentiality agreement',
    'Termination procedures'
  ],
  confidence_scores: {
    parties: 0.95,
    dates: 0.88,
    document_type: 0.92,
    key_clauses: 0.85,
    summary: 0.90
  }
};

const mockEmptyAnalysis: DocumentAnalysisType = {
  document_id: 'doc-002',
  key_dates: [],
  parties_involved: [],
  document_type: 'Unknown',
  summary: 'No summary available.',
  key_clauses: [],
  confidence_scores: {
    parties: 0.45,
    dates: 0.30,
    document_type: 0.55
  }
};

describe('DocumentAnalysis Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    vi.mocked(documentService.getDocumentAnalysis).mockImplementation(
      () => new Promise(() => {}) // Never resolves to keep loading state
    );

    render(<DocumentAnalysis documentId="doc-001" />);
    
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('renders analysis results when loaded', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('AI Document Analysis')).toBeInTheDocument();
      expect(screen.getByText(/doc-001/)).toBeInTheDocument();
    });
  });

  it('displays document summary correctly', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Document Summary')).toBeInTheDocument();
      expect(screen.getByText(/employment agreement establishes the terms/)).toBeInTheDocument();
    });
  });

  it('shows key dates section with formatted dates', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Key Dates (3)')).toBeInTheDocument();
      expect(screen.getByText('January 15, 2024')).toBeInTheDocument();
      expect(screen.getByText('March 1, 2024')).toBeInTheDocument();
      expect(screen.getByText('June 15, 2024')).toBeInTheDocument();
    });
  });

  it('displays parties involved correctly', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Parties Involved (3)')).toBeInTheDocument();
      expect(screen.getByText('Sarah Chen')).toBeInTheDocument();
      expect(screen.getByText('TechCorp Solutions Inc.')).toBeInTheDocument();
      expect(screen.getByText('Safety Department')).toBeInTheDocument();
    });
  });

  it('shows document classification', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Document Classification')).toBeInTheDocument();
      expect(screen.getByText('Employment Contract')).toBeInTheDocument();
    });
  });

  it('displays key clauses', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Key Clauses (4)')).toBeInTheDocument();
      expect(screen.getByText('At-will employment clause')).toBeInTheDocument();
      expect(screen.getByText('Safety reporting obligations')).toBeInTheDocument();
      expect(screen.getByText('Confidentiality agreement')).toBeInTheDocument();
      expect(screen.getByText('Termination procedures')).toBeInTheDocument();
    });
  });

  it('shows confidence scores with correct formatting', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Analysis Confidence Scores')).toBeInTheDocument();
      expect(screen.getByText('95%')).toBeInTheDocument(); // parties
      expect(screen.getByText('88%')).toBeInTheDocument(); // dates
      expect(screen.getByText('92%')).toBeInTheDocument(); // document_type
      expect(screen.getByText('85%')).toBeInTheDocument(); // key_clauses
      expect(screen.getByText('90%')).toBeInTheDocument(); // summary
    });
  });

  it('displays confidence score categories correctly', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Parties')).toBeInTheDocument();
      expect(screen.getByText('Dates')).toBeInTheDocument();
      expect(screen.getByText('Document type')).toBeInTheDocument();
      expect(screen.getByText('Key clauses')).toBeInTheDocument();
      expect(screen.getByText('Summary')).toBeInTheDocument();
    });
  });

  it('handles empty analysis data gracefully', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockEmptyAnalysis);

    render(<DocumentAnalysis documentId="doc-002" />);

    await waitFor(() => {
      expect(screen.getByText('Key Dates (0)')).toBeInTheDocument();
      expect(screen.getByText('No key dates identified')).toBeInTheDocument();
      
      expect(screen.getByText('Parties Involved (0)')).toBeInTheDocument();
      expect(screen.getByText('No parties identified')).toBeInTheDocument();
      
      expect(screen.getByText('Key Clauses (0)')).toBeInTheDocument();
      expect(screen.getByText('No key clauses identified')).toBeInTheDocument();
    });
  });

  it('shows low confidence scores with warning indicators', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockEmptyAnalysis);

    render(<DocumentAnalysis documentId="doc-002" />);

    await waitFor(() => {
      expect(screen.getByText('45%')).toBeInTheDocument(); // parties - low confidence
      expect(screen.getByText('30%')).toBeInTheDocument(); // dates - very low confidence
      expect(screen.getByText('55%')).toBeInTheDocument(); // document_type - low confidence
    });
  });

  it('uses preloaded analysis when provided', () => {
    render(<DocumentAnalysis documentId="doc-001" analysis={mockAnalysis} />);

    // Should not call the service when analysis is preloaded
    expect(documentService.getDocumentAnalysis).not.toHaveBeenCalled();
    
    // Should immediately show the analysis
    expect(screen.getByText('AI Document Analysis')).toBeInTheDocument();
    expect(screen.getByText('Employment Contract')).toBeInTheDocument();
  });

  it('displays error state when analysis fetch fails', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockRejectedValue(new Error('API Error'));

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load document analysis. Please try again.')).toBeInTheDocument();
    });
  });

  it('displays not found state when analysis is null', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(null as any);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('No analysis available for this document')).toBeInTheDocument();
    });
  });

  it('shows confidence explanation', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText(/Confidence scores indicate the AI's certainty/)).toBeInTheDocument();
      expect(screen.getByText(/Scores above 80% are considered highly reliable/)).toBeInTheDocument();
    });
  });

  it('expands accordions by default', async () => {
    vi.mocked(documentService.getDocumentAnalysis).mockResolvedValue(mockAnalysis);

    render(<DocumentAnalysis documentId="doc-001" />);

    await waitFor(() => {
      // Check that accordion content is visible (expanded by default)
      expect(screen.getByText('January 15, 2024')).toBeInTheDocument();
      expect(screen.getByText('Sarah Chen')).toBeInTheDocument();
      expect(screen.getByText('At-will employment clause')).toBeInTheDocument();
    });
  });
});