import { apiClient } from './api';
import { Playbook, CaseAssessment, ComprehensiveAnalysis } from '../types/playbook';

export const playbooksService = {
  /**
   * Get all available playbooks
   */
  async getAllPlaybooks(): Promise<Playbook[]> {
    const response = await apiClient.get<Playbook[]>('/api/playbooks/');
    return response.data;
  },

  /**
   * Get a specific playbook by case type
   */
  async getPlaybook(caseType: string): Promise<Playbook> {
    const response = await apiClient.get<Playbook>(`/api/playbooks/${encodeURIComponent(caseType)}`);
    return response.data;
  },

  /**
   * Match a playbook for a specific case type
   */
  async matchPlaybook(caseType: string): Promise<Playbook | null> {
    try {
      const response = await apiClient.get<Playbook>(`/api/playbooks/match/${encodeURIComponent(caseType)}`);
      return response.data;
    } catch (error: any) {
      if (error.status === 404) {
        return null; // No matching playbook found
      }
      throw error;
    }
  },

  /**
   * Get comprehensive case analysis using playbook
   */
  async getComprehensiveAnalysis(caseId: string): Promise<ComprehensiveAnalysis> {
    const response = await apiClient.get<ComprehensiveAnalysis>(`/api/playbooks/cases/${caseId}/comprehensive-analysis`);
    return response.data;
  },

  /**
   * Legacy method for backward compatibility
   */
  async getCaseAssessment(caseId: string): Promise<CaseAssessment> {
    const response = await apiClient.get<CaseAssessment>(`/api/playbooks/cases/${caseId}/assessment`);
    return response.data;
  },

  /**
   * Legacy method for backward compatibility
   */
  async getAppliedRules(caseId: string): Promise<any> {
    const response = await apiClient.get(`/api/playbooks/cases/${caseId}/applied-rules`);
    return response.data;
  },
};