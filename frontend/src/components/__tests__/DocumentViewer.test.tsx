import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '../../test-utils';
import DocumentViewer from '../DocumentManagement/DocumentViewer';
import { documentService } from '../../services/documentService';
import { Document } from '../../types/document';

// Mock the document service
vi.mock('../../services/documentService', () => ({
  documentService: {
    getDocumentById: vi.fn(),
  },
}));

const mockDocument: Document = {
  id: 'doc-001',
  case_id: 'case-001',
  name: 'Employment Contract - Sarah Chen',
  type: 'Contract',
  size: 245760,
  upload_date: '2024-01-15T09:30:00Z',
  content_preview: 'EMPLOYMENT AGREEMENT\n\nThis agreement is between TechCorp Solutions Ltd. and Sarah Chen for the position of Senior Safety Engineer.',
  analysis_completed: true,
};

const mockDocumentPending: Document = {
  ...mockDocument,
  id: 'doc-002',
  name: 'Pending Analysis Document',
  analysis_completed: false,
};

describe('DocumentViewer Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    vi.mocked(documentService.getDocumentById).mockImplementation(
      () => new Promise(() => {}) // Never resolves to keep loading state
    );

    render(<DocumentViewer documentId="doc-001" />);
    
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('renders document information when loaded', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocument);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Employment Contract - Sarah Chen')).toBeInTheDocument();
      expect(screen.getByText('doc-001')).toBeInTheDocument();
    });
  });

  it('displays document metadata correctly', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocument);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Contract')).toBeInTheDocument();
      expect(screen.getByText('240 KB')).toBeInTheDocument();
      expect(screen.getByText(/January 15, 2024/)).toBeInTheDocument();
    });
  });

  it('shows analysis complete status for analyzed documents', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocument);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('AI Analysis Complete')).toBeInTheDocument();
      expect(screen.getByText(/AI analysis is complete/)).toBeInTheDocument();
    });
  });

  it('shows analysis pending status for unanalyzed documents', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocumentPending);

    render(<DocumentViewer documentId="doc-002" />);

    await waitFor(() => {
      expect(screen.getByText('Analysis Pending')).toBeInTheDocument();
      expect(screen.getByText(/This document is pending AI analysis/)).toBeInTheDocument();
    });
  });

  it('displays document preview content', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocument);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText(/EMPLOYMENT AGREEMENT/)).toBeInTheDocument();
      expect(screen.getByText(/TechCorp Solutions Ltd. and Sarah Chen/)).toBeInTheDocument();
    });
  });

  it('renders tabs correctly', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocument);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Document Preview')).toBeInTheDocument();
      expect(screen.getByText('AI Analysis')).toBeInTheDocument();
    });
  });

  it('enables AI Analysis tab only for analyzed documents', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocument);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      const analysisTab = screen.getByText('AI Analysis').closest('button');
      expect(analysisTab).not.toHaveAttribute('disabled');
    });
  });

  it('disables AI Analysis tab for pending documents', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocumentPending);

    render(<DocumentViewer documentId="doc-002" />);

    await waitFor(() => {
      const analysisTab = screen.getByText('AI Analysis').closest('button');
      expect(analysisTab).toHaveAttribute('disabled');
    });
  });

  it('switches between tabs correctly', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(mockDocument);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Document Preview')).toBeInTheDocument();
    });

    // Initially should show preview tab content
    expect(screen.getByText('Document Information')).toBeInTheDocument();

    // Click on AI Analysis tab
    const analysisTab = screen.getByText('AI Analysis').closest('button');
    fireEvent.click(analysisTab!);

    // Should now show analysis content (DocumentAnalysis component)
    await waitFor(() => {
      expect(screen.getByText('AI Document Analysis')).toBeInTheDocument();
    });
  });

  it('uses preloaded document when provided', () => {
    render(<DocumentViewer documentId="doc-001" document={mockDocument} />);

    // Should not call the service when document is preloaded
    expect(documentService.getDocumentById).not.toHaveBeenCalled();
    
    // Should immediately show the document
    expect(screen.getByText('Employment Contract - Sarah Chen')).toBeInTheDocument();
  });

  it('displays error state when document fetch fails', async () => {
    vi.mocked(documentService.getDocumentById).mockRejectedValue(new Error('API Error'));

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load document. Please try again.')).toBeInTheDocument();
    });
  });

  it('displays not found state when document is null', async () => {
    vi.mocked(documentService.getDocumentById).mockResolvedValue(null as any);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('Document not found')).toBeInTheDocument();
    });
  });

  it('handles missing content preview gracefully', async () => {
    const documentWithoutPreview = { ...mockDocument, content_preview: '' };
    vi.mocked(documentService.getDocumentById).mockResolvedValue(documentWithoutPreview);

    render(<DocumentViewer documentId="doc-001" />);

    await waitFor(() => {
      expect(screen.getByText('No preview available for this document')).toBeInTheDocument();
    });
  });
});