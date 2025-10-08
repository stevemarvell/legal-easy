import { apiRequest } from './api';
import { Case, CaseStatistics } from '../types/case';

export const caseService = {
  async getAllCases(): Promise<Case[]> {
    return apiRequest<Case[]>('/cases');
  },

  async getCaseById(caseId: string): Promise<Case> {
    return apiRequest<Case>(`/cases/${caseId}`);
  },

  async getCaseStatistics(): Promise<CaseStatistics> {
    return apiRequest<CaseStatistics>('/cases/statistics');
  },
};