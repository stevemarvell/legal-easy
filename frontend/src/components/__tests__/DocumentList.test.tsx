import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '../../test-utils';
import DocumentList from '../DocumentManagement/DocumentList';
import { documentService } from '../../services/documentService';
import { Document } from '../../types/document';

// Mock the document service
vi.mock('../../services/documentService', () => ({
  documentService: {
    getCaseDocuments: vi.fn(),
  },
}));

const mockDocuments: Document[] = [
  {
    id: 'doc-001',
    case_id: 'case-001',
    name: 'Employment Contract - Sarah Chen',
    type: 'Contract',
    size: 245760,
    upload_date: '2024-01-15T09:30:00Z',
    content_preview: 'EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...',
    analysis_completed: true,
  },
  {
    id: 'doc-002',
    case_id: 'case-001',
    name: 'Safety Incident Report',
    type: 'Email',
    size: 156432,
    upload_date: '2024-01-20T14:15:00Z',
    content_preview: 'Subject: Safety Incident Report - Workplace Accident...',
    analysis_completed: false,
  },
  {
    id: 'doc-003',
    case_id: 'case-001',
    name: 'Legal Brief - Employment Dispute',
    type: 'Legal Brief',
    size: 512000,
    upload_date: '2024-01-25T11:45:00Z',
    content_preview: 'LEGAL BRIEF - Employment Dispute Case...',
    analysis_completed: true,
  },
];

describe('DocumentList Component', () => {
  const mockOnDocumentSelect = vi.fn();
  const defaultProps = {
    caseId: 'case-001',
    onDocumentSelect: mockOnDocumentSelect,
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    vi.mocked(documentService.getCaseDocuments).mockImplementation(
      () => new Promise(() => {}) // Never resolves to keep loading state
    );

    render(<DocumentList {...defaultProps} />);
    
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('renders documents list when data is loaded', async () => {
    vi.mocked(documentService.getCaseDocuments).mockResolvedValue(mockDocuments);

    render(<DocumentList {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Documents (3)')).toBeInTheDocument();
    });

    // Check that all documents are rendered
    expect(screen.getByText('Employment Contract - Sarah Chen')).toBeInTheDocument();
    expect(screen.getByText('Safety Incident Report')).toBeInTheDocument();
    expect(screen.getByText('Legal Brief - Employment Dispute')).toBeInTheDocument();
  });

  it('displays analysis status indicators correctly', async () => {
    vi.mocked(documentService.getCaseDocuments).mockResolvedValue(mockDocuments);

    render(<DocumentList {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('2 Analyzed')).toBeInTheDocument();
      expect(screen.getByText('1 Pending')).toBeInTheDocument();
    });
  });

  it('shows document metadata correctly', async () => {
    vi.mocked(documentService.getCaseDocuments).mockResolvedValue(mockDocuments);

    render(<DocumentList {...defaultProps} />);

    await waitFor(() => {
      // Check document types
      expect(screen.getByText(/Contract/)).toBeInTheDocument();
      expect(screen.getByText(/Email/)).toBeInTheDocument();
      expect(screen.getByText(/Legal Brief/)).toBeInTheDocument();

      // Check file sizes (formatted)
      expect(screen.getByText(/240 KB/)).toBeInTheDocument();
      expect(screen.getByText(/153 KB/)).toBeInTheDocument();
      expect(screen.getByText(/500 KB/)).toBeInTheDocument();
    });
  });

  it('calls onDocumentSelect when document is clicked', async () => {
    vi.mocked(documentService.getCaseDocuments).mockResolvedValue(mockDocuments);

    render(<DocumentList {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Employment Contract - Sarah Chen')).toBeInTheDocument();
    });

    const documentButton = screen.getByText('Employment Contract - Sarah Chen').closest('button');
    expect(documentButton).toBeInTheDocument();

    fireEvent.click(documentButton!);

    expect(mockOnDocumentSelect).toHaveBeenCalledWith(mockDocuments[0]);
  });

  it('highlights selected document', async () => {
    vi.mocked(documentService.getCaseDocuments).mockResolvedValue(mockDocuments);

    render(<DocumentList {...defaultProps} selectedDocumentId="doc-001" />);

    await waitFor(() => {
      const selectedButton = screen.getByText('Employment Contract - Sarah Chen').closest('button');
      expect(selectedButton).toHaveClass('Mui-selected');
    });
  });

  it('displays empty state when no documents', async () => {
    vi.mocked(documentService.getCaseDocuments).mockResolvedValue([]);

    render(<DocumentList {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('No documents found for this case')).toBeInTheDocument();
    });
  });

  it('displays error state when API call fails', async () => {
    vi.mocked(documentService.getCaseDocuments).mockRejectedValue(new Error('API Error'));

    render(<DocumentList {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load documents. Please try again.')).toBeInTheDocument();
    });
  });

  it('shows content preview for documents', async () => {
    vi.mocked(documentService.getCaseDocuments).mockResolvedValue(mockDocuments);

    render(<DocumentList {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText(/EMPLOYMENT AGREEMENT between TechCorp Solutions/)).toBeInTheDocument();
      expect(screen.getByText(/Subject: Safety Incident Report/)).toBeInTheDocument();
    });
  });

  it('displays analysis completion status', async () => {
    vi.mocked(documentService.getCaseDocuments).mockResolvedValue(mockDocuments);

    render(<DocumentList {...defaultProps} />);

    await waitFor(() => {
      // Check for analysis status text
      expect(screen.getByText('2 Analyzed')).toBeInTheDocument();
      expect(screen.getByText('1 Pending')).toBeInTheDocument();
    });
  });
});