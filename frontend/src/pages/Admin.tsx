import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Container,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Paper,
  Grid,
  IconButton,
  Collapse
} from '@mui/material';
import {
  CheckCircle as GreenIcon,
  Warning as AmberIcon,
  Error as RedIcon,
  Refresh as RefreshIcon,
  PlayArrow as PlayIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Settings as AdminIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';

interface HealthCheck {
  status: 'green' | 'amber' | 'red';
  message: string;
  timestamp: string;
  details: Record<string, any>;
}

interface SystemHealth {
  overall_status: 'green' | 'amber' | 'red';
  timestamp: string;
  checks: {
    backend_api: HealthCheck;
    document_service: HealthCheck;
    rag_service: HealthCheck;
    legal_corpus: HealthCheck;
    case_assessment: HealthCheck;
  };
  summary: {
    total_checks: number;
    green_count: number;
    amber_count: number;
    red_count: number;
  };
}

interface DemoDataSummary {
  cases: {
    total_cases: number;
    by_status: Record<string, number>;
    by_type: Record<string, number>;
    case_types: string[];
  };
  documents: {
    total_documents: number;
    by_type: Record<string, number>;
    by_case: Record<string, number>;
    analyzed_count: number;
    analysis_status: string;
  };
  document_analyses: {
    total_analyses: number;
    status: string;
    demo_data_available: boolean;
  };
  legal_corpus: {
    full_corpus: {
      exists: boolean;
      documents: number;
      categories: Record<string, number>;
    };
    demo_corpus: {
      exists: boolean;
      documents: number;
      categories: Record<string, number>;
    };
  };
  playbooks: {
    total_playbooks: number;
    by_case_type: Record<string, number>;
    total_rules: number;
    case_types: string[];
  };
}

const Admin = () => {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [demoData, setDemoData] = useState<DemoDataSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [expandedDetails, setExpandedDetails] = useState<string | null>(null);

  const fetchHealth = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch health status
      const healthResponse = await apiClient.get<SystemHealth>('/api/admin/health');
      setHealth(healthResponse.data);
      
      // Fetch demo data summary
      const demoResponse = await apiClient.get<{success: boolean, summary: DemoDataSummary}>('/api/admin/demo-data-summary');
      if (demoResponse.data.success) {
        setDemoData(demoResponse.data.summary);
      }
    } catch (err) {
      console.error('Failed to fetch system health:', err);
      setError('Failed to fetch system health. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  const getStatusIcon = (status: 'green' | 'amber' | 'red') => {
    switch (status) {
      case 'green':
        return <GreenIcon color="success" />;
      case 'amber':
        return <AmberIcon color="warning" />;
      case 'red':
        return <RedIcon color="error" />;
    }
  };

  const getStatusColor = (status: 'green' | 'amber' | 'red') => {
    switch (status) {
      case 'green':
        return 'success';
      case 'amber':
        return 'warning';
      case 'red':
        return 'error';
    }
  };

  const handleAction = async (action: string, params?: any) => {
    try {
      setActionLoading(action);
      setError(null);

      let response;
      if (action === 'initialize-corpus') {
        response = await apiClient.post('/api/admin/actions/initialize-corpus');
      } else if (action === 'test-rag-search') {
        response = await apiClient.post('/api/admin/actions/test-rag-search?query=employment contract');
      } else if (action === 'analyze-documents') {
        response = await apiClient.post('/api/admin/actions/analyze-documents');
      } else if (action === 'run-document-analysis') {
        response = await apiClient.post('/api/admin/actions/run-document-analysis');
      }

      if (response?.data.success) {
        // Refresh health status after action
        await fetchHealth();
      }
    } catch (err: any) {
      console.error(`Action ${action} failed:`, err);
      setError(`Action failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setActionLoading(null);
    }
  };

  const toggleDetails = (checkName: string) => {
    setExpandedDetails(expandedDetails === checkName ? null : checkName);
  };

  if (loading) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="400px">
        <CircularProgress />
        <Typography variant="body1" sx={{ mt: 2 }}>Loading system status...</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box>
        {/* Header */}
        <Box mb={4}>
          <Box display="flex" alignItems="center" gap={2} mb={2}>
            <AdminIcon color="primary" />
            <Typography variant="h3" component="h1" color="primary">
              System Administration
            </Typography>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={fetchHealth}
              disabled={loading}
            >
              Refresh
            </Button>
          </Box>
          <Typography variant="h6" color="text.secondary">
            Monitor system health and perform administrative actions
          </Typography>
        </Box>

        {/* Error Alert */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Overall Status */}
        {health && (
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box display="flex" alignItems="center" gap={2}>
                  {getStatusIcon(health.overall_status)}
                  <Typography variant="h5">
                    Overall System Status
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Last updated: {new Date(health.timestamp).toLocaleString()}
                </Typography>
              </Box>
              
              <Box mt={2}>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={3}>
                    <Paper sx={{ p: 2, textAlign: 'center', backgroundColor: '#4caf50', color: 'white' }}>
                      <Typography variant="h4" color="inherit">
                        {health.summary.green_count}
                      </Typography>
                      <Typography variant="body2" color="inherit">
                        Healthy
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={3}>
                    <Paper sx={{ p: 2, textAlign: 'center', backgroundColor: '#ff9800', color: 'white' }}>
                      <Typography variant="h4" color="inherit">
                        {health.summary.amber_count}
                      </Typography>
                      <Typography variant="body2" color="inherit">
                        Warning
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={3}>
                    <Paper sx={{ p: 2, textAlign: 'center', backgroundColor: '#f44336', color: 'white' }}>
                      <Typography variant="h4" color="inherit">
                        {health.summary.red_count}
                      </Typography>
                      <Typography variant="body2" color="inherit">
                        Critical
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} sm={3}>
                    <Paper sx={{ p: 2, textAlign: 'center', backgroundColor: '#2196f3', color: 'white' }}>
                      <Typography variant="h4" color="inherit">
                        {health.summary.total_checks}
                      </Typography>
                      <Typography variant="body2" color="inherit">
                        Total Checks
                      </Typography>
                    </Paper>
                  </Grid>
                </Grid>
              </Box>
            </CardContent>
          </Card>
        )}

        {/* Health Checks */}
        {health && (
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                System Components
              </Typography>
              
              <List>
                {Object.entries(health.checks).map(([checkName, check], index) => (
                  <React.Fragment key={checkName}>
                    <ListItem>
                      <ListItemIcon>
                        {getStatusIcon(check.status)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Typography variant="h6">
                            {checkName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </Typography>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {check.message}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {new Date(check.timestamp).toLocaleString()}
                            </Typography>
                          </Box>
                        }
                      />
                      <IconButton
                        onClick={() => toggleDetails(checkName)}
                        size="small"
                      >
                        {expandedDetails === checkName ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                      </IconButton>
                    </ListItem>
                    
                    <Collapse in={expandedDetails === checkName}>
                      <Box sx={{ pl: 4, pr: 2, pb: 2 }}>
                        <Paper variant="outlined" sx={{ p: 2, backgroundColor: '#f5f5f5', border: '1px solid #ddd' }}>
                          <Typography variant="subtitle2" gutterBottom color="text.primary">
                            Details:
                          </Typography>
                          <pre style={{ 
                            fontSize: '0.75rem', 
                            margin: 0, 
                            whiteSpace: 'pre-wrap',
                            color: '#333',
                            backgroundColor: '#fff',
                            padding: '8px',
                            borderRadius: '4px',
                            border: '1px solid #ddd'
                          }}>
                            {JSON.stringify(check.details, null, 2)}
                          </pre>
                        </Paper>
                      </Box>
                    </Collapse>
                    
                    {index < Object.entries(health.checks).length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        )}

        {/* Demo Data Summary */}
        {demoData && (
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h5" gutterBottom color="text.primary">
                Demo Data Summary
              </Typography>
              <Alert severity="info" sx={{ mb: 3 }}>
                <Typography variant="body2">
                  <strong>Note:</strong> All analysis results are pre-computed demo data, not live AI processing. 
                  This demonstrates the platform's capabilities with realistic sample outputs.
                </Typography>
              </Alert>
              
              <Grid container spacing={3}>
                {/* Cases */}
                <Grid item xs={12} md={6} lg={4}>
                  <Paper sx={{ p: 2, backgroundColor: '#e3f2fd', border: '1px solid #2196f3' }}>
                    <Typography variant="h6" color="#1976d2" gutterBottom>
                      Cases ({demoData.cases.total_cases})
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.primary">
                        <strong>By Status:</strong>
                      </Typography>
                      {Object.entries(demoData.cases.by_status || {}).map(([status, count]) => (
                        <Typography key={status} variant="body2" color="text.secondary">
                          • {status}: {count}
                        </Typography>
                      ))}
                    </Box>
                    <Typography variant="body2" color="text.primary">
                      <strong>Case Types:</strong> {demoData.cases.case_types?.join(', ')}
                    </Typography>
                  </Paper>
                </Grid>

                {/* Documents */}
                <Grid item xs={12} md={6} lg={4}>
                  <Paper sx={{ p: 2, backgroundColor: '#e8f5e8', border: '1px solid #4caf50' }}>
                    <Typography variant="h6" color="#388e3c" gutterBottom>
                      Documents ({demoData.documents.total_documents})
                    </Typography>
                    <Typography variant="body2" color="text.primary" sx={{ mb: 1 }}>
                      <strong>Analyzed:</strong> {demoData.documents.analyzed_count}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      Status: {demoData.documents.analysis_status}
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.primary">
                        <strong>By Type:</strong>
                      </Typography>
                      {Object.entries(demoData.documents.by_type || {}).map(([type, count]) => (
                        <Typography key={type} variant="body2" color="text.secondary">
                          • {type}: {count}
                        </Typography>
                      ))}
                    </Box>
                  </Paper>
                </Grid>

                {/* Legal Corpus */}
                <Grid item xs={12} md={6} lg={4}>
                  <Paper sx={{ p: 2, backgroundColor: '#fff3e0', border: '1px solid #ff9800' }}>
                    <Typography variant="h6" color="#f57c00" gutterBottom>
                      Legal Corpus
                    </Typography>
                    <Typography variant="body2" color="text.primary" sx={{ mb: 1 }}>
                      <strong>Full Corpus:</strong> {demoData.legal_corpus.full_corpus.exists ? 
                        `${demoData.legal_corpus.full_corpus.documents} docs` : 'Not available'}
                    </Typography>
                    <Typography variant="body2" color="text.primary" sx={{ mb: 1 }}>
                      <strong>Demo Corpus:</strong> {demoData.legal_corpus.demo_corpus.exists ? 
                        `${demoData.legal_corpus.demo_corpus.documents} docs` : 'Not available'}
                    </Typography>
                    {demoData.legal_corpus.demo_corpus.categories && (
                      <Box>
                        <Typography variant="body2" color="text.primary">
                          <strong>Categories:</strong>
                        </Typography>
                        {Object.entries(demoData.legal_corpus.demo_corpus.categories).map(([category, count]) => (
                          <Typography key={category} variant="body2" color="text.secondary">
                            • {category}: {count}
                          </Typography>
                        ))}
                      </Box>
                    )}
                  </Paper>
                </Grid>

                {/* Document Analyses */}
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2, backgroundColor: '#ffebee', border: '1px solid #f44336' }}>
                    <Typography variant="h6" color="#d32f2f" gutterBottom>
                      Document Analyses ({demoData.document_analyses.total_analyses})
                    </Typography>
                    <Typography variant="body2" color="text.primary" sx={{ mb: 1 }}>
                      <strong>Status:</strong> {demoData.document_analyses.status}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Demo data available: {demoData.document_analyses.demo_data_available ? 'Yes' : 'No'}
                    </Typography>
                  </Paper>
                </Grid>

                {/* Playbooks */}
                <Grid item xs={12} md={6}>
                  <Paper sx={{ p: 2, backgroundColor: '#ffebee', border: '1px solid #f44336' }}>
                    <Typography variant="h6" color="#d32f2f" gutterBottom>
                      Playbooks ({demoData.playbooks.total_playbooks})
                    </Typography>
                    <Typography variant="body2" color="text.primary" sx={{ mb: 1 }}>
                      <strong>Total Rules:</strong> {demoData.playbooks.total_rules}
                    </Typography>
                    <Box>
                      <Typography variant="body2" color="text.primary">
                        <strong>Case Types:</strong>
                      </Typography>
                      {demoData.playbooks.case_types?.map((type) => (
                        <Typography key={type} variant="body2" color="text.secondary">
                          • {type}
                        </Typography>
                      ))}
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        )}

        {/* Administrative Actions */}
        <Card>
          <CardContent>
            <Typography variant="h5" gutterBottom color="text.primary">
              Administrative Actions
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" sx={{ p: 2, border: '1px solid #ddd' }}>
                  <Typography variant="h6" gutterBottom color="text.primary">
                    Initialize Legal Corpus
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Initialize the vector database and generate embeddings for the legal document corpus.
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<PlayIcon />}
                    onClick={() => handleAction('initialize-corpus')}
                    disabled={actionLoading === 'initialize-corpus'}
                    sx={{ backgroundColor: '#2196f3', '&:hover': { backgroundColor: '#1976d2' } }}
                  >
                    {actionLoading === 'initialize-corpus' ? (
                      <>
                        <CircularProgress size={16} sx={{ mr: 1, color: 'white' }} />
                        Initializing...
                      </>
                    ) : (
                      'Initialize Corpus'
                    )}
                  </Button>
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" sx={{ p: 2, border: '1px solid #ddd' }}>
                  <Typography variant="h6" gutterBottom color="text.primary">
                    Test RAG Search
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Test the RAG search functionality with a sample query.
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<PlayIcon />}
                    onClick={() => handleAction('test-rag-search')}
                    disabled={actionLoading === 'test-rag-search'}
                    sx={{ backgroundColor: '#4caf50', '&:hover': { backgroundColor: '#388e3c' } }}
                  >
                    {actionLoading === 'test-rag-search' ? (
                      <>
                        <CircularProgress size={16} sx={{ mr: 1, color: 'white' }} />
                        Testing...
                      </>
                    ) : (
                      'Test Search'
                    )}
                  </Button>
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" sx={{ p: 2, border: '1px solid #f44336' }}>
                  <Typography variant="h6" gutterBottom color="#d32f2f">
                    Analyze Documents
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Run AI document analysis on all documents (not yet implemented).
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<PlayIcon />}
                    onClick={() => handleAction('analyze-documents')}
                    disabled={actionLoading === 'analyze-documents'}
                    sx={{ backgroundColor: '#f44336', '&:hover': { backgroundColor: '#d32f2f' } }}
                  >
                    {actionLoading === 'analyze-documents' ? (
                      <>
                        <CircularProgress size={16} sx={{ mr: 1, color: 'white' }} />
                        Analyzing...
                      </>
                    ) : (
                      'Analyze Documents'
                    )}
                  </Button>
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" sx={{ p: 2, border: '1px solid #ddd' }}>
                  <Typography variant="h6" gutterBottom color="text.primary">
                    Run Document Analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Run AI analysis on all documents to generate real insights.
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<PlayIcon />}
                    onClick={() => handleAction('run-document-analysis')}
                    disabled={actionLoading === 'run-document-analysis'}
                    sx={{ backgroundColor: '#f44336', '&:hover': { backgroundColor: '#d32f2f' } }}
                  >
                    {actionLoading === 'run-document-analysis' ? (
                      <>
                        <CircularProgress size={16} sx={{ mr: 1, color: 'white' }} />
                        Analyzing...
                      </>
                    ) : (
                      'Run Analysis'
                    )}
                  </Button>
                </Paper>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Admin;