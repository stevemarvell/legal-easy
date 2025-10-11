import { Case, Document, LegalSearchResult, CaseAnalysis, DocumentAnalysis } from '../types/api';

// Mock Cases
export const mockCases: Case[] = [
  {
    id: 'case-001',
    title: 'Employment Dispute - Sarah Chen',
    case_type: 'Employment Dispute',
    client_name: 'Sarah Chen',
    status: 'Active',
    created_date: '2024-01-15T10:00:00Z',
    summary: 'Unfair dismissal case involving safety violations',
    key_parties: ['Sarah Chen (Claimant)', 'TechCorp Solutions Ltd. (Respondent)'],
    documents: ['doc-001', 'doc-002'],
    playbook_id: 'employment-dispute',
    // Legacy fields for backward compatibility
    description: 'Unfair dismissal case involving safety violations',
    priority: 'high',
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2024-01-20T14:30:00Z',
  },
  {
    id: 'case-002',
    title: 'Software License Violation',
    case_type: 'Intellectual Property',
    client_name: 'TechStart Inc.',
    status: 'Under Review',
    created_date: '2024-01-10T09:00:00Z',
    summary: 'Intellectual property dispute over software licensing',
    key_parties: ['TechStart Inc. (Claimant)', 'SoftwareCorp Ltd. (Respondent)'],
    documents: ['doc-003'],
    playbook_id: 'intellectual-property',
    // Legacy fields for backward compatibility
    description: 'Intellectual property dispute over software licensing',
    priority: 'medium',
    created_at: '2024-01-10T09:00:00Z',
    updated_at: '2024-01-18T16:45:00Z',
  },
  {
    id: 'case-003',
    title: 'Contract Dispute - TechCorp',
    case_type: 'Contract Breach',
    client_name: 'TechCorp Solutions',
    status: 'Resolved',
    created_date: '2024-01-05T11:30:00Z',
    summary: 'Breach of contract in consulting services agreement',
    key_parties: ['TechCorp Solutions (Claimant)', 'ConsultingFirm LLC (Respondent)'],
    documents: ['doc-004'],
    playbook_id: 'contract-breach',
    // Legacy fields for backward compatibility
    description: 'Breach of contract in consulting services agreement',
    priority: 'low',
    created_at: '2024-01-05T11:30:00Z',
    updated_at: '2024-01-25T13:15:00Z',
  },
];

// Mock Documents
export const mockDocuments: Document[] = [
  {
    id: 'doc-001',
    name: 'Employment Contract - Sarah Chen',
    case_id: 'case-001',
    type: 'Contract',
    size: 15420,
    upload_date: '2024-01-15T10:30:00Z',
    content_preview: 'EMPLOYMENT AGREEMENT between TechCorp Solutions Ltd. and Sarah Chen...',
    analysis_completed: true,
    // Legacy fields for backward compatibility
    filename: 'employment_contract_sarah_chen.txt',
    file_type: 'text/plain',
    file_size: 15420,
    analysis_status: 'completed',
  },
  {
    id: 'doc-002',
    name: 'Termination Notice - Sarah Chen',
    case_id: 'case-001',
    type: 'Legal Brief',
    size: 8750,
    upload_date: '2024-01-12T14:15:00Z',
    content_preview: 'NOTICE OF TERMINATION - This letter serves as formal notice...',
    analysis_completed: true,
    // Legacy fields for backward compatibility
    filename: 'termination_notice_sarah_chen.txt',
    file_type: 'text/plain',
    file_size: 8750,
    analysis_status: 'completed',
  },
  {
    id: 'doc-003',
    name: 'Software License Agreement',
    case_id: 'case-002',
    type: 'Contract',
    size: 28750,
    upload_date: '2024-01-10T09:15:00Z',
    content_preview: 'SOFTWARE LICENSE AGREEMENT - This agreement governs the use...',
    analysis_completed: false,
    // Legacy fields for backward compatibility
    filename: 'software_license_agreement.txt',
    file_type: 'text/plain',
    file_size: 28750,
    analysis_status: 'pending',
  },
  {
    id: 'doc-004',
    name: 'Consulting Services Agreement',
    case_id: 'case-003',
    type: 'Contract',
    size: 22100,
    upload_date: '2024-01-05T12:00:00Z',
    content_preview: 'CONSULTING SERVICES AGREEMENT between TechCorp Solutions...',
    analysis_completed: true,
    // Legacy fields for backward compatibility
    filename: 'consulting_services_agreement.txt',
    file_type: 'text/plain',
    file_size: 22100,
    analysis_status: 'completed',
  },
];

// Mock Legal Search Results
export const mockSearchResults: LegalSearchResult[] = [
  {
    id: 'result-001',
    title: 'Employment Termination Precedent',
    content: 'Key precedent case regarding unfair dismissal in safety-related incidents...',
    source: 'Federal Court Database',
    relevance_score: 0.95,
    document_type: 'case_law',
    jurisdiction: 'Federal',
    date: '2023-08-15',
    url: 'https://example.com/case/001',
  },
  {
    id: 'result-002',
    title: 'Software Licensing Statute',
    content: 'Relevant statute regarding intellectual property rights in software licensing...',
    source: 'Legal Code Database',
    relevance_score: 0.88,
    document_type: 'statute',
    jurisdiction: 'Federal',
    date: '2023-12-01',
  },
];

// Mock Case Analysis
export const mockCaseAnalysis: CaseAnalysis = {
  case_id: 'case-001',
  summary: 'Employment termination case with strong evidence of wrongful dismissal',
  key_findings: [
    'Employee terminated immediately after reporting safety violations',
    'No prior disciplinary actions on record',
    'Company failed to follow proper termination procedures',
  ],
  recommendations: [
    'Pursue unfair dismissal claim',
    'Seek reinstatement and back pay',
    'Consider whistleblower protection claims',
  ],
  risk_assessment: 'low',
  estimated_value: 75000,
  timeline: [
    {
      date: '2024-01-10',
      event: 'Safety violation reported',
      description: 'Employee reported unsafe working conditions to management',
    },
    {
      date: '2024-01-12',
      event: 'Termination notice',
      description: 'Employee received termination notice citing performance issues',
    },
  ],
};

// Mock Document Analysis
export const mockDocumentAnalysis: DocumentAnalysis = {
  document_id: 'doc-001',
  summary: 'Standard employment contract with notice period clause',
  key_points: [
    'Employment relationship with notice period established',
    'Confidentiality agreement included',
    'Non-compete clause for 6 months post-employment',
  ],
  entities: [
    { text: 'Sarah Chen', type: 'person', confidence: 0.99 },
    { text: 'TechCorp Inc.', type: 'organization', confidence: 0.95 },
    { text: '$65,000', type: 'money', confidence: 0.92 },
  ],
  sentiment: 'neutral',
  confidence_score: 0.87,
};

// Mock API responses
export const mockApiResponses = {
  '/api/cases': {
    data: mockCases,
    status: 200,
  },
  '/api/documents': {
    data: mockDocuments,
    status: 200,
  },
  '/api/legal-research/search': {
    data: {
      results: mockSearchResults,
      total_count: mockSearchResults.length,
      query: 'employment termination',
      processing_time: 0.45,
    },
    status: 200,
  },
  '/api/cases/case-001/analysis': {
    data: mockCaseAnalysis,
    status: 200,
  },
  '/api/documents/doc-001/analysis': {
    data: mockDocumentAnalysis,
    status: 200,
  },
};

// Mock fetch function for testing
export const mockFetch = (url: string, options?: RequestInit) => {
  const endpoint = url.replace('http://localhost:8000', '');
  const response = mockApiResponses[endpoint as keyof typeof mockApiResponses];
  
  if (response) {
    return Promise.resolve({
      ok: true,
      status: response.status,
      json: () => Promise.resolve(response.data),
    } as Response);
  }
  
  return Promise.resolve({
    ok: false,
    status: 404,
    json: () => Promise.resolve({ error: 'Not found' }),
  } as Response);
};