import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  Grid,
  Divider,
  List,
  ListItem,
  ListItemText,
  Alert,
  CircularProgress,
  Container
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Person as PersonIcon,
  Description as DocumentIcon,
  Gavel as GavelIcon,
  Schedule as ScheduleIcon
} from '@mui/icons-material';
import { apiClient } from '../../services/api';
import { Case } from '../../types/api';

const CaseDetail: React.FC = () => {
  const { caseId } = useParams<{ caseId: string }>();
  const navigate = useNavigate();
  const [caseData, setCaseData] = useState<Case | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

    fetchCaseDetail();
  }, [caseId]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active': return 'success';
      case 'Under Review': return 'warning';
      case 'Resolved': return 'info';
      default: return 'default';
    }
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

  if (error) {
    return (
      <Container maxWidth="xl">
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
        <Button
          variant="outlined"
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/cases')}
        >
          Back to Cases
        </Button>
      </Container>
    );
  }

  if (!caseData) {
    return (
      <Container maxWidth="xl">
        <Alert severity="warning" sx={{ mb: 4 }}>
          Case not found
        </Alert>
        <Button
          variant="outlined"
          startIcon={<ArrowBackIcon />}
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
        {/* Header */}
        <Box mb={4}>
          <Button
            variant="outlined"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/cases')}
            sx={{ mb: 2 }}
          >
            Back to Cases
          </Button>
          
          <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
            <Box>
              <Typography variant="h3" component="h1" color="primary" gutterBottom>
                {caseData.title}
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Case ID: {caseData.id}
              </Typography>
            </Box>
            <Chip 
              label={caseData.status} 
              color={getStatusColor(caseData.status) as any}
              size="large"
            />
          </Box>
        </Box>

        <Grid container spacing={4}>
          {/* Case Overview */}
          <Grid item xs={12} md={8}>
            <Card sx={{ mb: 4 }}>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom>
                  Case Overview
                </Typography>
                <Divider sx={{ mb: 3 }} />
                
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6}>
                    <Box display="flex" alignItems="center" mb={2}>
                      <PersonIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6">Client</Typography>
                    </Box>
                    <Typography variant="body1" color="text.secondary">
                      {caseData.client_name}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <Box display="flex" alignItems="center" mb={2}>
                      <GavelIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6">Case Type</Typography>
                    </Box>
                    <Typography variant="body1" color="text.secondary">
                      {caseData.case_type}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <Box display="flex" alignItems="center" mb={2}>
                      <ScheduleIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6">Created Date</Typography>
                    </Box>
                    <Typography variant="body1" color="text.secondary">
                      {new Date(caseData.created_date).toLocaleDateString()}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12}>
                    <Typography variant="h6" gutterBottom>
                      Summary
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                      {caseData.summary}
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>

            {/* Key Parties */}
            {caseData.key_parties && caseData.key_parties.length > 0 && (
              <Card sx={{ mb: 4 }}>
                <CardContent>
                  <Typography variant="h5" component="h2" gutterBottom>
                    Key Parties
                  </Typography>
                  <Divider sx={{ mb: 3 }} />
                  <List>
                    {caseData.key_parties.map((party, index) => (
                      <ListItem key={index} divider={index < caseData.key_parties.length - 1}>
                        <ListItemText primary={party} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            )}
          </Grid>

          {/* Sidebar */}
          <Grid item xs={12} md={4}>
            {/* Documents */}
            <Card sx={{ mb: 4 }}>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <DocumentIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Documents</Typography>
                </Box>
                <Divider sx={{ mb: 2 }} />
                
                {caseData.documents && caseData.documents.length > 0 ? (
                  <List dense>
                    {caseData.documents.map((doc, index) => (
                      <ListItem key={index}>
                        <ListItemText 
                          primary={doc}
                          primaryTypographyProps={{ variant: 'body2' }}
                        />
                      </ListItem>
                    ))}
                  </List>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No documents uploaded yet
                  </Typography>
                )}
                
                <Button
                  variant="outlined"
                  fullWidth
                  sx={{ mt: 2 }}
                  onClick={() => navigate(`/cases/${caseId}/documents`)}
                >
                  Manage Documents
                </Button>
              </CardContent>
            </Card>

            {/* Actions */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Case Actions
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <Box display="flex" flexDirection="column" gap={2}>
                  <Button variant="contained" fullWidth>
                    Run Analysis
                  </Button>
                  <Button variant="outlined" fullWidth>
                    Generate Report
                  </Button>
                  <Button variant="outlined" fullWidth>
                    Update Status
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default CaseDetail;