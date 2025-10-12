import { apiClient } from './api';
import { Document } from '../types/document';

export const documentsService = {
  async getCaseDocuments(caseId: string): Promise<Document[]> {
    const response = await apiClient.get<Document[]>(`/api/documents/cases/${caseId}/documents`);
    return response.data;
  },

  async getDocumentById(documentId: string): Promise<Document> {
    const response = await apiClient.get<Document>(`/api/documents/${documentId}`);
    return response.data;
  },



  async getAllDocuments(): Promise<Document[]> {
    // Get all documents across all cases
    const cases = ['case-001', 'case-002', 'case-003', 'case-004', 'case-005', 'case-006'];
    const allDocuments: Document[] = [];

    for (const caseId of cases) {
      try {
        const caseDocuments = await this.getCaseDocuments(caseId);
        allDocuments.push(...caseDocuments);
      } catch (error) {
        console.warn(`Failed to fetch documents for ${caseId}:`, error);
      }
    }

    return allDocuments;
  },



  async getDocumentContent(documentId: string): Promise<{ document_id: string; content: string; content_length: number }> {
    const response = await apiClient.get<{ document_id: string; content: string; content_length: number }>(`/api/documents/${documentId}/content`);
    return response.data;
  },
};