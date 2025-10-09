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
}

const DocumentList: React.FC<DocumentListProps> = ({ 
  caseId, 
  onDocumentSelect,
  selectedDocumentId 
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
  }, [caseId]);

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
    return new Date(dateString).toLocaleDateString('en-US', {
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
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">
            Documents ({documents.length})
          </Typography>
          <Box display="flex" gap={1}>
            <Chip
              size="small"
              icon={<AnalyzedIcon />}
              label={`${documents.filter(doc => doc.analysis_completed).length} Analyzed`}
              color="success"
              variant="outlined"
            />
            <Chip
              size="small"
              icon={<PendingIcon />}
              label={`${documents.filter(doc => !doc.analysis_completed).length} Pending`}
              color="warning"
              variant="outlined"
            />
          </Box>
        </Box>
        
        <Divider sx={{ mb: 2 }} />
        
        <List disablePadding>
          {documents.map((document, index) => (
            <React.Fragment key={document.id}>
              <ListItem
                disablePadding
                secondaryAction={
                  <Box display="flex" alignItems="center" gap={1}>
                    {document.analysis_completed ? (
                      <Tooltip title="AI Analysis Complete">
                        <AnalyzedIcon color="success" fontSize="small" />
                      </Tooltip>
                    ) : (
                      <Tooltip title="Analysis Pending">
                        <PendingIcon color="warning" fontSize="small" />
                      </Tooltip>
                    )}
                    {onDocumentSelect && (
                      <Tooltip title="View Document">
                        <IconButton
                          size="small"
                          onClick={() => onDocumentSelect(document)}
                        >
                          <ViewIcon />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                }
              >
                <ListItemButton
                  selected={selectedDocumentId === document.id}
                  onClick={() => onDocumentSelect?.(document)}
                  sx={{ pr: 8 }}
                >
                  <ListItemIcon>
                    {getDocumentIcon(document.type)}
                  </ListItemIcon>
                  <ListItemText
                    primary={document.name}
                    secondary={
                      <Box component="span">
                        <Typography variant="caption" display="block">
                          {document.type} • {formatFileSize(document.size)} • {formatDate(document.upload_date)}
                        </Typography>
                        {document.content_preview && (
                          <Typography 
                            variant="caption" 
                            color="text.secondary"
                            sx={{ 
                              display: '-webkit-box',
                              WebkitLineClamp: 2,
                              WebkitBoxOrient: 'vertical',
                              overflow: 'hidden',
                              mt: 0.5
                            }}
                          >
                            {document.content_preview}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                </ListItemButton>
              </ListItem>
              {index < documents.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default DocumentList;