import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Grid,
  Chip,
  TextField,
  InputAdornment,
  Alert,
  CircularProgress,
  Container
} from '@mui/material';
import {
  Search as SearchIcon,
  Person as PersonIcon,
  Gavel as GavelIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { apiClient } from '../../services/api';
import { Case } from '../../types/api';

const CaseList: React.FC = () => {
  const navigate = useNavigate();
  const [cases, setCases] = useState<Case[]>([]);
  const [filteredCases, setFilteredCases] = useState<Case[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCases = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiClient.get<Case[]>('/api/cases');
        setCases(response.data);
        setFilteredCases(response.data);
      } catch (err) {
        console.error('Failed to fetch cases:', err);
        setError('Failed to load cases. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchCases();
  }, []);

  useEffect(() => {
    if (!searchQuery.trim()) {
      setFilteredCases(cases);
    } else {
      const filtered = cases.filter(case_ =>
        case_.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        case_.client_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        case_.case_type.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredCases(filtered);
    }
  }, [searchQuery, cases]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active': return 'success';
      case 'Under Review': return 'warning';
      case 'Resolved': return 'info';
      default: return 'default';
    }
  };

  const handleViewDetails = (caseId: string) => {
    navigate(`/cases/${caseId}`);
  };

  const handleViewDocuments = (caseId: string) => {
    navigate(`/cases/${caseId}/documents`);
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

  return (
    <Container maxWidth="xl">
      <Box>
        {/* Header */}
        <Box mb={4}>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={3}>
            <Box>
              <Typography variant="h3" component="h1" color="primary" gutterBottom>
                Cases
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Manage and track all legal cases
              </Typography>
            </Box>
          </Box>

          {/* Search */}
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search cases by title, client, or case type..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon color="primary" />
                </InputAdornment>
              ),
            }}
            sx={{ mb: 3 }}
          />
        </Box>

        {/* Error State */}
        {error && (
          <Alert severity="error" sx={{ mb: 4 }}>
            {error}
          </Alert>
        )}

        {/* Cases Grid */}
        {filteredCases.length === 0 && !loading ? (
          <Alert severity="info">
            {searchQuery ? 'No cases found matching your search.' : 'No cases found.'}
          </Alert>
        ) : (
          <Grid container spacing={3}>
            {filteredCases.map((case_) => (
              <Grid item xs={12} md={6} lg={4} key={case_.id}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                      <Typography variant="h6" component="h3" gutterBottom>
                        {case_.title}
                      </Typography>
                      <Chip
                        label={case_.status}
                        color={getStatusColor(case_.status) as any}
                        size="small"
                      />
                    </Box>

                    <Box display="flex" alignItems="center" mb={1}>
                      <PersonIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
                      <Typography variant="body2" color="text.secondary">
                        {case_.client_name}
                      </Typography>
                    </Box>

                    <Box display="flex" alignItems="center" mb={2}>
                      <GavelIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
                      <Typography variant="body2" color="text.secondary">
                        {case_.case_type}
                      </Typography>
                    </Box>

                    <Typography variant="body2" color="text.secondary" paragraph>
                      {case_.summary.length > 150
                        ? `${case_.summary.substring(0, 150)}...`
                        : case_.summary
                      }
                    </Typography>

                    <Typography variant="caption" color="text.secondary">
                      Created: {new Date(case_.created_date).toLocaleDateString()}
                    </Typography>
                  </CardContent>

                  <CardActions>
                    <Button
                      size="small"
                      variant="contained"
                      onClick={() => handleViewDetails(case_.id)}
                    >
                      View Details
                    </Button>
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => handleViewDocuments(case_.id)}
                    >
                      Documents
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Container>
  );
};

export default CaseList;