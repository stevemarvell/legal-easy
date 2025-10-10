import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Paper,
  Tooltip,
  Button,

  IconButton,
  Collapse,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Snackbar
} from '@mui/material';
import {
  Psychology as AIIcon,
  Event as DateIcon,
  Person as PersonIcon,
  Gavel as LegalIcon,
  Assignment as SummaryIcon,
  TrendingUp as ConfidenceIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  PlayArrow as RunIcon,
  Clear as ClearIcon,
  Refresh as RefreshIcon,

  KeyboardArrowDown,
  KeyboardArrowUp,
  Description as DocumentIcon
} from '@mui/icons-material';
import { documentService } from '../../services/documentService';
import { DocumentAnalysis as DocumentAnalysisType, Document } from '../../types/document';
import { PartiesComponent, KeyDatesComponent, KeyClausesComponent } from './AnalysisComponents';

interface DocumentAnalysisProps {
  documentId?: string;
  analysis?: DocumentAnalysisType; // Optional pre-loaded analysis
  showManagementInterface?: boolean; // Show the management buttons and list
}

interface AnalyzedDocument {
  document: Document;
  analysis: DocumentAnalysisType | null;
  status: 'pending' | 'analyzing' | 'completed' | 'error';
  error?: string;
}

const DocumentAnalysis: React.FC<DocumentAnalysisProps> = ({
  documentId,
  analysis: preloadedAnalysis,
  showManagementInterface = false
}) => {
  // Single document analysis state
  const [analysis, setAnalysis] = useState<DocumentAnalysisType | null>(preloadedAnalysis || null);
  const [loading, setLoading] = useState(!preloadedAnalysis && !!documentId);
  const [error, setError] = useState<string | null>(null);

  // Management interface state
  const [documents, setDocuments] = useState<Document[]>([]);
  const [analyzedDocuments, setAnalyzedDocuments] = useState<AnalyzedDocument[]>([]);
  const [isRunningAnalysis, setIsRunningAnalysis] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [currentlyAnalyzing, setCurrentlyAnalyzing] = useState<string>('');
  const [isLoadingDocuments, setIsLoadingDocuments] = useState(false);

  // Load single document analysis
  useEffect(() => {
    const fetchAnalysis = async () => {
      if (preloadedAnalysis || !documentId) {
        setAnalysis(preloadedAnalysis || null);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const fetchedAnalysis = await documentService.getDocumentAnalysis(documentId);
        setAnalysis(fetchedAnalysis);
      } catch (err) {
        console.error('Failed to fetch document analysis:', err);
        setError('Failed to load document analysis. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (documentId && !showManagementInterface) {
      fetchAnalysis();
    }
  }, [documentId, preloadedAnalysis, showManagementInterface]);

  // Load all documents for management interface
  useEffect(() => {
    const fetchAllDocuments = async () => {
      if (!showManagementInterface) return;

      try {
        setIsLoadingDocuments(true);
        setError(null);
        const allDocuments = await documentService.getAllDocuments();
        setDocuments(allDocuments);

        // Initialize analyzed documents state and check for existing analysis
        const initialAnalyzedDocs: AnalyzedDocument[] = [];

        for (const doc of allDocuments) {
          try {
            // Try to fetch existing analysis for each document
            const existingAnalysis = await documentService.getDocumentAnalysis(doc.id);
            initialAnalyzedDocs.push({
              document: doc,
              analysis: existingAnalysis,
              status: 'completed'
            });
          } catch (err) {
            // No existing analysis found, initialize as pending
            initialAnalyzedDocs.push({
              document: doc,
              analysis: null,
              status: 'pending'
            });
          }
        }

        setAnalyzedDocuments(initialAnalyzedDocs);
      } catch (err) {
        console.error('Failed to fetch documents:', err);
        setError('Failed to load documents. Please try again.');
      } finally {
        setIsLoadingDocuments(false);
      }
    };

    fetchAllDocuments();
  }, [showManagementInterface]);

  // Clear all analysis results
  const handleClearAll = async () => {
    if (isRunningAnalysis) return; // Safety check

    try {
      // Clear from backend storage
      await documentService.clearAllAnalyses();

      // Update UI state
      setAnalyzedDocuments(prev =>
        prev.map(doc => ({
          ...doc,
          analysis: null,
          status: 'pending',
          error: undefined
        }))
      );
      setAnalysisProgress(0);
      setCurrentlyAnalyzing('');
      setSnackbarMessage('All analysis results cleared from storage');
      setSnackbarOpen(true);
    } catch (error) {
      console.error('Failed to clear analysis results:', error);
      setSnackbarMessage('Failed to clear analysis results');
      setSnackbarOpen(true);
    }
  };

  // Run analysis on all documents
  const handleRunAnalysis = async () => {
    if (isRunningAnalysis || analyzedDocuments.length === 0) return; // Safety checks

    setIsRunningAnalysis(true);
    setAnalysisProgress(0);
    setCurrentlyAnalyzing('');

    const totalDocuments = analyzedDocuments.length;
    let completedCount = 0;
    let successCount = 0;
    let errorCount = 0;

    for (let i = 0; i < analyzedDocuments.length; i++) {
      const docItem = analyzedDocuments[i];

      // Update current document being analyzed
      setCurrentlyAnalyzing(docItem.document.name);

      // Update status to analyzing
      setAnalyzedDocuments(prev =>
        prev.map((item, index) =>
          index === i ? { ...item, status: 'analyzing' } : item
        )
      );

      try {
        const analysisResult = await documentService.analyzeDocument(docItem.document.id);

        // Update with successful analysis
        setAnalyzedDocuments(prev =>
          prev.map((item, index) =>
            index === i ? {
              ...item,
              analysis: analysisResult,
              status: 'completed',
              error: undefined
            } : item
          )
        );
        successCount++;
      } catch (err) {
        console.error(`Failed to analyze document ${docItem.document.id}:`, err);

        // Update with error
        setAnalyzedDocuments(prev =>
          prev.map((item, index) =>
            index === i ? {
              ...item,
              status: 'error',
              error: err instanceof Error ? err.message : 'Analysis failed'
            } : item
          )
        );
        errorCount++;
      }

      completedCount++;
      setAnalysisProgress((completedCount / totalDocuments) * 100);

      // Small delay to show progress visually
      if (i < analyzedDocuments.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }

    setIsRunningAnalysis(false);
    setCurrentlyAnalyzing('');

    // Enhanced completion message
    let message = `Analysis completed: ${successCount} successful`;
    if (errorCount > 0) {
      message += `, ${errorCount} failed`;
    }
    setSnackbarMessage(message);
    setSnackbarOpen(true);
  };



  const getConfidenceColor = (score: number): 'success' | 'warning' | 'error' => {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'error';
  };

  const getConfidenceIcon = (score: number) => {
    if (score >= 0.8) return <CheckIcon color="success" />;
    return <WarningIcon color="warning" />;
  };

  const formatConfidenceScore = (score: number): string => {
    return `${Math.round(score * 100)}%`;
  };

  // Helper function to check if there are any analysis results to clear
  const hasAnyResults = (): boolean => {
    return analyzedDocuments.some(doc =>
      doc.analysis !== null || doc.status === 'completed' || doc.status === 'error'
    );
  };

  // Refresh documents list
  const handleRefreshDocuments = async () => {
    if (isRunningAnalysis) return;

    try {
      setIsLoadingDocuments(true);
      setError(null);
      const allDocuments = await documentService.getAllDocuments();
      setDocuments(allDocuments);

      // Initialize analyzed documents state and check for existing analysis
      const initialAnalyzedDocs: AnalyzedDocument[] = [];

      for (const doc of allDocuments) {
        try {
          // Try to fetch existing analysis for each document
          const existingAnalysis = await documentService.getDocumentAnalysis(doc.id);
          initialAnalyzedDocs.push({
            document: doc,
            analysis: existingAnalysis,
            status: 'completed'
          });
        } catch (err) {
          // No existing analysis found, initialize as pending
          initialAnalyzedDocs.push({
            document: doc,
            analysis: null,
            status: 'pending'
          });
        }
      }

      setAnalyzedDocuments(initialAnalyzedDocs);
      setSnackbarMessage('Documents refreshed successfully');
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Failed to refresh documents:', err);
      setError('Failed to refresh documents. Please try again.');
    } finally {
      setIsLoadingDocuments(false);
    }
  };

  // Render management interface
  if (showManagementInterface) {
    return (
      <Box>
        <Snackbar
          open={snackbarOpen}
          autoHideDuration={4000}
          onClose={() => setSnackbarOpen(false)}
          message={snackbarMessage}
        />

        {/* Management Header */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
              <Box display="flex" alignItems="center">
                <AIIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h5" component="h2">
                  Document Analysis Management
                </Typography>
              </Box>
              <Box display="flex" gap={2}>
                <Tooltip title="Refresh documents list">
                  <span>
                    <IconButton
                      color="primary"
                      onClick={handleRefreshDocuments}
                      disabled={isRunningAnalysis || isLoadingDocuments}
                      sx={{
                        opacity: (isRunningAnalysis || isLoadingDocuments) ? 0.6 : 1,
                        transition: 'opacity 0.2s ease-in-out'
                      }}
                    >
                      {isLoadingDocuments ? (
                        <CircularProgress size={24} />
                      ) : (
                        <RefreshIcon />
                      )}
                    </IconButton>
                  </span>
                </Tooltip>
                <Tooltip
                  title={
                    isRunningAnalysis
                      ? "Cannot clear while analysis is running"
                      : hasAnyResults()
                        ? "Clear all analysis results"
                        : "No results to clear"
                  }
                >
                  <span>
                    <Button
                      variant="outlined"
                      color="secondary"
                      startIcon={<ClearIcon />}
                      onClick={handleClearAll}
                      disabled={isRunningAnalysis || isLoadingDocuments || !hasAnyResults()}
                      sx={{
                        opacity: (isRunningAnalysis || isLoadingDocuments || !hasAnyResults()) ? 0.6 : 1,
                        transition: 'opacity 0.2s ease-in-out'
                      }}
                    >
                      Clear All
                    </Button>
                  </span>
                </Tooltip>
                <Tooltip
                  title={
                    isRunningAnalysis
                      ? `Analyzing: ${currentlyAnalyzing}`
                      : documents.length === 0
                        ? "No documents available"
                        : isLoadingDocuments
                          ? "Loading documents..."
                          : `Analyze ${documents.length} documents`
                  }
                >
                  <span>
                    <Button
                      variant="contained"
                      color="primary"
                      startIcon={
                        isRunningAnalysis ? (
                          <CircularProgress size={20} color="inherit" />
                        ) : isLoadingDocuments ? (
                          <CircularProgress size={20} color="inherit" />
                        ) : (
                          <RunIcon />
                        )
                      }
                      onClick={handleRunAnalysis}
                      disabled={isRunningAnalysis || isLoadingDocuments || documents.length === 0}
                      sx={{
                        minWidth: 140,
                        opacity: (isRunningAnalysis || isLoadingDocuments || documents.length === 0) ? 0.8 : 1,
                        transition: 'all 0.2s ease-in-out',
                        '&:disabled': {
                          backgroundColor: isRunningAnalysis ? 'primary.main' : undefined,
                          color: isRunningAnalysis ? 'primary.contrastText' : undefined,
                        }
                      }}
                    >
                      {isRunningAnalysis
                        ? 'Analyzing...'
                        : isLoadingDocuments
                          ? 'Loading...'
                          : 'Run Analysis'
                      }
                    </Button>
                  </span>
                </Tooltip>
              </Box>
            </Box>

            {isRunningAnalysis && (
              <Box sx={{ mt: 2 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    Analysis Progress: {Math.round(analysisProgress)}%
                  </Typography>
                  <Typography variant="body2" color="primary" fontWeight="medium">
                    {Math.round(analysisProgress / 100 * analyzedDocuments.length)} / {analyzedDocuments.length} documents
                  </Typography>
                </Box>
                {currentlyAnalyzing && (
                  <Typography variant="caption" color="text.secondary" gutterBottom display="block">
                    Currently analyzing: {currentlyAnalyzing}
                  </Typography>
                )}
                <LinearProgress
                  variant="determinate"
                  value={analysisProgress}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: 'grey.200',
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 4,
                      transition: 'transform 0.4s ease-in-out'
                    }
                  }}
                />
              </Box>
            )}

            <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Chip
                label={`${analyzedDocuments.filter(d => d.status === 'pending').length} Pending`}
                color="default"
                size="small"
                variant="outlined"
              />
              <Chip
                label={`${analyzedDocuments.filter(d => d.status === 'analyzing').length} Analyzing`}
                color="info"
                size="small"
                variant="outlined"
              />
              <Chip
                label={`${analyzedDocuments.filter(d => d.status === 'completed').length} Completed`}
                color="success"
                size="small"
                variant="outlined"
              />
              <Chip
                label={`${analyzedDocuments.filter(d => d.status === 'error').length} Errors`}
                color="error"
                size="small"
                variant="outlined"
              />
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Manage AI analysis for all documents in the system
            </Typography>
          </CardContent>
        </Card>

        {/* Analysis Results Table */}
        <Card>
          <CardContent>
            <style>
              {`
                @keyframes pulse {
                  0% { opacity: 1; }
                  50% { opacity: 0.5; }
                  100% { opacity: 1; }
                }
              `}
            </style>
            <Typography variant="h6" gutterBottom>
              Analysis Results ({analyzedDocuments.length} documents)
            </Typography>
            <Divider sx={{ mb: 2 }} />

            {error ? (
              <Alert
                severity="error"
                action={
                  <Button
                    color="inherit"
                    size="small"
                    onClick={handleRefreshDocuments}
                    disabled={isLoadingDocuments}
                  >
                    Retry
                  </Button>
                }
              >
                {error}
              </Alert>
            ) : analyzedDocuments.length === 0 ? (
              <Alert severity="info">
                {isLoadingDocuments
                  ? "Loading documents..."
                  : "No documents found. Please check your data or try refreshing."
                }
              </Alert>
            ) : (
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell />
                      <TableCell>Document</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Case</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Confidence</TableCell>
                      <TableCell>Parties</TableCell>
                      <TableCell>Dates</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {analyzedDocuments.map((item, index) => (
                      <AnalyzedDocumentRow
                        key={item.document.id}
                        item={item}
                        index={index}
                      />
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </CardContent>
        </Card>
      </Box>
    );
  }

  // Render single document analysis
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="300px">
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

  if (!analysis) {
    return (
      <Alert severity="info" sx={{ mb: 2 }}>
        No analysis available for this document
      </Alert>
    );
  }

  return (
    <Box>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>

        {/* Key Information and Legal Analysis */}
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
          {/* Key Information */}
          <Box sx={{ flex: 1 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Key Information
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {/* Key Dates */}
                <KeyDatesComponent dates={analysis.key_dates} variant="accordion" />

                {/* Parties Involved */}
                <PartiesComponent parties={analysis.parties_involved} variant="accordion" />
              </CardContent>
            </Card>
          </Box>

          {/* Legal Analysis */}
          <Box sx={{ flex: 1 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Legal Analysis
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {/* Document Type */}
                <Box mb={3}>
                  <Typography variant="subtitle2" gutterBottom>
                    Document Classification
                  </Typography>
                  <Chip
                    label={analysis.document_type}
                    color="primary"
                    variant="outlined"
                    size="medium"
                  />
                </Box>

                {/* Key Clauses */}
                <KeyClausesComponent clauses={analysis.key_clauses} variant="accordion" />
              </CardContent>
            </Card>
          </Box>
        </Box>

        {/* Legal Significance and Issues */}
        {(analysis.legal_significance && analysis.legal_significance.length > 0) ||
          (analysis.potential_issues && analysis.potential_issues.length > 0) ? (
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
            {/* Legal Significance */}
            {analysis.legal_significance && analysis.legal_significance.length > 0 && (
              <Box sx={{ flex: 1 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                      <CheckIcon color="success" sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        Legal Significance
                      </Typography>
                    </Box>
                    <Divider sx={{ mb: 2 }} />

                    <List dense>
                      {analysis.legal_significance.map((significance, index) => (
                        <ListItem key={index}>
                          <ListItemIcon>
                            <CheckIcon fontSize="small" color="success" />
                          </ListItemIcon>
                          <ListItemText
                            primary={
                              <Paper
                                variant="outlined"
                                sx={{
                                  p: 1.5,
                                  backgroundColor: 'grey.800',
                                  borderColor: 'grey.600',
                                  borderWidth: 1,
                                  color: 'white'
                                }}
                              >
                                <Typography variant="body2" fontWeight="medium">
                                  {significance}
                                </Typography>
                              </Paper>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Box>
            )}

            {/* Potential Issues */}
            {analysis.potential_issues && analysis.potential_issues.length > 0 && (
              <Box sx={{ flex: 1 }}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                      <WarningIcon color="error" sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        Potential Issues
                      </Typography>
                    </Box>
                    <Divider sx={{ mb: 2 }} />

                    <List dense>
                      {analysis.potential_issues.map((issue, index) => (
                        <ListItem key={index}>
                          <ListItemIcon>
                            <WarningIcon fontSize="small" color="error" />
                          </ListItemIcon>
                          <ListItemText
                            primary={
                              <Paper
                                variant="outlined"
                                sx={{
                                  p: 1.5,
                                  backgroundColor: 'grey.800',
                                  borderColor: 'grey.600',
                                  borderWidth: 1,
                                  color: 'white'
                                }}
                              >
                                <Typography variant="body2" fontWeight="medium">
                                  {issue}
                                </Typography>
                              </Paper>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Box>
            )}
          </Box>
        ) : null}

        {/* Confidence Scores */}
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <ConfidenceIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">
                Analysis Confidence Scores
              </Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />

            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
              {Object.entries(analysis.confidence_scores).map(([category, score]) => (
                <Box key={category} sx={{ minWidth: 200, flex: '1 1 200px' }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                    <Typography variant="subtitle2" sx={{ textTransform: 'capitalize' }}>
                      {category.replace('_', ' ')}
                    </Typography>
                    <Box display="flex" alignItems="center" gap={0.5}>
                      <Tooltip title={`Confidence: ${formatConfidenceScore(score)}`}>
                        {getConfidenceIcon(score)}
                      </Tooltip>
                      <Typography variant="body2" fontWeight="bold">
                        {formatConfidenceScore(score)}
                      </Typography>
                    </Box>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={score * 100}
                    color={getConfidenceColor(score)}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
              ))}
            </Box>

            <Alert severity="info" sx={{ mt: 3 }}>
              <Typography variant="body2">
                Confidence scores indicate the AI's certainty in the extracted information.
                Scores above 80% are considered highly reliable, while scores below 60% may require manual review.
              </Typography>
            </Alert>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

// Component for individual document row in the analysis table
interface AnalyzedDocumentRowProps {
  item: AnalyzedDocument;
  index: number;
}

const AnalyzedDocumentRow: React.FC<AnalyzedDocumentRowProps> = ({ item }) => {
  const [open, setOpen] = useState(false);

  const getStatusChip = (status: AnalyzedDocument['status']) => {
    switch (status) {
      case 'pending':
        return <Chip label="Pending" color="default" size="small" variant="outlined" />;
      case 'analyzing':
        return <Chip label="Analyzing" color="info" size="small" variant="outlined" icon={<CircularProgress size={16} />} />;
      case 'completed':
        return <Chip label="Completed" color="success" size="small" variant="outlined" icon={<CheckIcon />} />;
      case 'error':
        return <Chip label="Error" color="error" size="small" variant="outlined" icon={<WarningIcon />} />;
      default:
        return <Chip label="Unknown" color="default" size="small" variant="outlined" />;
    }
  };

  const getAverageConfidence = (analysis: DocumentAnalysisType | null): number => {
    if (!analysis || !analysis.confidence_scores) return 0;
    const scores = Object.values(analysis.confidence_scores);
    return scores.reduce((sum, score) => sum + score, 0) / scores.length;
  };

  const formatConfidenceScore = (score: number): string => {
    return `${Math.round(score * 100)}%`;
  };

  return (
    <>
      <TableRow
        sx={{
          '& > *': { borderBottom: 'unset' },
          backgroundColor: item.status === 'analyzing' ? 'action.hover' : 'inherit',
          transition: 'background-color 0.3s ease-in-out',
          '&:hover': {
            backgroundColor: item.status === 'analyzing' ? 'action.selected' : 'action.hover'
          }
        }}
      >
        <TableCell>
          <Tooltip title={
            !item.analysis
              ? "No analysis data to expand"
              : open
                ? "Collapse details"
                : "Expand to see detailed analysis"
          }>
            <IconButton
              aria-label="expand row"
              size="small"
              onClick={() => setOpen(!open)}
              disabled={!item.analysis}
              sx={{
                transition: 'transform 0.2s ease-in-out',
                transform: open ? 'rotate(180deg)' : 'rotate(0deg)'
              }}
            >
              <KeyboardArrowDown />
            </IconButton>
          </Tooltip>
        </TableCell>
        <TableCell>
          <Box display="flex" alignItems="center">
            <DocumentIcon
              sx={{
                mr: 1,
                color: item.status === 'analyzing' ? 'primary.main' : 'text.secondary',
                animation: item.status === 'analyzing' ? 'pulse 2s infinite' : 'none'
              }}
            />
            <Box>
              <Typography
                variant="body2"
                fontWeight="medium"
                sx={{
                  color: item.status === 'analyzing' ? 'primary.main' : 'inherit'
                }}
              >
                {item.document.name}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {item.document.id}
              </Typography>
            </Box>
          </Box>
        </TableCell>
        <TableCell>
          <Chip
            label={item.analysis?.document_type || item.document.type}
            color="primary"
            variant="outlined"
            size="small"
          />
        </TableCell>
        <TableCell>
          <Typography variant="body2">
            {item.document.case_id}
          </Typography>
        </TableCell>
        <TableCell>
          {getStatusChip(item.status)}
          {item.error && (
            <Tooltip title={item.error}>
              <WarningIcon color="error" sx={{ ml: 1, fontSize: 16 }} />
            </Tooltip>
          )}
        </TableCell>
        <TableCell>
          {item.analysis ? (
            <Box display="flex" alignItems="center">
              <Typography variant="body2" fontWeight="medium">
                {formatConfidenceScore(getAverageConfidence(item.analysis))}
              </Typography>
              <LinearProgress
                variant="determinate"
                value={getAverageConfidence(item.analysis) * 100}
                sx={{ ml: 1, width: 60, height: 4 }}
                color={getAverageConfidence(item.analysis) >= 0.8 ? 'success' :
                  getAverageConfidence(item.analysis) >= 0.6 ? 'warning' : 'error'}
              />
            </Box>
          ) : (
            <Typography variant="body2" color="text.secondary">-</Typography>
          )}
        </TableCell>
        <TableCell>
          {item.analysis ? (
            <Typography variant="body2">
              {item.analysis.parties_involved.length}
            </Typography>
          ) : (
            <Typography variant="body2" color="text.secondary">-</Typography>
          )}
        </TableCell>
        <TableCell>
          {item.analysis ? (
            <Typography variant="body2">
              {item.analysis.key_dates.length}
            </Typography>
          ) : (
            <Typography variant="body2" color="text.secondary">-</Typography>
          )}
        </TableCell>
      </TableRow>

      {/* Expandable row with detailed analysis */}
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={8}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 2 }}>
              {item.analysis ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                  {/* Summary Section */}
                  <Paper
                    variant="outlined"
                    sx={{
                      p: 3,
                      backgroundColor: 'grey.900',
                      borderRadius: 2
                    }}
                  >
                    <Box display="flex" alignItems="center" mb={2}>
                      <SummaryIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="subtitle1" fontWeight="bold">
                        Document Summary
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ lineHeight: 1.6 }}>
                      {item.analysis.summary}
                    </Typography>
                  </Paper>

                  {/* Key Information Grid */}
                  <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
                    {/* Parties */}
                    <Box sx={{ flex: 1 }}>
                      <PartiesComponent parties={item.analysis.parties_involved} variant="paper" />
                    </Box>

                    {/* Key Dates */}
                    <Box sx={{ flex: 1 }}>
                      <KeyDatesComponent dates={item.analysis.key_dates} variant="paper" />
                    </Box>
                  </Box>

                  {/* Key Clauses */}
                  {item.analysis.key_clauses && item.analysis.key_clauses.length > 0 && (
                    <KeyClausesComponent clauses={item.analysis.key_clauses} variant="paper" />
                  )}

                  {/* Confidence Scores */}
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Box display="flex" alignItems="center" mb={2}>
                      <ConfidenceIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="subtitle2" fontWeight="bold">
                        Confidence Scores
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                      {Object.entries(item.analysis.confidence_scores).map(([category, score]) => (
                        <Box key={category} sx={{ minWidth: 120, flex: '1 1 120px' }}>
                          <Typography variant="caption" sx={{ textTransform: 'capitalize', fontWeight: 'medium' }}>
                            {category.replace('_', ' ')}
                          </Typography>
                          <Box display="flex" alignItems="center" gap={1}>
                            <LinearProgress
                              variant="determinate"
                              value={score * 100}
                              sx={{ flex: 1, height: 6, borderRadius: 3 }}
                              color={score >= 0.8 ? 'success' : score >= 0.6 ? 'warning' : 'error'}
                            />
                            <Typography variant="caption" fontWeight="bold">
                              {Math.round(score * 100)}%
                            </Typography>
                          </Box>
                        </Box>
                      ))}
                    </Box>
                  </Paper>
                </Box>
              ) : (
                <Alert severity="info" sx={{ m: 2 }}>
                  No analysis data available for this document
                </Alert>
              )}
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

export default DocumentAnalysis;