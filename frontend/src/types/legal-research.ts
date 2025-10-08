export interface SearchResult {
  content: string;
  source_document: string;
  relevance_score: number;
  document_type: string;
  citation: string;
}

export interface LegalClause {
  id: string;
  content: string;
  source_document: string;
  legal_area: string;
  clause_type: string;
  relevance_score?: number;
}

export interface SearchQuery {
  query: string;
  filters?: Record<string, string>;
  limit?: number;
}