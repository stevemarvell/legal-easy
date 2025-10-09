export interface Document {
  id: string;
  case_id: string;
  name: string;
  type: string; // "Contract", "Email", "Legal Brief", "Evidence"
  size: number;
  upload_date: string;
  content_preview: string;
  analysis_completed: boolean;
}

export interface DocumentAnalysis {
  document_id: string;
  key_dates: string[];
  parties_involved: string[];
  document_type: string;
  summary: string;
  key_clauses: string[];
  legal_significance?: string[];
  potential_issues?: string[];
  confidence_scores: Record<string, number>;
}

export interface KeyInformation {
  dates: string[];
  parties: string[];
  amounts: string[];
  legal_concepts: string[];
  confidence: number;
}