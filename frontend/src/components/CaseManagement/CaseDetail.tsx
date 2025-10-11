import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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
  Alert,
  CircularProgress,
  ListItemIcon,
  Paper,
  Stack,
  Tabs,
  Tab
} from '@mui/material';
import {
  Person as PersonIcon,
  Description as DocumentIcon,
  Gavel as GavelIcon,
  Schedule as ScheduleIcon,
  Group as GroupIcon,
  MenuBook as PlaybookIcon,
  CheckCircle as CheckCircleIcon,
  HourglassEmpty as HourglassEmptyIcon,
  Error as ErrorIcon,
  Folder as FolderIcon,
  Email as EmailIcon,
  Assignment as AssignmentIcon,
  Gavel as EvidenceIcon,
  Analytics as AnalyticsIcon,
  Timeline as TimelineIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { apiClient } from '../../services/api';
import { Case, Document } from '../../types/api';
import SharedLayout from '../layout/SharedLayout';
import IntegratedCaseAnalysis from './IntegratedCaseAnalysis';

const CaseDetail: React.FC = () => {
  const { caseId } = useParams<{ caseId: string }>();
  const navigate = useNavigate();
  const [caseData, setCaseData] = useState<Case | null>(null);
  const [caseDocuments, setCaseDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [documentsLoading, setDocumentsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    const fetchCaseDetail = async () => {
      if (!caseId) return;

      try {
        setLoading(true);
        setError(null);
        const response = await apiClient.get<Case>(`/api/cases/${caseId}`);

        setCaseData(response.data);
      } catch (err) {
        console.error('Failed to fetch case details:', err);
        setError('Failed to load case details. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    const fetchCaseDocuments = async () => {
      if (!caseId) return;



      try {
        setDocumentsLoading(true);
        const response = await apiClient.get<Document[]>(`/api/documents/cases/${caseId}/documents`);

        setCaseDocuments(response.data);
      } catch (err) {
        console.error('Failed to fetch case documents:', err);
        // Don't set error for documents, just log it
      } finally {
        setDocumentsLoading(false);
      }
    };

    fetchCaseDetail();
    fetchCaseDocuments();
  }, [caseId]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active': return 'success';
      case 'Under Review': return 'warning';
      case 'Resolved': return 'info';
      default: return 'default';
    }
  };

  const getPlaybookName = (playbookId: string) => {
    const playbookNames: Record<string, string> = {
      'employment-dispute': 'Employment Law Playbook',
      'contract-breach': 'Contract Breach Playbook',
      'debt-claim': 'Debt Collection Playbook',
      'personal-injury': 'Personal Injury Playbook',
      'intellectual-property': 'IP Protection Playbook'
    };
    return playbookNames[playbookId] || 'General Playbook';
  };

  const getDocumentTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'contract': return <AssignmentIcon />;
      case 'email': return <EmailIcon />;
      case 'evidence': return <EvidenceIcon />;
      case 'legal brief': return <DocumentIcon />;
      default: return <FolderIcon />;
    }
  };

  const getAnalysisStatusIcon = (completed: boolean) => {
    return completed ? <CheckCircleIcon color="success" /> : <HourglassEmptyIcon color="disabled" />;
  };

  const getAnalysisStatusText = (completed: boolean) => {
    return completed ? 'completed' : 'pending';
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getAnalysisStatusCount = () => {
    const completed = caseDocuments.filter(doc => doc.analysis_completed).length;
    const total = caseDocuments.length;
    return { completed, total };
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <SharedLayout
        title="Case Details"
        showBackButton={true}
        backButtonLabel="Back to Cases"
        onBackClick={() => navigate('/cases')}
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'Cases', path: '/cases' },
          { label: 'Case Details' }
        ]}
      >
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </SharedLayout>
    );
  }

  if (error) {
    return (
      <SharedLayout
        title="Case Details"
        showBackButton={true}
        backButtonLabel="Back to Cases"
        onBackClick={() => navigate('/cases')}
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'Cases', path: '/cases' },
          { label: 'Case Details' }
        ]}
      >
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      </SharedLayout>
    );
  }

  if (!caseData) {
    return (
      <SharedLayout
        title="Case Details"
        showBackButton={true}
        backButtonLabel="Back to Cases"
        onBackClick={() => navigate('/cases')}
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'Cases', path: '/cases' },
          { label: 'Case Details' }
        ]}
      >
        <Alert severity="warning" sx={{ mb: 4 }}>
          Case not found
        </Alert>
      </SharedLayout>
    );
  }

  const analysisStatus = getAnalysisStatusCount();

  return (
    <SharedLayout
      title={caseData.title}
      subtitle={`Case ID: ${caseData.id}`}
      showBackButton={true}
      backButtonLabel="Back to Cases"
      onBackClick={() => navigate('/cases')}
      breadcrumbs={[
        { label: 'Dashboard', path: '/' },
        { label: 'Cases', path: '/cases' },
        { label: caseData.title }
      ]}
    >
      {/* Status Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Stack direction="row" spacing={2} alignItems="center">
          <Chip
            label={caseData.status}
            color={getStatusColor(caseData.status) as any}
            size="medium"
          />
          <Typography variant="body2" color="text.secondary">
            Created: {new Date(caseData.created_date).toLocaleDateString()}
          </Typography>
        </Stack>
      </Box>

      {/* Tabbed Interface */}
      <Box sx={{ width: '100%', mb: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={handleTabChange} aria-label="case detail tabs">
            <Tab
              icon={<InfoIcon />}
              label="Overview"
              iconPosition="start"
              sx={{ minHeight: 48 }}
            />
            <Tab
              icon={<DocumentIcon />}
              label="Documents"
              iconPosition="start"
              sx={{ minHeight: 48 }}
            />
            <Tab
              icon={<AnalyticsIcon />}
              label="Analysis"
              iconPosition="start"
              sx={{ minHeight: 48 }}
              disabled={analysisStatus.completed === 0}
            />
            <Tab
              icon={<TimelineIcon />}
              label="Timeline"
              iconPosition="start"
              sx={{ minHeight: 48 }}
            />
          </Tabs>
        </Box>

        <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={4} sx={{ mt: 3 }}>
          {/* Main Content */}
          <Box flex={2}>
            {/* Overview Tab */}
            {activeTab === 0 && (
              <Box>
                {/* Comprehensive Case Metadata */}
                <Card sx={{ mb: 4 }} data-testid="case-overview">
                  <CardContent>
                    <Typography variant="h5" component="h2" gutterBottom>
                      Case Overview
                    </Typography>
                    <Divider sx={{ mb: 3 }} />

                    <Box display="flex" flexDirection="column" gap={3}>
                      <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={3}>
                        <Box flex={1}>
                          <Box display="flex" alignItems="center" mb={2}>
                            <PersonIcon color="primary" sx={{ mr: 1 }} />
                            <Typography variant="h6">Client</Typography>
                          </Box>
                          <Typography variant="body1" color="text.secondary" data-testid="case-client">
                            {caseData.client_name}
                          </Typography>
                        </Box>

                        <Box flex={1}>
                          <Box display="flex" alignItems="center" mb={2}>
                            <GavelIcon color="primary" sx={{ mr: 1 }} />
                            <Typography variant="h6">Case Type</Typography>
                          </Box>
                          <Typography variant="body1" color="text.secondary" data-testid="case-type">
                            {caseData.case_type}
                          </Typography>
                        </Box>
                      </Box>

                      <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={3}>
                        <Box flex={1}>
                          <Box display="flex" alignItems="center" mb={2}>
                            <ScheduleIcon color="primary" sx={{ mr: 1 }} />
                            <Typography variant="h6">Created Date</Typography>
                          </Box>
                          <Typography variant="body1" color="text.secondary" data-testid="case-created-date">
                            {new Date(caseData.created_date).toLocaleDateString()}
                          </Typography>
                        </Box>

                        <Box flex={1}>
                          <Box display="flex" alignItems="center" mb={2}>
                            <PlaybookIcon color="primary" sx={{ mr: 1 }} />
                            <Typography variant="h6">Assigned Playbook</Typography>
                          </Box>
                          <Typography variant="body1" color="text.secondary" data-testid="case-playbook">
                            {getPlaybookName(caseData.playbook_id)}
                          </Typography>
                        </Box>
                      </Box>

                      <Box>
                        <Typography variant="h6" gutterBottom>
                          Summary
                        </Typography>
                        <Typography variant="body1" color="text.secondary" data-testid="case-summary">
                          {caseData.summary}
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>

                {/* Key Parties */}
                {caseData.key_parties && caseData.key_parties.length > 0 && (
                  <Card sx={{ mb: 4 }} data-testid="key-parties-section">
                    <CardContent>
                      <Box display="flex" alignItems="center" mb={2}>
                        <GroupIcon color="primary" sx={{ mr: 1 }} />
                        <Typography variant="h5" component="h2">
                          Key Parties
                        </Typography>
                      </Box>
                      <Divider sx={{ mb: 3 }} />
                      <List>
                        {caseData.key_parties.map((party, index) => (
                          <ListItem key={index} divider={index < caseData.key_parties.length - 1}>
                            <ListItemIcon>
                              <PersonIcon color="primary" />
                            </ListItemIcon>
                            <ListItemText primary={party} />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                )}
              </Box>
            )}

            {/* Documents Tab */}
            {activeTab === 1 && (
              <Card sx={{ mb: 4 }} data-testid="documents-section">
                <CardContent>
                  <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                    <Box display="flex" alignItems="center">
                      <DocumentIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h5" component="h2">
                        Associated Documents
                      </Typography>
                    </Box>
                    <Chip
                      label={`${caseDocuments.length} document${caseDocuments.length !== 1 ? 's' : ''}`}
                      variant="outlined"
                      size="small"
                    />
                  </Box>
                  <Divider sx={{ mb: 3 }} />

                  {documentsLoading ? (
                    <Box display="flex" justifyContent="center" p={2}>
                      <CircularProgress size={24} />
                    </Box>
                  ) : caseDocuments.length > 0 ? (
                    <List>
                      {caseDocuments.map((doc, index) => (
                        <ListItem key={doc.id} divider={index < caseDocuments.length - 1}>
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
                                onClick={() => navigate(`/cases/${caseId}/documents/${doc.id}`)}
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
                                  Uploaded: {new Date(doc.upload_date).toLocaleDateString()}
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
                            {getAnalysisStatusIcon(doc.analysis_completed)}
                            <Typography variant="caption" color="text.secondary" ml={1}>
                              {getAnalysisStatusText(doc.analysis_completed)}
                            </Typography>
                          </Box>
                        </ListItem>
                      ))}
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

                  <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
                    <Button
                      variant="outlined"
                      fullWidth
                      onClick={() => navigate(`/cases/${caseId}/documents`)}
                    >
                      View All Documents
                    </Button>
                    {caseDocuments.some(doc => !doc.analysis_completed) && (
                      <Button
                        variant="contained"
                        fullWidth
                        onClick={() => {
                          // Trigger analysis for pending documents
                          console.log('Analyzing pending documents...');
                        }}
                      >
                        Analyze Pending
                      </Button>
                    )}
                  </Stack>
                </CardContent>
              </Card>
            )}

            {/* Analysis Tab */}
            {activeTab === 2 && analysisStatus.completed > 0 && (
              <Box>
                <Typography variant="h5" component="h2" gutterBottom>
                  Integrated Case Analysis
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  Comprehensive analysis linking case documents, legal research, and strategic playbooks.
                </Typography>
                <IntegratedCaseAnalysis caseId={caseId!} />
              </Box>
            )}

            {/* Timeline Tab */}
            {activeTab === 3 && (
              <Card sx={{ mb: 4 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <TimelineIcon color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h5" component="h2">
                      Case Timeline
                    </Typography>
                  </Box>
                  <Divider sx={{ mb: 3 }} />

                  <Box>
                    <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                      Timeline functionality will be implemented to show key case events, document uploads,
                      analysis completions, and important milestones.
                    </Typography>

                    {/* Basic timeline for now */}
                    <List>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText
                          primary="Case Created"
                          secondary={new Date(caseData.created_date).toLocaleDateString()}
                        />
                      </ListItem>
                      {caseDocuments.length > 0 && (
                        <ListItem>
                          <ListItemIcon>
                            <DocumentIcon color="primary" />
                          </ListItemIcon>
                          <ListItemText
                            primary={`${caseDocuments.length} Document${caseDocuments.length !== 1 ? 's' : ''} Uploaded`}
                            secondary="Various dates"
                          />
                        </ListItem>
                      )}
                      {analysisStatus.completed > 0 && (
                        <ListItem>
                          <ListItemIcon>
                            <AnalyticsIcon color="secondary" />
                          </ListItemIcon>
                          <ListItemText
                            primary={`${analysisStatus.completed} Document${analysisStatus.completed !== 1 ? 's' : ''} Analyzed`}
                            secondary="Analysis completed"
                          />
                        </ListItem>
                      )}
                    </List>
                  </Box>
                </CardContent>
              </Card>
            )}
          </Box>

          {/* Sidebar */}
          <Box flex={1}>
            {/* Document and Analysis Status Indicators */}
            <Paper sx={{ p: 3, mb: 4 }} data-testid="analysis-status-indicators">
              <Typography variant="h6" gutterBottom>
                Document Analysis Status
              </Typography>
              <Divider sx={{ mb: 2 }} />

              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="body2">Total Documents:</Typography>
                <Chip
                  label={caseDocuments.length}
                  size="small"
                  color={caseDocuments.length > 0 ? 'primary' : 'default'}
                  data-testid="total-document-count"
                />
              </Box>

              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="body2">Analysis Complete:</Typography>
                <Chip
                  label={`${analysisStatus.completed}/${analysisStatus.total}`}
                  size="small"
                  color={analysisStatus.completed === analysisStatus.total && analysisStatus.total > 0 ? 'success' : 'warning'}
                  data-testid="analysis-completion-status"
                />
              </Box>

              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="body2">Pending Analysis:</Typography>
                <Chip
                  label={analysisStatus.total - analysisStatus.completed}
                  size="small"
                  color={analysisStatus.total - analysisStatus.completed > 0 ? 'warning' : 'success'}
                />
              </Box>

              {analysisStatus.total > 0 && (
                <Box mt={2}>
                  <Typography variant="caption" color="text.secondary" display="block">
                    Analysis Progress: {Math.round((analysisStatus.completed / analysisStatus.total) * 100)}%
                  </Typography>
                  <Box
                    sx={{
                      width: '100%',
                      height: 8,
                      backgroundColor: 'grey.300',
                      borderRadius: 1,
                      mt: 1,
                      overflow: 'hidden'
                    }}
                  >
                    <Box
                      sx={{
                        width: `${(analysisStatus.completed / analysisStatus.total) * 100}%`,
                        height: '100%',
                        backgroundColor: analysisStatus.completed === analysisStatus.total ? 'success.main' : 'warning.main',
                        transition: 'width 0.3s ease'
                      }}
                      data-testid="analysis-progress-bar"
                    />
                  </Box>
                </Box>
              )}
            </Paper>

            {/* Quick Analysis Summary */}
            {analysisStatus.completed > 0 && (
              <Card sx={{ mb: 4 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Quick Analysis Summary
                  </Typography>
                  <Divider sx={{ mb: 2 }} />

                  <Box mb={2}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Analysis available for {analysisStatus.completed} document{analysisStatus.completed !== 1 ? 's' : ''}
                    </Typography>
                    <Button
                      variant="outlined"
                      size="small"
                      fullWidth
                      onClick={() => setActiveTab(2)}
                    >
                      View Integrated Analysis
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            )}

            {/* Actions */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Case Actions
                </Typography>
                <Divider sx={{ mb: 2 }} />

                <Stack spacing={2}>
                  <Button
                    variant="contained"
                    fullWidth
                    onClick={() => navigate(`/cases/${caseId}/analysis`)}
                  >
                    Run Comprehensive Analysis
                  </Button>
                  <Button
                    variant="outlined"
                    fullWidth
                    onClick={() => navigate(`/cases/${caseId}/report`)}
                  >
                    Generate Case Report
                  </Button>
                  <Button
                    variant="outlined"
                    fullWidth
                    onClick={() => {
                      // TODO: Implement status update functionality
                      console.log('Update case status');
                    }}
                  >
                    Update Case Status
                  </Button>
                  <Button
                    variant="outlined"
                    fullWidth
                    onClick={() => navigate(`/playbooks/${caseData.playbook_id}`)}
                  >
                    View Playbook
                  </Button>
                </Stack>
              </CardContent>
            </Card>
          </Box>
        </Box>
      </Box>
    </SharedLayout>
  );
};

export default CaseDetail;