import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  TextField,
  Chip,
  CircularProgress,
  Alert,
  Container,
  Paper,
  IconButton,
  CardActions
} from '@mui/material';
import {
  Search as SearchIcon,
  TrendingUp as TrendingUpIcon,
  Gavel as GavelIcon,
  Assignment as AssignmentIcon,
  CheckCircle as CheckCircleIcon,
  Visibility as VisibilityIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';
import { Case } from '../types/api';
import Button from './Button';


interface CaseStatistics {
  total_cases: number;
  active_cases: number;
  resolved_cases: number;
  under_review_cases: number;
  recent_activity_count: number;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [statistics, setStatistics] = useState<CaseStatistics | null>(null);
  const [recentCases, setRecentCases] = useState<Case[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch case statistics
        const statsResponse = await apiClient.get<CaseStatistics>('/api/cases/statistics');
        setStatistics(statsResponse.data);

        // Fetch recent cases (all cases for now, we'll show the most recent ones)
        const casesResponse = await apiClient.get<Case[]>('/api/cases');
        const sortedCases = casesResponse.data
          .sort((a, b) => new Date(b.updated_at || b.created_at || b.created_date).getTime() - new Date(a.updated_at || a.created_at || a.created_date).getTime())
          .slice(0, 5); // Show 5 most recent cases
        setRecentCases(sortedCases);
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/legal-research?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleCaseClick = (caseId: string) => {
    navigate(`/cases/${caseId}`);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return '#10b981'; // green
      case 'under review':
        return '#f59e0b'; // amber
      case 'resolved':
        return '#6b7280'; // gray
      case 'pending':
        return '#3b82f6'; // blue
      default:
        return '#6b7280';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
      case 'critical':
        return '#744EFD'; // primary purple
      case 'medium':
        return '#f59e0b'; // amber
      case 'low':
        return '#10b981'; // green
      default:
        return '#6b7280';
    }
  };

  if (loading) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight="400px">
        <CircularProgress data-testid="loading-spinner" />
        <Typography variant="body1" sx={{ mt: 2 }}>Loading dashboard...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Container>
        <Alert
          severity="error"
          action={
            <Button onClick={() => window.location.reload()}>
              Retry
            </Button>
          }
        >
          {error}
        </Alert>
      </Container>
    );
  }

  return (
    <Box>
      {/* Demo Environment Banner */}
      <Paper sx={{ mb: 3, p: 2, backgroundColor: '#161821' }}>
        <Box display="flex" alignItems="center" gap={2}>
          <Chip label="DEMO" color="primary" size="small" />
          <Typography variant="body2" color="text.secondary">
            Shift AI Legal Demo - Explore implemented features with sample legal case data
          </Typography>
        </Box>
      </Paper>

      {/* Header Section */}
      <Box mb={4}>
        <Typography variant="h3" component="h1" color="primary" gutterBottom>
          Shift AI Legal Dashboard
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Intelligent case management and legal research platform
        </Typography>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <AssignmentIcon color="primary" />
                <Box>
                  <Typography variant="h4" component="h3">
                    {statistics?.total_cases || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Cases
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <TrendingUpIcon color="primary" />
                <Box>
                  <Typography variant="h4" component="h3">
                    {statistics?.active_cases || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active Cases
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <VisibilityIcon color="primary" />
                <Box>
                  <Typography variant="h4" component="h3">
                    {statistics?.under_review_cases || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Under Review
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <CheckCircleIcon color="primary" />
                <Box>
                  <Typography variant="h4" component="h3">
                    {statistics?.resolved_cases || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Resolved
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <GavelIcon color="primary" />
                <Box>
                  <Typography variant="h4" component="h3">
                    {statistics?.recent_activity_count || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Recent Activity
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Legal Research Search */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" component="h2" gutterBottom>
            Legal Research
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Search through legal precedents, statutes, and case law with semantic search
          </Typography>
          <Box component="form" onSubmit={handleSearchSubmit} sx={{ mb: 2 }}>
            <Box display="flex" gap={2}>
              <TextField
                fullWidth
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search legal documents, precedents, statutes..."
                variant="outlined"
              />
              <Button
                type="submit"
                variant="primary"
                disabled={!searchQuery.trim()}
                startIcon={<SearchIcon />}
              >
                Search
              </Button>
            </Box>
          </Box>
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Try searching for:
            </Typography>
            <Box display="flex" gap={1} flexWrap="wrap">
              <Chip
                label="employment termination"
                onClick={() => setSearchQuery('employment termination')}
                clickable
                variant="outlined"
              />
              <Chip
                label="contract breach"
                onClick={() => setSearchQuery('contract breach')}
                clickable
                variant="outlined"
              />
              <Chip
                label="intellectual property"
                onClick={() => setSearchQuery('intellectual property')}
                clickable
                variant="outlined"
              />
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Recent Cases */}
      <Box>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h5" component="h2">
            Recent Cases
          </Typography>
          <Button
            variant="outline"
            onClick={() => navigate('/cases')}
          >
            View All Cases
          </Button>
        </Box>

        <Grid container spacing={3}>
          {recentCases.map((case_) => (
            <Grid item xs={12} md={6} lg={4} key={case_.id}>
              <Card
                sx={{
                  cursor: 'pointer',
                  '&:hover': {
                    boxShadow: 3
                  }
                }}
                onClick={() => handleCaseClick(case_.id)}
              >
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                    <Typography variant="h6" component="h3" sx={{ flexGrow: 1, mr: 1 }}>
                      {case_.title}
                    </Typography>
                    <Box display="flex" flexDirection="column" gap={0.5}>
                      <Chip
                        label={case_.status}
                        size="small"
                        color={case_.status.toLowerCase() === 'active' ? 'success' : 'default'}
                      />
                      {case_.priority && (
                        <Chip
                          label={case_.priority}
                          size="small"
                          color={case_.priority.toLowerCase() === 'high' ? 'primary' : 'default'}
                        />
                      )}
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary" paragraph>
                    {case_.description}
                  </Typography>

                  <Box display="flex" justifyContent="space-between" mb={2}>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Type:
                      </Typography>
                      <Typography variant="body2">
                        {case_.case_type}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Updated:
                      </Typography>
                      <Typography variant="body2">
                        {new Date(case_.updated_at || case_.created_at || case_.created_date).toLocaleDateString()}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>

                <CardActions>
                  <Button
                    variant="primary"
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleCaseClick(case_.id);
                    }}
                  >
                    View Details
                  </Button>
                  <Button
                    variant="secondary"
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/cases/${case_.id}/documents`);
                    }}
                  >
                    Documents
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>

        {recentCases.length === 0 && (
          <Card>
            <CardContent>
              <Typography variant="body1" color="text.secondary" textAlign="center">
                No recent cases found.
              </Typography>
            </CardContent>
          </Card>
        )}
      </Box>
    </Box>
  );
};

export default Dashboard;