// Case types
export interface Case {
  id: string;
  title: string;
  description: string;
  status: 'active' | 'pending' | 'resolved' | 'closed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  case_type: string;
  created_at: string;
  updated_at: string;
  documents?: Document[];
}

export interface CaseAnalysis {
  case_id: string;
  summary: string;
  key_findings: string[];
  recommendations: string[];
  risk_assessment: 'low' | 'medium' | 'high';
  estimated_value?: number;
  timeline?: TimelineEvent[];
}

export interface TimelineEvent {
  date: string;
  event: string;
  description: string;
  document_reference?: string;
}

// Document types
export interface Document {
  id: string;
  filename: string;
  case_id: string;
  file_type: string;
  file_size: number;
  upload_date: string;
  analysis_status: 'pending' | 'processing' | 'completed' | 'failed';
  content?: string;
}

export interface DocumentAnalysis {
  document_id: string;
  summary: string;
  key_points: string[];
  entities: Entity[];
  sentiment: 'positive' | 'negative' | 'neutral';
  confidence_score: number;
}

export interface Entity {
  text: string;
  type: 'person' | 'organization' | 'date' | 'money' | 'location' | 'other';
  confidence: number;
}

// Legal Research types
export interface LegalQuery {
  query: string;
  filters?: {
    jurisdiction?: string;
    date_range?: {
      start: string;
      end: string;
    };
    document_types?: string[];
  };
}

export interface LegalSearchResult {
  id: string;
  title: string;
  content: string;
  source: string;
  relevance_score: number;
  document_type: 'case_law' | 'statute' | 'regulation' | 'contract' | 'other';
  jurisdiction?: string;
  date?: string;
  url?: string;
}

export interface LegalSearchResponse {
  results: LegalSearchResult[];
  total_count: number;
  query: string;
  processing_time: number;
}

// Playbook types
export interface Playbook {
  id: string;
  name: string;
  description: string;
  rules: PlaybookRule[];
  created_at: string;
  updated_at: string;
}

export interface PlaybookRule {
  id: string;
  condition: string;
  action: string;
  priority: number;
  enabled: boolean;
}

export interface PlaybookExecution {
  playbook_id: string;
  case_id: string;
  results: PlaybookResult[];
  execution_time: string;
  status: 'success' | 'partial' | 'failed';
}

export interface PlaybookResult {
  rule_id: string;
  matched: boolean;
  action_taken?: string;
  confidence: number;
  details?: any;
}

// API Response wrappers
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: any;
}