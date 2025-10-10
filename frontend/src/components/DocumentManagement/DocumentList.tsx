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
  Tooltip,
  Paper
} from '@mui/material';
import {
  Description as DocumentIcon,
  Email as EmailIcon,
  Gavel as LegalIcon,
  Assignment as ContractIcon,
  Visibility as ViewIcon,
  CheckCircle as AnalyzedIcon,
  Schedule as PendingIcon,
  Folder as FolderIcon,
  Assessment as AssessmentIcon,
  CalendarToday as CalendarIcon
} from '@mui/icons-material';
import { documentService } from '../../services/documentService';
import { caseService } from '../../services/caseService';
import { Document } from '../../types/document';
import { Case } from '../../types/case';

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
  const [caseInfo, setCaseInfo] = useState<Case | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch documents first
        const fetchedDocuments = await documentService.getCaseDocuments(caseId);
        setDocuments(fetchedDocuments);
        onDocumentsLoaded?.(fetchedDocuments);
        
        // Try to fetch case info, but don't fail if it doesn't work
        try {
          const fetchedCase = await caseService.getCaseById(caseId);
          setCaseInfo(fetchedCase);
        } catch (caseErr) {
          console.warn('Failed to fetch case info:', caseErr);
          // Continue without case info - the component will still work
        }
      } catch (err) {
        console.error('Failed to fetch data:', err);
        setError('Failed to load case information and documents. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (caseId) {
      fetchData();
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

  const getTotalSize = () => {
    return documents.reduce((total, doc) => total + doc.size, 0);
  };

  const getDocumentTypes = () => {
    const types = documents.reduce((acc, doc) => {
      acc[doc.type] = (acc[doc.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    return Object.entries(types).map(([type, count]) => ({ type, count }));
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }} data-testid="document-list">
      {/* Case Summary Section */}
      {caseInfo && (
        <Card sx={{ mb: 2, flexShrink: 0 }} data-testid="case-summary">
          <CardContent sx={{ pb: 2 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <FolderIcon color="primary" />
              Case Summary
            </Typography>
            
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                <strong>{caseInfo.title}</strong>
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {caseInfo.summary}
              </Typography>
              
              <Box sx={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 2 }}>
                <Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <AssessmentIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                    <Typography variant="caption" color="text.secondary">
                      Case Type: {caseInfo.case_type}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CalendarIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                    <Typography variant="caption" color="text.secondary">
                      Created: {formatDate(caseInfo.created_date)}
                    </Typography>
                  </Box>
                </Box>
                
                <Box>
                  <Chip
                    size="small"
                    label={caseInfo.status}
                    color={caseInfo.status === 'Active' ? 'success' : caseInfo.status === 'Under Review' ? 'warning' : 'default'}
                    sx={{ mb: 1 }}
                  />
                  <Typography variant="caption" color="text.secondary" display="block">
                    Client: {caseInfo.client_name}
                  </Typography>
                </Box>
              </Box>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Document Summary Section */}
      <Card sx={{ mb: 2, flexShrink: 0 }} data-testid="document-summary">
        <CardContent sx={{ pb: 2 }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <DocumentIcon color="primary" />
            Document Summary
          </Typography>
          
          <Box>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center', flex: 1 }}>
                <Typography variant="h4" color="primary" fontWeight="bold">
                  {documents.length}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Total Documents
                </Typography>
              </Paper>
              
              <Paper variant="outlined" sx={{ p: 1.5, textAlign: 'center', flex: 1 }} data-testid="analyzed-count">
                <Typography variant="h4" color="success.main" fontWeight="bold">
                  {documents.filter(doc => doc.analysis_completed).length}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Analyzed
                </Typography>
              </Paper>
            </Box>
            
            <Typography variant="body2" color="text.secondary" gutterBottom>
              <strong>Total Size:</strong> {formatFileSize(getTotalSize())}
            </Typography>
            
            <Box display="flex" flexWrap="wrap" gap={0.5} mt={1}>
              {getDocumentTypes().map(({ type, count }) => (
                <Chip
                  key={type}
                  size="small"
                  label={`${type} (${count})`}
                  variant="outlined"
                  sx={{ fontSize: '0.7rem' }}
                />
              ))}
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Document List Header */}
      <Box mb={1} sx={{ flexShrink: 0 }}>
        <Typography variant="subtitle1" gutterBottom>
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
      
      {/* Document List */}
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <List disablePadding>
          {documents.map((document) => (
            <React.Fragment key={document.id}>
              <ListItem disablePadding>
                <ListItemButton
                  selected={selectedDocumentId === document.id}
                  onClick={() => onDocumentSelect?.(document)}
                  data-testid="document-item"
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
                          <Box 
                            data-testid="analysis-status" 
                            data-status={document.analysis_completed ? 'completed' : 'pending'}
                          >
                            {document.analysis_completed ? (
                              <AnalyzedIcon color="success" sx={{ fontSize: 12 }} />
                            ) : (
                              <PendingIcon color="warning" sx={{ fontSize: 12 }} />
                            )}
                          </Box>
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