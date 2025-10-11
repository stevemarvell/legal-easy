import React, { useState, useEffect } from 'react';
import {
  Box,
  Alert,
  CircularProgress,
  Typography,
  Chip
} from '@mui/material';
import {
  Description as DocumentIcon,
  CheckCircle as AnalyzedIcon,
  Schedule as PendingIcon
} from '@mui/icons-material';
import DocumentCard from './DocumentCard';
import { documentService } from '../../services/documentService';
import { Document } from '../../types/document';
import SharedLayout from '../layout/SharedLayout';

interface DocumentGridProps {
  caseId?: string;
  searchQuery?: string;
  onSearchChange?: (value: string) => void;
  showCaseInfo?: boolean;
  onDocumentAnalyze?: (document: Document) => void;
}

const DocumentGrid: React.FC<DocumentGridProps> = ({ 
  caseId, 
  searchQuery = '',
  onSearchChange,
  showCaseInfo = false,
  onDocumentAnalyze
}) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [filteredDocuments, setFilteredDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        setLoading(true);
        setError(null);
        
        let fetchedDocuments: Document[];
        if (caseId) {
          fetchedDocuments = await documentService.getCaseDocuments(caseId);
        } else {
          // For now, we'll fetch all documents by getting all cases and their documents
          // In a real app, you'd have a dedicated endpoint for all documents
          fetchedDocuments = [];
        }
        
        setDocuments(fetchedDocuments);
        setFilteredDocuments(fetchedDocuments);
      } catch (err) {
        console.error('Failed to fetch documents:', err);
        setError('Failed to load documents. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, [caseId]);

  useEffect(() => {
    if (!searchQuery.trim()) {
      setFilteredDocuments(documents);
    } else {
      const filtered = documents.filter(doc =>
        doc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        doc.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (doc.content_preview && doc.content_preview.toLowerCase().includes(searchQuery.toLowerCase()))
      );
      setFilteredDocuments(filtered);
    }
  }, [searchQuery, documents]);

  const handleAnalyzeDocument = async (document: Document) => {
    try {
      await documentService.analyzeDocument(document.id);
      
      // Update the document in the list
      setDocuments(prev => prev.map(doc => 
        doc.id === document.id 
          ? { ...doc, analysis_completed: true }
          : doc
      ));
      
      if (onDocumentAnalyze) {
        onDocumentAnalyze(document);
      }
    } catch (err) {
      console.error('Failed to analyze document:', err);
      // You might want to show a toast notification here
    }
  };

  const getAnalysisStats = () => {
    const total = filteredDocuments.length;
    const analyzed = filteredDocuments.filter(doc => doc.analysis_completed).length;
    const pending = total - analyzed;
    return { total, analyzed, pending };
  };

  const stats = getAnalysisStats();

  if (loading) {
    return (
      <SharedLayout
        title={caseId ? `Case ${caseId} Documents` : "All Documents"}
        subtitle="Legal document management and analysis"
        showSearchBar={true}
        searchPlaceholder="Search documents by name, type, or content..."
        searchValue={searchQuery}
        onSearchChange={onSearchChange}
      >
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress data-testid="loading-spinner" />
        </Box>
      </SharedLayout>
    );
  }

  return (
    <SharedLayout
      title={caseId ? `Case ${caseId} Documents` : "All Documents"}
      subtitle="Legal document management and analysis"
      showSearchBar={true}
      searchPlaceholder="Search documents by name, type, or content..."
      searchValue={searchQuery}
      onSearchChange={onSearchChange}
    >
      {/* Error State */}
      {error && (
        <Alert severity="error" sx={{ mb: 4 }} data-testid="error-message">
          {error}
        </Alert>
      )}

      {/* Analysis Statistics */}
      {filteredDocuments.length > 0 && (
        <Box display="flex" gap={2} mb={4}>
          <Chip
            icon={<DocumentIcon />}
            label={`${stats.total} Total`}
            color="primary"
            variant="outlined"
          />
          <Chip
            icon={<AnalyzedIcon />}
            label={`${stats.analyzed} Analyzed`}
            color="success"
            variant="outlined"
          />
          <Chip
            icon={<PendingIcon />}
            label={`${stats.pending} Pending`}
            color="warning"
            variant="outlined"
          />
        </Box>
      )}

      {/* Documents Grid */}
      {filteredDocuments.length === 0 && !loading ? (
        <Alert severity="info">
          {searchQuery ? 'No documents found matching your search.' : 'No documents found.'}
        </Alert>
      ) : (
        <Box 
          display="grid" 
          gridTemplateColumns={{ xs: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }} 
          gap={3}
          data-testid="documents-grid"
        >
          {filteredDocuments.map((document) => (
            <DocumentCard
              key={document.id}
              document={document}
              caseId={caseId}
              onAnalyze={handleAnalyzeDocument}
              showCaseInfo={showCaseInfo}
            />
          ))}
        </Box>
      )}
    </SharedLayout>
  );
};

export default DocumentGrid;