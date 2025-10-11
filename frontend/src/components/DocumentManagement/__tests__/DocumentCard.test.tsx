import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import DocumentCard from '../DocumentCard';
import { Document } from '../../../types/document';

// Mock react-router-dom
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

const mockDocument: Document = {
  id: 'doc-001',
  name: 'Employment Contract - John Doe',
  case_id: 'case-001',
  type: 'Contract',
  size: 15420,
  upload_date: '2024-01-15T10:30:00Z',
  content_preview: 'EMPLOYMENT AGREEMENT between ABC Corp and John Doe...',
  analysis_completed: true
};

const renderDocumentCard = (props = {}) => {
  const defaultProps = {
    document: mockDocument,
    caseId: 'case-001',
    ...props
  };

  return render(
    <BrowserRouter>
      <DocumentCard {...defaultProps} />
    </BrowserRouter>
  );
};

describe('DocumentCard', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it('renders document information correctly', () => {
    renderDocumentCard();

    expect(screen.getByTestId('document-title')).toHaveTextContent('Employment Contract - John Doe');
    expect(screen.getByTestId('document-type')).toHaveTextContent('Contract');
    expect(screen.getByTestId('document-size')).toHaveTextContent('Size: 15.06 KB');
    expect(screen.getByTestId('document-upload-date')).toHaveTextContent('Uploaded: Jan 15, 2024');
  });

  it('shows analysis status correctly for analyzed document', () => {
    renderDocumentCard();

    const statusChip = screen.getByTestId('document-analysis-status');
    expect(statusChip).toHaveTextContent('Analyzed');
    expect(statusChip).toHaveAttribute('data-status', 'completed');
  });

  it('shows analysis status correctly for pending document', () => {
    const pendingDocument = { ...mockDocument, analysis_completed: false };
    renderDocumentCard({ document: pendingDocument });

    const statusChip = screen.getByTestId('document-analysis-status');
    expect(statusChip).toHaveTextContent('Pending');
    expect(statusChip).toHaveAttribute('data-status', 'pending');
  });

  it('displays content preview when available', () => {
    renderDocumentCard();

    expect(screen.getByTestId('document-preview')).toHaveTextContent(
      'EMPLOYMENT AGREEMENT between ABC Corp and John Doe...'
    );
  });

  it('truncates long content preview', () => {
    const longPreview = 'A'.repeat(150);
    const documentWithLongPreview = { ...mockDocument, content_preview: longPreview };
    renderDocumentCard({ document: documentWithLongPreview });

    const preview = screen.getByTestId('document-preview');
    expect(preview.textContent).toHaveLength(123); // 120 chars + "..."
    expect(preview.textContent).toEndWith('...');
  });

  it('navigates to document detail on card click', () => {
    renderDocumentCard();

    const card = screen.getByTestId('document-card');
    fireEvent.click(card);

    expect(mockNavigate).toHaveBeenCalledWith('/cases/case-001/documents/doc-001');
  });

  it('navigates to document detail without case context', () => {
    renderDocumentCard({ caseId: undefined });

    const card = screen.getByTestId('document-card');
    fireEvent.click(card);

    expect(mockNavigate).toHaveBeenCalledWith('/documents/doc-001');
  });

  it('navigates to document detail on view button click', () => {
    renderDocumentCard();

    const viewButton = screen.getByTestId('view-document-button');
    fireEvent.click(viewButton);

    expect(mockNavigate).toHaveBeenCalledWith('/cases/case-001/documents/doc-001');
  });

  it('prevents navigation when clicking on buttons', () => {
    renderDocumentCard();

    const viewButton = screen.getByTestId('view-document-button');
    fireEvent.click(viewButton);

    // Should only navigate once (from button click), not from card click
    expect(mockNavigate).toHaveBeenCalledTimes(1);
  });

  it('shows analyze button for unanalyzed documents', () => {
    const mockOnAnalyze = vi.fn();
    const pendingDocument = { ...mockDocument, analysis_completed: false };
    
    renderDocumentCard({ 
      document: pendingDocument, 
      onAnalyze: mockOnAnalyze 
    });

    const analyzeButton = screen.getByTestId('analyze-document-button');
    expect(analyzeButton).toBeInTheDocument();
    
    fireEvent.click(analyzeButton);
    expect(mockOnAnalyze).toHaveBeenCalledWith(pendingDocument);
  });

  it('does not show analyze button for analyzed documents', () => {
    const mockOnAnalyze = vi.fn();
    renderDocumentCard({ onAnalyze: mockOnAnalyze });

    expect(screen.queryByTestId('analyze-document-button')).not.toBeInTheDocument();
  });

  it('shows case info when requested', () => {
    renderDocumentCard({ showCaseInfo: true });

    expect(screen.getByText('Case: case-001')).toBeInTheDocument();
  });

  it('does not show case info by default', () => {
    renderDocumentCard();

    expect(screen.queryByText('Case: case-001')).not.toBeInTheDocument();
  });

  it('handles keyboard navigation', () => {
    renderDocumentCard();

    const card = screen.getByTestId('document-card');
    expect(card).toHaveAttribute('tabIndex', '0');
    expect(card).toHaveAttribute('role', 'button');
  });

  it('displays correct document type icons', () => {
    const contractDoc = { ...mockDocument, type: 'Contract' };
    const { rerender } = renderDocumentCard({ document: contractDoc });
    
    // Contract should show AssignmentIcon (we can't easily test the icon itself, but we can test the type)
    expect(screen.getByTestId('document-type')).toHaveTextContent('Contract');

    // Test email document
    const emailDoc = { ...mockDocument, type: 'Email' };
    rerender(
      <BrowserRouter>
        <DocumentCard document={emailDoc} caseId="case-001" />
      </BrowserRouter>
    );
    expect(screen.getByTestId('document-type')).toHaveTextContent('Email');
  });

  it('formats file sizes correctly', () => {
    const testCases = [
      { size: 0, expected: '0 Bytes' },
      { size: 1024, expected: '1 KB' },
      { size: 1048576, expected: '1 MB' },
      { size: 15420, expected: '15.06 KB' }
    ];

    testCases.forEach(({ size, expected }) => {
      const doc = { ...mockDocument, size };
      const { rerender } = renderDocumentCard({ document: doc });
      
      expect(screen.getByTestId('document-size')).toHaveTextContent(`Size: ${expected}`);
      
      rerender(<div />); // Clear between tests
    });
  });

  it('formats dates correctly', () => {
    renderDocumentCard();

    expect(screen.getByTestId('document-upload-date')).toHaveTextContent('Uploaded: Jan 15, 2024');
  });
});