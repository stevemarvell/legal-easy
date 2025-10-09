import { apiClient } from './api';
import { Document, DocumentAnalysis } from '../types/document';

export const documentService = {
  async getCaseDocuments(caseId: string): Promise<Document[]> {
    const response = await apiClient.get<Document[]>(`/api/documents/cases/${caseId}/documents`);
    return response.data;
  },

  async getDocumentById(documentId: string): Promise<Document> {
    const response = await apiClient.get<Document>(`/api/documents/${documentId}`);
    return response.data;
  },

  async getDocumentAnalysis(documentId: string): Promise<DocumentAnalysis> {
    const response = await apiClient.get<DocumentAnalysis>(`/api/documents/${documentId}/analysis`);
    return response.data;
  },

  async analyzeDocument(documentId: string): Promise<DocumentAnalysis> {
    const response = await apiClient.post<DocumentAnalysis>(`/api/documents/${documentId}/analyze`);
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

  async clearAllAnalyses(): Promise<void> {
    const response = await apiClient.delete('/api/documents/analysis/all');
    return response.data;
  },
};