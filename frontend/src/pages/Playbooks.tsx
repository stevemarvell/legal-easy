import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CardActionArea,
  Alert,
  CircularProgress,
  Breadcrumbs,
  Link,
  Button,
  Chip,
  Divider
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Home as HomeIcon,
  MenuBook as PlaybookIcon,
  Gavel as RuleIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';
import PlaybookViewer from '../components/Playbook/PlaybookViewer';
import { Playbook } from '../types/api';

const Playbooks: React.FC = () => {
  const { caseType } = useParams<{ caseType: string }>();
  const navigate = useNavigate();
  const [playbooks, setPlaybooks] = useState<Playbook[]>([]);
  const [selectedPlaybook, setSelectedPlaybook] = useState<Playbook | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPlaybooks();
  }, []);

  useEffect(() => {
    if (caseType && playbooks.length > 0) {
      const playbook = playbooks.find(p => p.case_type === decodeURIComponent(caseType));
      if (playbook) {
        setSelectedPlaybook(playbook);
      } else {
        setError(`No playbook found for case type: ${decodeURIComponent(caseType)}`);
      }
    }
  }, [caseType, playbooks]);

  const fetchPlaybooks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.get<Playbook[]>('/api/playbooks/');
      setPlaybooks(response.data);
    } catch (err) {
      console.error('Failed to fetch playbooks:', err);
      setError('Failed to load playbooks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePlaybookSelect = (playbook: Playbook) => {
    setSelectedPlaybook(playbook);
    navigate(`/playbooks/${encodeURIComponent(playbook.case_type)}`);
  };

  const handleBackToList = () => {
    setSelectedPlaybook(null);
    navigate('/playbooks');
  };

  const handleBreadcrumbNavigation = (path: string) => {
    navigate(path);
  };

  if (loading) {
    return (
      <Container maxWidth="xl">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error && !selectedPlaybook) {
    return (
      <Container maxWidth="xl">
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
        <Button
          variant="outlined"
          onClick={fetchPlaybooks}
        >
          Retry
        </Button>
      </Container>
    );
  }

  // If a specific playbook is selected, show the PlaybookViewer
  if (selectedPlaybook) {
    return (
      <Container maxWidth="xl">
        <Box>
          {/* Header with Navigation */}
          <Box mb={4}>
            <Button
              variant="outlined"
              startIcon={<ArrowBackIcon />}
              onClick={handleBackToList}
              sx={{ mb: 2 }}
            >
              Back to Playbooks
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
                onClick={handleBackToList}
                sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
              >
                <PlaybookIcon sx={{ mr: 0.5 }} fontSize="inherit" />
                Playbooks
              </Link>
              <Typography color="text.primary" variant="body2">
                {selectedPlaybook.case_type}
              </Typography>
            </Breadcrumbs>
          </Box>

          {/* PlaybookViewer Component */}
          <PlaybookViewer caseType={selectedPlaybook.case_type} />
        </Box>
      </Container>
    );
  }

  // Show playbooks list
  return (
    <Container maxWidth="xl">
      <Box>
        {/* Header */}
        <Box mb={4}>
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
            <Typography color="text.primary" variant="body2">
              Playbooks
            </Typography>
          </Breadcrumbs>

          <Typography variant="h3" component="h1" color="primary" gutterBottom>
            Legal Playbooks
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            AI-powered legal decision frameworks and rule sets
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Explore our comprehensive collection of legal playbooks that guide case assessment,
            provide decision frameworks, and offer strategic recommendations for different types of legal matters.
          </Typography>
        </Box>

        {/* Playbooks Grid */}
        {playbooks.length === 0 ? (
          <Alert severity="info">
            No playbooks are currently available in the system.
          </Alert>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            {playbooks.map((playbook) => (
              <Card
                key={playbook.id}
                sx={{
                  transition: 'all 0.2s ease-in-out',
                  border: '1px solid',
                  borderColor: 'divider',
                  backgroundColor: '#161821', // Dark background
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: 4,
                    borderColor: 'primary.main'
                  }
                }}
              >
                <CardActionArea onClick={() => handlePlaybookSelect(playbook)}>
                  <CardContent sx={{ p: 4 }}>
                    <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
                      {/* Main Content */}
                      <Box sx={{ flex: 1 }}>
                        <Box mb={2}>
                          <Box display="flex" alignItems="center" gap={2} mb={1}>
                            <PlaybookIcon color="primary" sx={{ fontSize: 32 }} />
                            <Typography variant="h5" component="h2" sx={{ color: 'white' }}>
                              {playbook.name}
                            </Typography>
                          </Box>
                          <Chip
                            label={playbook.case_type}
                            sx={{
                              color: 'white',
                              borderColor: '#744EFD',
                              '&.MuiChip-outlined': {
                                borderColor: '#744EFD'
                              }
                            }}
                            variant="outlined"
                            size="small"
                          />
                        </Box>

                        <Typography variant="body1" sx={{ color: 'white', mb: 3 }}>
                          {playbook.description || `Comprehensive legal framework for ${playbook.case_type} cases, including decision rules, assessment criteria, and strategic recommendations.`}
                        </Typography>

                        {/* Playbook Stats */}
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
                          <Box display="flex" alignItems="center" gap={1}>
                            <RuleIcon sx={{ color: '#744EFD' }} fontSize="small" />
                            <Typography variant="body2" sx={{ color: 'white' }}>
                              {playbook.rules?.length || 0} Rules
                            </Typography>
                          </Box>

                          <Box display="flex" alignItems="center" gap={1}>
                            <AssessmentIcon sx={{ color: '#744EFD' }} fontSize="small" />
                            <Typography variant="body2" sx={{ color: 'white' }}>
                              {Object.keys(playbook.monetary_ranges || {}).length} Assessment Ranges
                            </Typography>
                          </Box>

                          {playbook.escalation_paths && playbook.escalation_paths.length > 0 && (
                            <Box display="flex" alignItems="center" gap={1}>
                              <Typography variant="body2" sx={{ color: 'white' }}>
                                {playbook.escalation_paths.length} Escalation Paths
                              </Typography>
                            </Box>
                          )}
                        </Box>
                      </Box>

                      {/* Quick Preview */}
                      <Box sx={{ width: { xs: '100%', md: '300px' } }}>
                        <Typography variant="subtitle2" sx={{ color: 'white' }} gutterBottom>
                          Key Features
                        </Typography>
                        <Divider sx={{ mb: 2, borderColor: 'rgba(255, 255, 255, 0.3)' }} />
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                          <Typography variant="body2" sx={{ color: 'white' }}>
                            • Automated rule application
                          </Typography>
                          <Typography variant="body2" sx={{ color: 'white' }}>
                            • Case strength assessment
                          </Typography>
                          <Typography variant="body2" sx={{ color: 'white' }}>
                            • Strategic recommendations
                          </Typography>
                          <Typography variant="body2" sx={{ color: 'white' }}>
                            • Monetary range guidance
                          </Typography>
                          {playbook.escalation_paths && playbook.escalation_paths.length > 0 && (
                            <Typography variant="body2" sx={{ color: 'white' }}>
                              • Escalation procedures
                            </Typography>
                          )}
                        </Box>
                      </Box>
                    </Box>
                  </CardContent>
                </CardActionArea>
              </Card>
            ))}
          </Box>
        )}

        {/* Help Section */}
        <Card sx={{ mt: 4, backgroundColor: 'grey.50' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              About Legal Playbooks
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Legal playbooks are AI-powered frameworks that provide structured approaches to different types of legal cases.
              Each playbook contains decision rules, assessment criteria, monetary ranges, and strategic recommendations
              tailored to specific case types. They help ensure consistent, thorough case evaluation and provide
              evidence-based guidance for legal strategy.
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Playbooks;