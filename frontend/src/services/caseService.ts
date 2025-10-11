import { apiClient } from './api';
import { Case, CaseStatistics } from '../types/api';

export const caseService = {
  async getAllCases(): Promise<Case[]> {
    const response = await apiClient.get<Case[]>('/api/cases');
    return response.data;
  },

  async getCaseById(caseId: string): Promise<Case> {
    const response = await apiClient.get<Case>(`/api/cases/${caseId}`);
    return response.data;
  },

  async getCaseStatistics(): Promise<CaseStatistics> {
    const response = await apiClient.get<CaseStatistics>('/api/cases/statistics');
    return response.data;
  },
};