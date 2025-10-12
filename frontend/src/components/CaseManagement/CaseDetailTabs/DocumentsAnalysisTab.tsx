import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  ListItemIcon,
  Stack
} from '@mui/material';
import {
  Description as DocumentIcon,
  HourglassEmpty as HourglassEmptyIcon,
  Folder as FolderIcon,
  Email as EmailIcon,
  Assignment as AssignmentIcon,
  Gavel as EvidenceIcon
} from '@mui/icons-material';
import { Document } from '../../../types/api';

interface DocumentsAnalysisTabProps {
  caseId: string;
  caseDocuments: Document[];
  documentsLoading: boolean;
  onNavigateToDocument: (docId: string) => void;
}

interface DocumentAnalysisResult {
  document_id: string;
  summary: string;
  key_points: string[];
  confidence_score: number;
  analysis_timestamp: string;
  key_dates?: string[];
  parties_involved?: string[];
  document_type?: string;
  key_clauses?: string[];
  risk_level?: string;
  potential_issues?: string[];
}

const DocumentsAnalysisTab: React.FC<DocumentsAnalysisTabProps> = ({
  caseId,
  caseDocuments,
  documentsLoading,
  onNavigateToDocument
}) => {
  const [analysisResults, setAnalysisResults] = useState<Record<string, DocumentAnalysisResult>>({});
  const [analysisLoading, setAnalysisLoading] = useState<Record<string, boolean>>({});

  useEffect(() => {
    // TODO: Load analysis results when AI is implemented
    // For now, analysis functionality is disabled
    setAnalysisResults({});
  }, [caseDocuments]);

  const getDocumentTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'contract': return <AssignmentIcon />;
      case 'email': return <EmailIcon />;
      case 'evidence': return <EvidenceIcon />;
      case 'legal brief': return <DocumentIcon />;
      default: return <FolderIcon />;
    }
  };



  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'error';
  };

  const triggerDocumentAnalysis = async (docId: string) => {
    setAnalysisLoading(prev => ({ ...prev, [docId]: true }));
    
    try {
      // TODO: Implement AI document analysis
      console.log('Document analysis not yet implemented for:', docId);
      
      // Placeholder response
      const placeholderResult: DocumentAnalysisResult = {
        document_id: docId,
        summary: "AI analysis not yet implemented",
        key_points: [],
        confidence_score: 0.0,
        analysis_timestamp: new Date().toISOString()
      };
      
      setAnalysisResults(prev => ({
        ...prev,
        [docId]: placeholderResult
      }));
    } catch (error) {
      console.error(`Failed to analyze document ${docId}:`, error);
    } finally {
      setAnalysisLoading(prev => ({ ...prev, [docId]: false }));
    }
  };

  const analysisStatus = {
    completed: 0, // Analysis functionality disabled
    total: caseDocuments.length
  };

  return (
    <Card sx={{ mb: 4 }} data-testid="documents-analysis-section">
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Box display="flex" alignItems="center">
            <DocumentIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h5" component="h2">
              Documents with Analysis
            </Typography>
          </Box>
          <Stack direction="row" spacing={1}>
            <Chip
              label={`${caseDocuments.length} document${caseDocuments.length !== 1 ? 's' : ''}`}
              variant="outlined"
              size="small"
            />
            <Chip
              label={`${analysisStatus.completed}/${analysisStatus.total} analyzed`}
              color={analysisStatus.completed === analysisStatus.total ? 'success' : 'warning'}
              size="small"
            />
          </Stack>
        </Box>
        <Divider sx={{ mb: 3 }} />

        {documentsLoading ? (
          <Box display="flex" justifyContent="center" p={2}>
            <CircularProgress size={24} />
          </Box>
        ) : caseDocuments.length > 0 ? (
          <List>
            {caseDocuments.map((doc, index) => {
              const analysis = analysisResults[doc.id];
              const isAnalyzing = analysisLoading[doc.id];
              
              return (
                <ListItem key={doc.id} divider={index < caseDocuments.length - 1} sx={{ flexDirection: 'column', alignItems: 'stretch' }}>
                  {/* Document Header */}
                  <Box display="flex" alignItems="center" width="100%" mb={analysis ? 2 : 0}>
                    <ListItemIcon>
                      {getDocumentTypeIcon(doc.type)}
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Button
                          variant="text"
                          sx={{
                            justifyContent: 'flex-start',
                            textTransform: 'none',
                            p: 0,
                            minWidth: 'auto',
                            '&:hover': { backgroundColor: 'transparent', textDecoration: 'underline' }
                          }}
                          onClick={() => onNavigateToDocument(doc.id)}
                          data-testid="document-link"
                        >
                          {doc.name}
                        </Button>
                      }
                      secondary={
                        <Box>
                          <Typography variant="caption" color="text.secondary" display="block">
                            Type: {doc.type} • Size: {formatFileSize(doc.size)}
                          </Typography>
                          <Typography variant="caption" color="text.secondary" display="block">
                            Uploaded: {new Date(doc.upload_date).toLocaleDateString('en-GB')}
                          </Typography>
                          {doc.content_preview && (
                            <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.5, fontStyle: 'italic' }}>
                              {doc.content_preview.substring(0, 100)}...
                            </Typography>
                          )}
                        </Box>
                      }
                    />
                    <Box display="flex" alignItems="center" ml={2} data-testid="document-analysis-status">
                      {isAnalyzing ? (
                        <CircularProgress size={20} />
                      ) : (
                        <HourglassEmptyIcon color="disabled" />
                      )}
                      <Typography variant="caption" color="text.secondary" ml={1}>
                        {isAnalyzing ? 'analyzing...' : 'analysis disabled'}
                      </Typography>
                    </Box>
                  </Box>

                  {/* Analysis Results */}
                  {analysis && (
                    <Box sx={{ ml: 6, mt: 1, p: 2, bgcolor: 'grey.50', borderRadius: 1 }} data-testid="analysis-results">
                      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                        <Typography variant="subtitle2" color="primary">
                          Analysis Results
                        </Typography>
                        <Chip
                          label={`${Math.round(analysis.confidence_score * 100)}% confidence`}
                          color={getConfidenceColor(analysis.confidence_score) as any}
                          size="small"
                        />
                      </Box>
                      
                      <Typography variant="body2" sx={{ mb: 2 }}>
                        <strong>Summary:</strong> {analysis.summary}
                      </Typography>
                      
                      {analysis.key_points && analysis.key_points.length > 0 && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 1 }}>
                            Key Points:
                          </Typography>
                          <List dense>
                            {analysis.key_points.map((point, idx) => (
                              <ListItem key={idx} sx={{ py: 0.5, pl: 2 }}>
                                <Typography variant="body2">• {point}</Typography>
                              </ListItem>
                            ))}
                          </List>
                        </Box>
                      )}

                      {analysis.parties_involved && analysis.parties_involved.length > 0 && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Parties:</strong> {analysis.parties_involved.join(', ')}
                        </Typography>
                      )}

                      {analysis.key_dates && analysis.key_dates.length > 0 && (
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Key Dates:</strong> {analysis.key_dates.join(', ')}
                        </Typography>
                      )}

                      {analysis.risk_level && (
                        <Chip
                          label={`Risk Level: ${analysis.risk_level}`}
                          color={analysis.risk_level === 'high' ? 'error' : analysis.risk_level === 'medium' ? 'warning' : 'success'}
                          size="small"
                          sx={{ mt: 1 }}
                        />
                      )}

                      <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 2 }}>
                        Analyzed: {new Date(analysis.analysis_timestamp).toLocaleString('en-GB')}
                      </Typography>
                    </Box>
                  )}
                </ListItem>
              );
            })}
          </List>
        ) : (
          <Box textAlign="center" py={4}>
            <DocumentIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
            <Typography variant="body2" color="text.secondary" gutterBottom>
              No documents uploaded yet
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Upload documents to begin case analysis
            </Typography>
          </Box>
        )}

        {caseDocuments.length > 0 && (
          <Stack direction="row" spacing={2} sx={{ mt: 3 }}>
            <Button
              variant="outlined"
              fullWidth
              onClick={() => window.open(`/cases/${caseId}/documents`, '_blank')}
            >
              View Documents
            </Button>
          </Stack>
        )}
      </CardContent>
    </Card>
  );
};

export default DocumentsAnalysisTab;