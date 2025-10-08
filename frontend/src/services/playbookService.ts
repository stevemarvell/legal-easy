import { apiRequest } from './api';
import { Playbook, CaseAssessment } from '../types/playbook';

export const playbookService = {
  async getPlaybook(caseType: string): Promise<Playbook> {
    return apiRequest<Playbook>(`/playbooks/${caseType}`);
  },

  async getCaseAssessment(caseId: string): Promise<CaseAssessment> {
    return apiRequest<CaseAssessment>(`/playbooks/cases/${caseId}/assessment`);
  },
};