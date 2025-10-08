import { apiRequest } from './api';
import { SearchResult, SearchQuery } from '../types/legal-research';

export const legalResearchService = {
  async searchLegalCorpus(query: SearchQuery): Promise<SearchResult[]> {
    return apiRequest<SearchResult[]>('/legal-research/search', {
      method: 'POST',
      body: JSON.stringify(query),
    });
  },
};