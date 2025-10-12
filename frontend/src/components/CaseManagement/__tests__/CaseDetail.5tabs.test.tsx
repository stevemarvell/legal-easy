import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import CaseDetail from '../CaseDetail';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { apiClient } from '../../../services';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { apiClient } from '../../../services';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { beforeEach } from 'node:test';
import { describe } from 'node:test';

// Mock the API client
vi.mock('../../../services/api', () => ({
  apiClient: {
    get: vi.fn()
  }
}));

// Mock react-router-dom
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ caseId: 'case-001' }),
    useNavigate: () => mockNavigate,
  };
});

// Mock ReactMarkdown
vi.mock('react-markdown', () => ({
  default: ({ children }: { children: string }) => <div data-testid="markdown-content">{children}</div>
}));

const mockCase = {
  id: 'case-001',
  title: 'Test Employment Case',
  case_type: 'Employment Dispute',
  client_name: 'John Doe',
  status: 'Active' as const,
  created_date: '2024-01-15T00:00:00Z',
  summary: 'Test case summary for employment dispute',
  key_parties: ['John Doe (Claimant)', 'ABC Corp (Respondent)'],
  documents: ['doc-001', 'doc-002'],
  playbook_id: 'employment-dispute',
  description: '## Case Background\n\nThis is a detailed case description with markdown formatting.'
};

const mockDocuments = [
  {
    id: 'doc-001',
    name: 'Employment Contract',
    case_id: 'case-001',
    type: 'Contract',
    size: 15420,
    upload_date: '2024-01-15T00:00:00Z',
    content_preview: 'This employment contract outlines the terms and conditions...',
    analysis_completed: true
  },
  {
    id: 'doc-002',
    name: 'Termination Letter',
    case_id: 'case-001',
    type: 'Email',
    size: 8500,
    upload_date: '2024-01-16T00:00:00Z',
    content_preview: 'Dear John, we regret to inform you that your employment...',
    analysis_completed: false
  }
];

describe('CaseDetail 5-Tab Interface', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    const { apiClient } = require('../../../services/api');
    vi.mocked(apiClient.get).mockImplementation((url: string) => {
      if (url.includes('/api/cases/case-001')) {
        return Promise.resolve({ data: mockCase, status: 200 });
      }
      if (url.includes('/api/documents/cases/case-001/documents')) {
        return Promise.resolve({ data: mockDocuments, status: 200 });
      }
      return Promise.reject(new Error('Not found'));
    });
  });

  const renderCaseDetail = () => {
    return render(
      <BrowserRouter>
        <CaseDetail />
      </BrowserRouter>
    );
  };

  describe('Tab Structure', () => {
    it('displays all 5 tabs with correct labels', async () => {
      renderCaseDetail();

      await waitFor(() => {
        expect(screen.getByTestId('overview-tab')).toBeInTheDocument();
        expect(screen.getByTestId('details-tab')).toBeInTheDocument();
        expect(screen.getByTestId('documents-analysis-tab')).toBeInTheDocument();
        expect(screen.getByTestId('research-details-tab')).toBeInTheDocument();
        expect(screen.getByTestId('playbook-tab')).toBeInTheDocument();
      });

      expect(screen.getByText('Overview')).toBeInTheDocument();
      expect(screen.getByText('Details')).toBeInTheDocument();
      expect(screen.getByText('Documents with Analysis')).toBeInTheDocument();
      expect(screen.getByText('Research with Details')).toBeInTheDocument();
      expect(screen.getByText('Playbook')).toBeInTheDocument();
    });

    it('shows Overview tab content by default', async () => {
      renderCaseDetail();

      await waitFor(() => {
        expect(screen.getByTestId('case-overview')).toBeInTheDocument();
      });

      expect(screen.getByText('Case Overview')).toBeInTheDocument();
      expect(screen.getByTestId('case-client')).toHaveTextContent('John Doe');
      expect(screen.getByTestId('case-type')).toHaveTextContent('Employment Dispute');
      expect(screen.getByTestId('case-summary')).toHaveTextContent('Test case summary for employment dispute');
    });
  });

  describe('Overview Tab', () => {
    it('displays essential case information without fluff', async () => {
      renderCaseDetail();

      await waitFor(() => {
        expect(screen.getByTestId('case-overview')).toBeInTheDocument();
      });

      // Check essential information is displayed
      expect(screen.getByTestId('case-client')).toHaveTextContent('John Doe');
      expect(screen.getByTestId('case-type')).toHaveTextContent('Employment Dispute');
      expect(screen.getByTestId('case-created-date')).toHaveTextContent('15/01/2024');
      expect(screen.getByTestId('case-playbook')).toHaveTextContent('Employment Law Playbook');
      expect(screen.getByTestId('case-summary')).toHaveTextContent('Test case summary for employment dispute');

      // Check key parties section
      expect(screen.getByTestId('key-parties-section')).toBeInTheDocument();
      expect(screen.getByText('John Doe (Claimant)')).toBeInTheDocument();
      expect(screen.getByText('ABC Corp (Respondent)')).toBeInTheDocument();
    });

    it('does not display fabricated or fluff content', async () => {
      renderCaseDetail();

      await waitFor(() => {
        expect(screen.getByTestId('case-overview')).toBeInTheDocument();
      });

      // Ensure no generic fluff text is present
      expect(screen.queryByText(/lorem ipsum/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/placeholder/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/sample/i)).not.toBeInTheDocument();
    });
  });

  describe('Details Tab', () => {
    it('displays comprehensive case metadata when available', async () => {
      renderCaseDetail();

      // Click Details tab
      fireEvent.click(screen.getByTestId('details-tab'));

      await waitFor(() => {
        expect(screen.getByTestId('details-tab-content')).toBeInTheDocument();
      });

      expect(screen.getByText('Comprehensive Case Details')).toBeInTheDocument();
      expect(screen.getByTestId('case-full-description')).toBeInTheDocument();
      expect(screen.getByTestId('markdown-content')).toHaveTextContent('## Case Background');
    });

    it('shows appropriate message when no detailed description available', async () => {
      const caseWithoutDescription = { ...mockCase, description: undefined };
      vi.mocked(apiClient.get).mockImplementation((url: string) => {
        if (url.includes('/api/cases/case-001')) {
          return Promise.resolve({ data: caseWithoutDescription, status: 200 });
        }
        if (url.includes('/api/documents/cases/case-001/documents')) {
          return Promise.resolve({ data: mockDocuments, status: 200 });
        }
        return Promise.reject(new Error('Not found'));
      });

      renderCaseDetail();

      fireEvent.click(screen.getByTestId('details-tab'));

      await waitFor(() => {
        expect(screen.getByText('No detailed description available for this case')).toBeInTheDocument();
      });
    });
  });

  describe('Documents with Analysis Tab', () => {
    it('displays documents and their analysis status', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('documents-analysis-tab'));

      await waitFor(() => {
        expect(screen.getByTestId('documents-analysis-tab-content')).toBeInTheDocument();
      });

      expect(screen.getByText('Documents with Analysis')).toBeInTheDocument();
      expect(screen.getByText('2 documents')).toBeInTheDocument();
      expect(screen.getByText('1/2 analyzed')).toBeInTheDocument();

      // Check individual documents
      expect(screen.getByText('Employment Contract')).toBeInTheDocument();
      expect(screen.getByText('Termination Letter')).toBeInTheDocument();

      // Check analysis status
      const analysisStatuses = screen.getAllByTestId('document-analysis-status');
      expect(analysisStatuses).toHaveLength(2);
    });

    it('shows analysis results for completed documents', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('documents-analysis-tab'));

      await waitFor(() => {
        expect(screen.getByTestId('analysis-results')).toBeInTheDocument();
      });

      expect(screen.getByText('Analysis Results')).toBeInTheDocument();
      expect(screen.getByText('85% confidence')).toBeInTheDocument();
    });

    it('provides action buttons for document management', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('documents-analysis-tab'));

      await waitFor(() => {
        expect(screen.getByText('View Documents')).toBeInTheDocument();
        expect(screen.getByText('Analyze All Pending')).toBeInTheDocument();
      });
    });
  });

  describe('Research with Details Tab', () => {
    it('displays research generation prompt when no research exists', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('research-details-tab'));

      await waitFor(() => {
        expect(screen.getByTestId('research-details-tab-content')).toBeInTheDocument();
      });

      expect(screen.getByText('Research with Details')).toBeInTheDocument();
      expect(screen.getByText('Generate Research List')).toBeInTheDocument();
      expect(screen.getByText(/Generate a comprehensive research list/)).toBeInTheDocument();
    });

    it('provides factual description without fluff', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('research-details-tab'));

      await waitFor(() => {
        const description = screen.getByText(/Generate a comprehensive research list based on case files/);
        expect(description).toBeInTheDocument();
      });

      // Ensure description is factual and specific
      expect(screen.getByText(/identify key legal concepts, relevant precedents, applicable statutes/)).toBeInTheDocument();
    });
  });

  describe('Playbook Tab', () => {
    it('displays playbook decision interface', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('playbook-tab'));

      await waitFor(() => {
        expect(screen.getByTestId('playbook-tab-content')).toBeInTheDocument();
      });

      expect(screen.getByText('Playbook Decision Tree')).toBeInTheDocument();
      expect(screen.getByText('Employment Law Playbook')).toBeInTheDocument();
      expect(screen.getByText('Start Claude Decision Session')).toBeInTheDocument();
    });

    it('shows factual content without fabricated details', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('playbook-tab'));

      await waitFor(() => {
        const description = screen.getByText(/Start a Claude-driven playbook decision session/);
        expect(description).toBeInTheDocument();
      });

      // Ensure content is factual and specific to functionality
      expect(screen.getByText(/systematically work through the decision tree with AI assistance/)).toBeInTheDocument();
    });
  });

  describe('Claude Decision Prompting', () => {
    it('starts decision session and shows current decision', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('playbook-tab'));

      await waitFor(() => {
        const startButton = screen.getByText('Start Claude Decision Session');
        fireEvent.click(startButton);
      });

      await waitFor(() => {
        expect(screen.getByTestId('playbook-decision-interface')).toBeInTheDocument();
      });

      expect(screen.getByText('Current Decision')).toBeInTheDocument();
      expect(screen.getByText('What is the primary legal issue in this case?')).toBeInTheDocument();
    });
  });

  describe('Interface Consistency', () => {
    it('maintains consistent styling across all tabs', async () => {
      renderCaseDetail();

      // Check each tab has consistent header structure
      const tabs = ['overview-tab', 'details-tab', 'documents-analysis-tab', 'research-details-tab', 'playbook-tab'];
      
      for (const tabTestId of tabs) {
        const tab = screen.getByTestId(tabTestId);
        expect(tab).toHaveAttribute('role', 'tab');
      }
    });

    it('shows loading states appropriately', async () => {
      // Mock delayed API response
      vi.mocked(apiClient.get).mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({ data: mockCase, status: 200 }), 100))
      );

      renderCaseDetail();

      expect(screen.getByRole('progressbar')).toBeInTheDocument();

      await waitFor(() => {
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
      });
    });

    it('handles errors gracefully', async () => {
      const { apiClient } = require('../../../services/api');
      vi.mocked(apiClient.get).mockRejectedValue(new Error('API Error'));

      renderCaseDetail();

      await waitFor(() => {
        expect(screen.getByText(/Failed to load case details/)).toBeInTheDocument();
      });
    });
  });

  describe('Navigation and Interaction', () => {
    it('allows switching between tabs', async () => {
      renderCaseDetail();

      await waitFor(() => {
        expect(screen.getByTestId('case-overview')).toBeInTheDocument();
      });

      // Switch to Details tab
      fireEvent.click(screen.getByTestId('details-tab'));
      expect(screen.getByTestId('details-tab-content')).toBeInTheDocument();

      // Switch to Documents tab
      fireEvent.click(screen.getByTestId('documents-analysis-tab'));
      expect(screen.getByTestId('documents-analysis-tab-content')).toBeInTheDocument();
    });

    it('navigates to document details when document links are clicked', async () => {
      renderCaseDetail();

      fireEvent.click(screen.getByTestId('documents-analysis-tab'));

      await waitFor(() => {
        const documentLink = screen.getByTestId('document-link');
        fireEvent.click(documentLink);
      });

      expect(mockNavigate).toHaveBeenCalledWith('/cases/case-001/documents/doc-001');
    });
  });
});