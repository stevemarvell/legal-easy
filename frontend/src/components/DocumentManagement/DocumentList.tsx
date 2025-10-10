import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Chip,
  Alert,
  CircularProgress,
  Divider,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Description as DocumentIcon,
  Email as EmailIcon,
  Gavel as LegalIcon,
  Assignment as ContractIcon,
  Visibility as ViewIcon,
  CheckCircle as AnalyzedIcon,
  Schedule as PendingIcon
} from '@mui/icons-material';
import { documentService } from '../../services/documentService';
import { Document } from '../../types/document';

interface DocumentListProps {
  caseId: string;
  onDocumentSelect?: (document: Document) => void;
  selectedDocumentId?: string;
  refreshTrigger?: number; // Add refresh trigger
  onDocumentsLoaded?: (documents: Document[]) => void; // Add callback for when documents are loaded
}

const DocumentList: React.FC<DocumentListProps> = ({ 
  caseId, 
  onDocumentSelect,
  selectedDocumentId,
  refreshTrigger,
  onDocumentsLoaded
}) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        setLoading(true);
        setError(null);
        const fetchedDocuments = await documentService.getCaseDocuments(caseId);
        setDocuments(fetchedDocuments);
        onDocumentsLoaded?.(fetchedDocuments);
      } catch (err) {
        console.error('Failed to fetch documents:', err);
        setError('Failed to load documents. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (caseId) {
      fetchDocuments();
    }
  }, [caseId, refreshTrigger]);

  const getDocumentIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'email':
        return <EmailIcon color="primary" />;
      case 'contract':
        return <ContractIcon color="primary" />;
      case 'legal brief':
        return <LegalIcon color="primary" />;
      default:
        return <DocumentIcon color="primary" />;
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  if (documents.length === 0) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Documents
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <Typography variant="body2" color="text.secondary" textAlign="center" py={4}>
            No documents found for this case
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box mb={2}>
        <Typography variant="subtitle1" gutterBottom>
          {documents.length} Documents
        </Typography>
        <Box display="flex" gap={1}>
          <Chip
            size="small"
            icon={<AnalyzedIcon />}
            label={documents.filter(doc => doc.analysis_completed).length}
            color="success"
            variant="outlined"
          />
          <Chip
            size="small"
            icon={<PendingIcon />}
            label={documents.filter(doc => !doc.analysis_completed).length}
            color="warning"
            variant="outlined"
          />
        </Box>
      </Box>
      
      {/* Document List */}
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <List disablePadding>
          {documents.map((document) => (
            <React.Fragment key={document.id}>
              <ListItem disablePadding>
                <ListItemButton
                  selected={selectedDocumentId === document.id}
                  onClick={() => onDocumentSelect?.(document)}
                  sx={{ 
                    borderRadius: 1,
                    mb: 0.5,
                    '&.Mui-selected': {
                      bgcolor: 'primary.50',
                      '&:hover': {
                        bgcolor: 'primary.100',
                      }
                    }
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 36 }}>
                    {getDocumentIcon(document.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Typography variant="body2" fontWeight="medium" noWrap>
                        {document.name}
                      </Typography>
                    }
                    secondary={
                      <Box>
                        <Typography variant="caption" color="text.secondary" display="block">
                          {document.type}
                        </Typography>
                        <Box display="flex" alignItems="center" gap={0.5} mt={0.5}>
                          {document.analysis_completed ? (
                            <AnalyzedIcon color="success" sx={{ fontSize: 12 }} />
                          ) : (
                            <PendingIcon color="warning" sx={{ fontSize: 12 }} />
                          )}
                          <Typography variant="caption" color="text.secondary">
                            {formatFileSize(document.size)}
                          </Typography>
                        </Box>
                      </Box>
                    }
                  />
                </ListItemButton>
              </ListItem>
            </React.Fragment>
          ))}
        </List>
      </Box>
    </Box>
  );
};

export default DocumentList;