import { apiRequest } from './api';
import { Document, DocumentAnalysis } from '../types/document';

export const documentService = {
  async getCaseDocuments(caseId: string): Promise<Document[]> {
    return apiRequest<Document[]>(`/documents/cases/${caseId}/documents`);
  },

  async getDocumentById(documentId: string): Promise<Document> {
    return apiRequest<Document>(`/documents/${documentId}`);
  },

  async getDocumentAnalysis(documentId: string): Promise<DocumentAnalysis> {
    return apiRequest<DocumentAnalysis>(`/documents/${documentId}/analysis`);
  },
};