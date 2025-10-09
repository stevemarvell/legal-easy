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
};