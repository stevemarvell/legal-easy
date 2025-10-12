import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
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
  Stack,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
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
  Folder as FolderIcon,
  Email as EmailIcon,
  Assignment as AssignmentIcon,
  Gavel as EvidenceIcon,
  Analytics as AnalyticsIcon,
  Search as ResearchIcon,
  Info as InfoIcon,
  AccountTree as PlaybookTreeIcon,
  ExpandMore as ExpandMoreIcon,
  Psychology as ClaudeIcon,
  Lightbulb as RecommendationIcon
} from '@mui/icons-material';
import { apiClient } from '../../services/api';
import { Case, Document } from '../../types/api';
import SharedLayout from '../layout/SharedLayout';
// Playbook Decision Interface Component
interface PlaybookDecisionInterfaceProps {
  caseId: string;
  playbookId: string;
  playbookName: string;
}

interface DecisionNode {
  id: string;
  question: string;
  options: Record<string, string>;
  researchContext: string[];
  completed?: boolean;
  selectedOption?: string;
  rationale?: string;
  confidence?: number;
}

interface DecisionSession {
  sessionId: string;
  currentNodeId: string;
  decisionHistory: DecisionNode[];
  status: 'not_started' | 'active' | 'completed';
  finalRecommendations?: {
    overallAssessment: string;
    strategicRecommendations: string[];
    riskAssessment: string;
    nextSteps: string[];
  };
}

const PlaybookDecisionInterface: React.FC<PlaybookDecisionInterfaceProps> = ({ 
  caseId, 
  playbookId, 
  playbookName 
}) => {
  const [session, setSession] = useState<DecisionSession | null>(null);
  const [currentDecision, setCurrentDecision] = useState<DecisionNode | null>(null);
  const [decisionDialogOpen, setDecisionDialogOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState('');
  const [decisionRationale, setDecisionRationale] = useState('');
  const [loading, setLoading] = useState(false);

  // Mock decision tree data
  const mockDecisionTree: Record<string, DecisionNode> = {
    'start': {
      id: 'start',
      question: 'What is the primary legal issue in this case?',
      options: {
        'Contract Breach': 'contract_analysis',
        'Employment Dispute': 'employment_analysis',
        'Liability Claim': 'liability_analysis'
      },
      researchContext: [
        'Review case documents for contract terms',
        'Identify parties and their obligations',
        'Assess damages and remedies available'
      ]
    },
    'contract_analysis': {
      id: 'contract_analysis',
      question: 'Is there a valid contract between the parties?',
      options: {
        'Yes, valid contract exists': 'breach_assessment',
        'No, contract is invalid': 'no_contract_remedies',
        'Unclear, needs further analysis': 'contract_validity_research'
      },
      researchContext: [
        'Check contract formation elements',
        'Review consideration and capacity',
        'Examine contract terms and conditions'
      ]
    },
    'employment_analysis': {
      id: 'employment_analysis',
      question: 'What type of employment issue is this?',
      options: {
        'Wrongful Termination': 'termination_analysis',
        'Discrimination': 'discrimination_analysis',
        'Wage and Hour': 'wage_analysis'
      },
      researchContext: [
        'Review employment contract terms',
        'Check applicable labor laws',
        'Examine company policies and procedures'
      ]
    }
  };

  const startSession = () => {
    const newSession: DecisionSession = {
      sessionId: `session_${Date.now()}`,
      currentNodeId: 'start',
      decisionHistory: [],
      status: 'active'
    };
    setSession(newSession);
    setCurrentDecision(mockDecisionTree['start']);
  };

  const openDecisionDialog = (option: string) => {
    setSelectedOption(option);
    setDecisionRationale('');
    setDecisionDialogOpen(true);
  };

  const submitDecision = () => {
    if (!currentDecision || !session || !selectedOption) return;

    setLoading(true);

    // Simulate API call delay
    setTimeout(() => {
      const completedDecision: DecisionNode = {
        ...currentDecision,
        completed: true,
        selectedOption,
        rationale: decisionRationale,
        confidence: 0.85 // Mock confidence score
      };

      const updatedSession: DecisionSession = {
        ...session,
        decisionHistory: [...session.decisionHistory, completedDecision]
      };

      const nextNodeId = currentDecision.options[selectedOption];
      const nextNode = mockDecisionTree[nextNodeId];

      if (nextNode) {
        updatedSession.currentNodeId = nextNodeId;
        setCurrentDecision(nextNode);
      } else {
        // Session completed
        updatedSession.status = 'completed';
        updatedSession.finalRecommendations = {
          overallAssessment: 'Based on the decision path taken, this case shows strong potential for a favorable outcome.',
          strategicRecommendations: [
            'Gather additional evidence to support contract breach claim',
            'Consider settlement negotiations before proceeding to trial',
            'Prepare for potential counterclaims from defendant'
          ],
          riskAssessment: 'Medium risk - case has solid foundation but some uncertainties remain',
          nextSteps: [
            'Complete discovery process',
            'Depose key witnesses',
            'Prepare motion for summary judgment',
            'Develop trial strategy'
          ]
        };
        setCurrentDecision(null);
      }

      setSession(updatedSession);
      setDecisionDialogOpen(false);
      setSelectedOption('');
      setDecisionRationale('');
      setLoading(false);
    }, 1500);
  };

  if (!session) {
    return (
      <Box data-testid="playbook-tab-content">
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <PlaybookTreeIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Playbook Decision Tree
              </Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />

            <Box textAlign="center" py={4}>
              <ClaudeIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                {playbookName}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3, maxWidth: 600, mx: 'auto' }}>
                Start a Claude-driven playbook decision session to systematically work through 
                the decision tree with AI assistance. Claude will help make informed decisions 
                based on case research and legal analysis.
              </Typography>
              <Button
                variant="contained"
                size="large"
                startIcon={<ClaudeIcon />}
                onClick={startSession}
              >
                Start Claude Decision Session
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Box>
    );
  }

  if (session.status === 'completed' && session.finalRecommendations) {
    return (
      <Box data-testid="playbook-final-recommendations">
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <RecommendationIcon color="success" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Final Recommendations
              </Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />

            <Typography variant="h6" gutterBottom>
              Overall Assessment
            </Typography>
            <Typography variant="body1" sx={{ mb: 3 }}>
              {session.finalRecommendations.overallAssessment}
            </Typography>

            <Typography variant="h6" gutterBottom>
              Strategic Recommendations
            </Typography>
            <List>
              {session.finalRecommendations.strategicRecommendations.map((rec, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`• ${rec}`} />
                </ListItem>
              ))}
            </List>

            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Risk Assessment
            </Typography>
            <Typography variant="body1" sx={{ mb: 3 }}>
              {session.finalRecommendations.riskAssessment}
            </Typography>

            <Typography variant="h6" gutterBottom>
              Next Steps
            </Typography>
            <List>
              {session.finalRecommendations.nextSteps.map((step, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${index + 1}. ${step}`} />
                </ListItem>
              ))}
            </List>

            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Decision Path Taken
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap">
              {session.decisionHistory.map((decision, index) => (
                <Chip
                  key={index}
                  label={`${decision.question.substring(0, 30)}... → ${decision.selectedOption}`}
                  variant="outlined"
                  size="small"
                  sx={{ mb: 1 }}
                />
              ))}
            </Stack>

            <Button
              variant="outlined"
              onClick={() => setSession(null)}
              sx={{ mt: 3 }}
            >
              Start New Session
            </Button>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return (
    <Box data-testid="playbook-decision-interface">
      {/* Decision Progress */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center">
              <PlaybookTreeIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                {playbookName}
              </Typography>
            </Box>
            <Chip
              label={`${session.decisionHistory.length} decisions made`}
              color="primary"
              size="small"
            />
          </Box>
          <Divider sx={{ mb: 3 }} />

          {/* Decision History */}
          {session.decisionHistory.length > 0 && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Decision History
              </Typography>
              {session.decisionHistory.map((decision, index) => (
                <Accordion key={decision.id} sx={{ mb: 1 }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Box display="flex" alignItems="center" width="100%">
                      <CheckCircleIcon color="success" sx={{ mr: 2 }} />
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                        {decision.question}
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box>
                      <Typography variant="body2" sx={{ mb: 2 }}>
                        <strong>Selected Option:</strong> {decision.selectedOption}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 2 }}>
                        <strong>Rationale:</strong> {decision.rationale}
                      </Typography>
                      <Chip
                        label={`${Math.round((decision.confidence || 0) * 100)}% confidence`}
                        color={(decision.confidence || 0) >= 0.8 ? 'success' : (decision.confidence || 0) >= 0.6 ? 'warning' : 'error'}
                        size="small"
                      />
                    </Box>
                  </AccordionDetails>
                </Accordion>
              ))}
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Current Decision */}
      {currentDecision && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <ClaudeIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h6">
                Current Decision
              </Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />

            <Typography variant="h6" gutterBottom>
              {currentDecision.question}
            </Typography>

            {currentDecision.researchContext.length > 0 && (
              <Box sx={{ mb: 3, p: 2, bgcolor: 'info.light', borderRadius: 1 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Relevant Research Context:
                </Typography>
                <List dense>
                  {currentDecision.researchContext.map((context, index) => (
                    <ListItem key={index} sx={{ py: 0.5, pl: 2 }}>
                      <Typography variant="body2">• {context}</Typography>
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            <Typography variant="subtitle2" gutterBottom sx={{ mt: 3 }}>
              Available Options:
            </Typography>
            <Stack spacing={2}>
              {Object.entries(currentDecision.options).map(([option, nextNode]) => (
                <Button
                  key={option}
                  variant="outlined"
                  fullWidth
                  onClick={() => openDecisionDialog(option)}
                  sx={{ justifyContent: 'flex-start', textAlign: 'left' }}
                >
                  {option}
                </Button>
              ))}
            </Stack>
          </CardContent>
        </Card>
      )}

      {/* Decision Dialog */}
      <Dialog
        open={decisionDialogOpen}
        onClose={() => setDecisionDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Make Decision: {selectedOption}
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Provide the rationale for choosing this option. This will be recorded as part of the decision history.
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Decision Rationale"
            value={decisionRationale}
            onChange={(e) => setDecisionRationale(e.target.value)}
            placeholder="Explain why this option was chosen based on the case facts, research, and legal analysis..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDecisionDialogOpen(false)}>
            Cancel
          </Button>
          <Button
            onClick={submitDecision}
            variant="contained"
            disabled={!decisionRationale.trim() || loading}
            startIcon={loading ? <CircularProgress size={16} /> : null}
          >
            {loading ? 'Processing...' : 'Submit Decision'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

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
            Created: {new Date(caseData.created_date).toLocaleDateString('en-GB')}
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
              data-testid="overview-tab"
            />
            <Tab
              icon={<AssignmentIcon />}
              label="Details"
              iconPosition="start"
              sx={{ minHeight: 48 }}
              data-testid="details-tab"
            />
            <Tab
              icon={<AnalyticsIcon />}
              label="Documents with Analysis"
              iconPosition="start"
              sx={{ minHeight: 48 }}
              data-testid="documents-analysis-tab"
            />
            <Tab
              icon={<ResearchIcon />}
              label="Research with Details"
              iconPosition="start"
              sx={{ minHeight: 48 }}
              data-testid="research-details-tab"
            />
            <Tab
              icon={<PlaybookTreeIcon />}
              label="Playbook"
              iconPosition="start"
              sx={{ minHeight: 48 }}
              data-testid="playbook-tab"
            />
          </Tabs>
        </Box>

        <Box sx={{ mt: 3 }}>
          {/* Overview Tab */}
          {activeTab === 0 && (
            <Box data-testid="overview-tab-content">
              {/* Essential Case Information */}
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
                          {new Date(caseData.created_date).toLocaleDateString('en-GB')}
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
          
          {/* Details Tab */}
          {activeTab === 1 && (
            <Card sx={{ mb: 4 }} data-testid="details-tab-content">
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom>
                  Comprehensive Case Details
                </Typography>
                <Divider sx={{ mb: 3 }} />

                {caseData.description ? (
                  <Box
                    data-testid="case-full-description"
                    sx={{
                      '& h2': {
                        color: 'primary.main',
                        fontSize: '1.5rem',
                        fontWeight: 600,
                        mt: 3,
                        mb: 2,
                        '&:first-of-type': { mt: 0 }
                      },
                      '& h3': {
                        color: 'primary.dark',
                        fontSize: '1.25rem',
                        fontWeight: 500,
                        mt: 2.5,
                        mb: 1.5
                      },
                      '& p': {
                        lineHeight: 1.8,
                        textAlign: 'justify',
                        mb: 2,
                        fontSize: '1rem'
                      },
                      '& ul, & ol': {
                        mb: 2,
                        pl: 3
                      },
                      '& li': {
                        mb: 0.5,
                        lineHeight: 1.6
                      },
                      '& strong': {
                        color: 'text.primary',
                        fontWeight: 600
                      },
                      '& em': {
                        fontStyle: 'italic',
                        color: 'text.secondary'
                      }
                    }}
                  >
                    <ReactMarkdown>{caseData.description}</ReactMarkdown>
                  </Box>
                ) : (
                  <Box textAlign="center" py={4}>
                    <AssignmentIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      No detailed description available for this case
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      The case summary is available in the Overview tab
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          )}
          
          {/* Documents with Analysis Tab */}
          {activeTab === 2 && (
            <Card sx={{ mb: 4 }} data-testid="documents-analysis-tab-content">
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
                      label={`${caseDocuments.filter(doc => doc.analysis_completed).length}/${caseDocuments.length} analyzed`}
                      color={caseDocuments.every(doc => doc.analysis_completed) ? 'success' : 'warning'}
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
                    {caseDocuments.map((doc, index) => (
                      <ListItem key={doc.id} divider={index < caseDocuments.length - 1} sx={{ flexDirection: 'column', alignItems: 'stretch' }}>
                        {/* Document Header */}
                        <Box display="flex" alignItems="center" width="100%" mb={1}>
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
                            {getAnalysisStatusIcon(doc.analysis_completed)}
                            <Typography variant="caption" color="text.secondary" ml={1}>
                              {getAnalysisStatusText(doc.analysis_completed)}
                            </Typography>
                          </Box>
                        </Box>

                        {/* Analysis Results Placeholder */}
                        {doc.analysis_completed && (
                          <Box sx={{ ml: 6, mt: 1, p: 2, bgcolor: 'grey.50', borderRadius: 1 }} data-testid="analysis-results">
                            <Typography variant="subtitle2" color="primary" gutterBottom>
                              Analysis Results
                            </Typography>
                            <Typography variant="body2" sx={{ mb: 1 }}>
                              <strong>Summary:</strong> Document analysis completed. Key information extracted and processed.
                            </Typography>
                            <Chip
                              label="85% confidence"
                              color="success"
                              size="small"
                            />
                          </Box>
                        )}
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

                {caseDocuments.length > 0 && (
                  <Stack direction="row" spacing={2} sx={{ mt: 3 }}>
                    <Button
                      variant="outlined"
                      fullWidth
                      onClick={() => window.open(`/cases/${caseId}/documents`, '_blank')}
                    >
                      View All Documents
                    </Button>
                    {caseDocuments.some(doc => !doc.analysis_completed) && (
                      <Button
                        variant="contained"
                        fullWidth
                        onClick={() => {
                          console.log('Analyzing all pending documents...');
                        }}
                      >
                        Analyze All Pending
                      </Button>
                    )}
                  </Stack>
                )}
              </CardContent>
            </Card>
          )}
          
          {/* Research with Details Tab */}
          {activeTab === 3 && (
            <Box data-testid="research-details-tab-content">
              <Card sx={{ mb: 4 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <ResearchIcon color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h5" component="h2">
                      Research with Details
                    </Typography>
                  </Box>
                  <Divider sx={{ mb: 3 }} />

                  <Box textAlign="center" py={4}>
                    <ResearchIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
                    <Typography variant="h6" gutterBottom>
                      Generate Research List
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 3, maxWidth: 600, mx: 'auto' }}>
                      Generate a comprehensive research list based on case files and document analysis. 
                      This will identify key legal concepts, relevant precedents, applicable statutes, 
                      and factual research needs to support Claude-driven playbook decisions.
                    </Typography>
                    <Button
                      variant="contained"
                      size="large"
                      startIcon={<ResearchIcon />}
                      onClick={() => {
                        console.log('Generating research list...');
                      }}
                    >
                      Generate Research List
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          )}
          
          {/* Playbook Tab */}
          {activeTab === 4 && (
            <PlaybookDecisionInterface 
              caseId={caseId!}
              playbookId={caseData.playbook_id}
              playbookName={getPlaybookName(caseData.playbook_id)}
            />
          )}
        </Box>
      </Box>
    </SharedLayout>
  );
};

export default CaseDetail;