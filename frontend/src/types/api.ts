// Case types
export interface Case {
  id: string;
  title: string;
  case_type: string;
  client_name: string;
  status: 'Active' | 'Under Review' | 'Resolved';
  created_date: string;
  summary: string;
  key_parties: string[];
  documents: string[];
  playbook_id: string;
  // Optional fields for frontend compatibility
  description?: string;
  priority?: 'low' | 'medium' | 'high' | 'critical';
  created_at?: string;
  updated_at?: string;
}

export interface CaseStatistics {
  total_cases: number;
  active_cases: number;
  resolved_cases: number;
  under_review_cases: number;
  recent_activity_count: number;
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

export interface CaseAssessment {
  case_id: string;
  playbook_used: string;
  case_strength: 'Strong' | 'Moderate' | 'Weak';
  key_issues: string[];
  recommended_actions: string[];
  monetary_assessment?: [number, number];
  applied_rules: string[];
  reasoning: string;
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
  name: string; // Changed from filename to match backend
  case_id: string;
  type: string; // Changed from file_type to match backend
  size: number; // Changed from file_size to match backend
  upload_date: string;
  content_preview: string; // Added to match backend
  full_content_path?: string; // Added to match backend
  analysis_completed: boolean; // Changed from analysis_status to match backend
  // Legacy fields for backward compatibility
  filename?: string;
  file_type?: string;
  file_size?: number;
  analysis_status?: 'pending' | 'processing' | 'completed' | 'failed';
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
  case_type: string;
  name: string;
  description?: string;
  rules: PlaybookRule[];
  decision_tree: Record<string, any>;
  monetary_ranges: Record<string, MonetaryRange>;
  escalation_paths: string[];
}

export interface PlaybookRule {
  id: string;
  condition: string;
  action: string;
  weight: number;
  description: string;
  enabled?: boolean;
  priority?: number;
}

export interface MonetaryRange {
  range: [number, number];
  description: string;
  factors: string[];
}

export interface PlaybookResult {
  case_id: string;
  playbook_id: string;
  applied_rules: string[];
  recommendations: string[];
  case_strength: string;
  reasoning: string;
}

export interface PlaybookExecution {
  playbook_id: string;
  case_id: string;
  results: PlaybookResult[];
  execution_time: string;
  status: 'success' | 'partial' | 'failed';
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