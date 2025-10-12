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
import { documentsService } from '../../services/documentsService'
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
          fetchedDocuments = await documentsService.getCaseDocuments(caseId);
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
        </Box>
      )}
    </SharedLayout>
  );
};

export default DocumentGrid;