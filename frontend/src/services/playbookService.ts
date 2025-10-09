import { apiClient } from './api';
import { Playbook, CaseAssessment } from '../types/playbook';

export const playbookService = {
  async getAllPlaybooks(): Promise<Playbook[]> {
    const response = await apiClient.get<Playbook[]>('/api/playbooks/');
    return response.data;
  },

  async getPlaybook(caseType: string): Promise<Playbook> {
    const response = await apiClient.get<Playbook>(`/api/playbooks/${encodeURIComponent(caseType)}`);
    return response.data;
  },

  async getCaseAssessment(caseId: string): Promise<CaseAssessment> {
    const response = await apiClient.get<CaseAssessment>(`/api/playbooks/cases/${caseId}/assessment`);
    return response.data;
  },

  async getAppliedRules(caseId: string): Promise<any> {
    const response = await apiClient.get(`/api/playbooks/cases/${caseId}/applied-rules`);
    return response.data;
  },
};