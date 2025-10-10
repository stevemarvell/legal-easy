import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  Breadcrumbs,
  Link,
  Button,
  Chip,
  Grid,
  Tabs,
  Tab,
  Divider
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Home as HomeIcon,
  Assessment as AnalysisIcon,
  MenuBook as PlaybookIcon,
  Folder as CaseIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';
import { playbookService } from '../services/playbookService';
import ComprehensiveAnalysisComponent from '../components/CaseAnalysis/ComprehensiveAnalysis';
import { Case } from '../types/api';
import { Playbook, ComprehensiveAnalysis } from '../types/playbook';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`case-analysis-tabpanel-${index}`}
      aria-labelledby={`case-analysis-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ pt: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const CaseAnalysis: React.FC = () => {
  const { caseId } = useParams<{ caseId: string }>();
  const navigate = useNavigate();
  const [caseData, setCaseData] = useState<Case | null>(null);
  const [matchedPlaybook, setMatchedPlaybook] = useState<Playbook | null>(null);
  const [analysis, setAnalysis] = useState<ComprehensiveAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    if (caseId) {
      fetchCaseData();
    }
  }, [caseId]);

  const fetchCaseData = async () => {
    if (!caseId) return;

    try {
      setLoading(true);
      setError(null);

      // Fetch case data
      const caseResponse = await apiClient.get<Case[]>('/api/cases/');
      const cases = caseResponse.data;
      const foundCase = cases.find(c => c.id === caseId);

      if (!foundCase) {
        setError(`Case with ID ${caseId} not found`);
        return;
      }

      setCaseData(foundCase);

      // Try to match a playbook for this case type
      try {
        const playbook = await playbookService.matchPlaybook(foundCase.case_type);
        setMatchedPlaybook(playbook);
      } catch (err) {
        console.warn('No playbook found for case type:', foundCase.case_type);
        setMatchedPlaybook(null);
      }

    } catch (err: any) {
      console.error('Failed to fetch case data:', err);
      setError(err.message || 'Failed to load case data');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleAnalysisComplete = (analysisResult: ComprehensiveAnalysis) => {
    setAnalysis(analysisResult);
  };

  const handleBreadcrumbNavigation = (path: string) => {
    navigate(path);
  };

  if (!caseId) {
    return (
      <Container maxWidth="xl">
        <Alert severity="error">
          No case ID provided in the URL.
        </Alert>
      </Container>
    );
  }

  if (loading) {
    return (
      <Container maxWidth="xl">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error || !caseData) {
    return (
      <Container maxWidth="xl">
        <Alert severity="error" sx={{ mb: 4 }}>
          {error || 'Case data not found'}
        </Alert>
        <Button
          variant="outlined"
          onClick={() => navigate('/cases')}
        >
          Back to Cases
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box>
        {/* Header with Navigation */}
        <Box mb={4}>
          <Button
            variant="outlined"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/cases')}
            sx={{ mb: 2 }}
          >
            Back to Cases
          </Button>

          {/* Breadcrumbs */}
          <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
            <Link
              component="button"
              variant="body2"
              onClick={() => handleBreadcrumbNavigation('/')}
              sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
            >
              <HomeIcon sx={{ mr: 0.5 }} fontSize="inherit" />
              Dashboard
            </Link>
            <Link
              component="button"
              variant="body2"
              onClick={() => handleBreadcrumbNavigation('/cases')}
              sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
            >
              <CaseIcon sx={{ mr: 0.5 }} fontSize="inherit" />
              Cases
            </Link>
            <Typography color="text.primary" variant="body2">
              Case Analysis
            </Typography>
          </Breadcrumbs>
        </Box>

        {/* Case Header */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={8}>
                <Typography variant="h4" component="h1" color="primary" gutterBottom>
                  {caseData.title}
                </Typography>
                <Typography variant="body1" color="text.secondary" paragraph>
                  {caseData.summary}
                </Typography>
                <Box display="flex" gap={1} flexWrap="wrap">
                  <Chip label={caseData.case_type} color="primary" variant="outlined" />
                  <Chip label={caseData.status} color="secondary" variant="outlined" />
                  <Chip label={`Client: ${caseData.client_name}`} variant="outlined" />
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Case Information
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    <strong>Case ID:</strong> {caseData.id}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    <strong>Created:</strong> {new Date(caseData.created_date).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    <strong>Documents:</strong> {caseData.documents.length}
                  </Typography>
                  {matchedPlaybook && (
                    <Box mt={2}>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        <strong>Matched Playbook:</strong>
                      </Typography>
                      <Box display="flex" alignItems="center" gap={1}>
                        <PlaybookIcon color="primary" fontSize="small" />
                        <Typography variant="body2">
                          {matchedPlaybook.name}
                        </Typography>
                      </Box>
                    </Box>
                  )}
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Playbook Status */}
        {!matchedPlaybook && (
          <Alert severity="warning" sx={{ mb: 4 }}>
            <Typography variant="body1" gutterBottom>
              <strong>No Playbook Available</strong>
            </Typography>
            <Typography variant="body2">
              No specific playbook was found for case type "{caseData.case_type}". 
              The analysis will use general legal principles and fallback recommendations.
            </Typography>
          </Alert>
        )}

        {/* Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="case analysis tabs">
            <Tab 
              label="Comprehensive Analysis" 
              icon={<AnalysisIcon />} 
              iconPosition="start"
            />
            {matchedPlaybook && (
              <Tab 
                label="Playbook Details" 
                icon={<PlaybookIcon />} 
                iconPosition="start"
              />
            )}
          </Tabs>
        </Box>

        {/* Tab Panels */}
        <TabPanel value={tabValue} index={0}>
          <ComprehensiveAnalysisComponent 
            caseId={caseId} 
            onAnalysisComplete={handleAnalysisComplete}
          />
        </TabPanel>

        {matchedPlaybook && (
          <TabPanel value={tabValue} index={1}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  {matchedPlaybook.name}
                </Typography>
                <Typography variant="body1" color="text.secondary" paragraph>
                  {matchedPlaybook.description}
                </Typography>
                
                <Divider sx={{ my: 3 }} />
                
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Playbook Information
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Case Type:</strong> {matchedPlaybook.case_type}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Version:</strong> {matchedPlaybook.version || 'N/A'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Last Updated:</strong> {matchedPlaybook.last_updated ? new Date(matchedPlaybook.last_updated).toLocaleDateString() : 'N/A'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Rules:</strong> {matchedPlaybook.rules.length}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Key Features
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      • {matchedPlaybook.rules.length} decision rules
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      • {Object.keys(matchedPlaybook.monetary_ranges).length} monetary assessment ranges
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      • {matchedPlaybook.escalation_paths.length} escalation steps
                    </Typography>
                    {matchedPlaybook.key_statutes && (
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        • {matchedPlaybook.key_statutes.length} key statutes referenced
                      </Typography>
                    )}
                  </Grid>
                </Grid>

                {matchedPlaybook.key_statutes && matchedPlaybook.key_statutes.length > 0 && (
                  <Box mt={3}>
                    <Typography variant="h6" gutterBottom>
                      Key Statutes
                    </Typography>
                    <Box display="flex" flexWrap="wrap" gap={1}>
                      {matchedPlaybook.key_statutes.map((statute, index) => (
                        <Chip key={index} label={statute} variant="outlined" size="small" />
                      ))}
                    </Box>
                  </Box>
                )}
              </CardContent>
            </Card>
          </TabPanel>
        )}
      </Box>
    </Container>
  );
};

export default CaseAnalysis;