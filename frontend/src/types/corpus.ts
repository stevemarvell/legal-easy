// Corpus types based on backend models and design document

export interface CorpusItem {
  id: string;
  title: string;
  category: 'contracts' | 'clauses' | 'precedents' | 'statutes';
  content?: string; // Optional for browsing, required for full item view
  legal_concepts: string[];
  related_items: string[];
  metadata: Record<string, any>;
  
  // Additional fields from the data structure
  filename?: string;
  document_type?: string;
  research_areas: string[];
  description?: string;
}

export interface CorpusCategory {
  name: string;
  description: string;
  document_ids: string[];
}

export interface LegalConcept {
  id: string;
  name: string;
  definition: string;
  related_concepts: string[];
  corpus_references: string[];
}

export interface CorpusSearchResult {
  items: CorpusItem[];
  total_count: number;
  query: string;
  categories_found: string[];
  research_areas_found: string[];
}

export interface ConceptAnalysisResult {
  concepts: LegalConcept[];
  total_concepts: number;
  categories_analyzed: string[];
  research_areas: string[];
}

// UI-specific types
export interface CorpusCategoryInfo {
  id: 'contracts' | 'clauses' | 'precedents' | 'statutes';
  name: string;
  description: string;
  icon: React.ReactNode;
  count?: number;
}