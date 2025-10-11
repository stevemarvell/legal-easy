import { apiClient } from './api';
import { LegalSearchResult, LegalQuery } from '../types/api';

export const legalResearchService = {
  async searchLegalCorpus(query: LegalQuery): Promise<LegalSearchResult[]> {
    const response = await apiClient.post<LegalSearchResult[]>('/api/legal-research/search', query);
    return response.data;
  },
};