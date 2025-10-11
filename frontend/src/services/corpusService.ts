import { apiClient } from './api';
import { 
  CorpusItem, 
  CorpusCategory, 
  CorpusSearchResult, 
  ConceptAnalysisResult 
} from '../types/corpus';

export const corpusService = {
  /**
   * Browse corpus items by category
   */
  async browseCorpus(category?: string): Promise<CorpusItem[]> {
    const params = category ? { category } : {};
    const response = await apiClient.get<CorpusItem[]>('/api/corpus', { params });
    return response.data;
  },

  /**
   * Get all corpus categories with metadata
   */
  async getCategories(): Promise<Record<string, CorpusCategory>> {
    const response = await apiClient.get<Record<string, CorpusCategory>>('/api/corpus/categories');
    return response.data;
  },

  /**
   * Search corpus using concept-based search
   */
  async searchCorpus(
    query: string, 
    category?: string, 
    researchArea?: string
  ): Promise<CorpusSearchResult> {
    const params: Record<string, string> = { q: query };
    if (category) params.category = category;
    if (researchArea) params.research_area = researchArea;
    
    const response = await apiClient.get<CorpusSearchResult>('/api/corpus/search', { params });
    return response.data;
  },

  /**
   * Get specific corpus item with full content
   */
  async getCorpusItem(itemId: string): Promise<CorpusItem> {
    const response = await apiClient.get<CorpusItem>(`/api/corpus/${itemId}`);
    return response.data;
  },

  /**
   * Get related materials for a corpus item
   */
  async getRelatedMaterials(itemId: string): Promise<CorpusItem[]> {
    const response = await apiClient.get<CorpusItem[]>(`/api/corpus/${itemId}/related`);
    return response.data;
  },

  /**
   * Get research concept analysis
   */
  async getConceptAnalysis(): Promise<ConceptAnalysisResult> {
    const response = await apiClient.get<ConceptAnalysisResult>('/api/corpus/concepts');
    return response.data;
  }
};