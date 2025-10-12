import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Person as PersonIcon,
  Gavel as GavelIcon,
  Description as DocumentIcon,
  MenuBook as PlaybookIcon,
  Schedule as ScheduleIcon,
  Group as GroupIcon
} from '@mui/icons-material';
import { casesService } from '../../services/casesService';
import { Case } from '../../types/api';
import SharedLayout from '../layout/SharedLayout';

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
        const cases = await casesService.getAllCases();
        setCases(cases);
        setFilteredCases(cases);
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
        case_.case_type.toLowerCase().includes(searchQuery.toLowerCase()) ||
        case_.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
        case_.key_parties.some(party => party.toLowerCase().includes(searchQuery.toLowerCase()))
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

  const getPlaybookName = (playbookId: string) => {
    const playbookNames: Record<string, string> = {
      'employment-dispute': 'Employment Law',
      'contract-breach': 'Contract Breach',
      'debt-claim': 'Debt Collection',
      'personal-injury': 'Personal Injury',
      'intellectual-property': 'IP Protection'
    };
    return playbookNames[playbookId] || 'General';
  };

  const handleViewDetails = (caseId: string) => {
    navigate(`/cases/${caseId}`);
  };

  const handleViewDocuments = (caseId: string, event?: React.MouseEvent) => {
    if (event) {
      event.stopPropagation(); // Prevent card click when button is clicked
    }
    navigate(`/cases/${caseId}/documents`);
  };

  const handleCardClick = (caseId: string, event: React.MouseEvent) => {
    // Prevent navigation if clicking on buttons or other interactive elements
    const target = event.target as HTMLElement;
    if (target.closest('button') || target.closest('.MuiCardActions-root')) {
      return;
    }
    
    console.log('Navigating to case:', caseId);
    navigate(`/cases/${caseId}`);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const handleSearchChange = (value: string) => {
    setSearchQuery(value);
  };

  if (loading) {
    return (
      <SharedLayout
        title="Cases"
        subtitle="Manage and track all legal cases"
        showSearchBar={true}
        searchPlaceholder="Search cases by title, client, case type, or parties..."
        searchValue={searchQuery}
        onSearchChange={handleSearchChange}
      >
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress data-testid="loading-spinner" />
        </Box>
      </SharedLayout>
    );
  }

  return (
    <SharedLayout
      title="Cases"
      subtitle="Manage and track all legal cases"
      showSearchBar={true}
      searchPlaceholder="Search cases by title, client, case type, or parties..."
      searchValue={searchQuery}
      onSearchChange={handleSearchChange}
    >
      {/* Error State */}
      {error && (
        <Alert severity="error" sx={{ mb: 4 }} data-testid="error-message">
          {error}
        </Alert>
      )}

      {/* Cases Grid */}
      {filteredCases.length === 0 && !loading ? (
        <Alert severity="info">
          {searchQuery ? 'No cases found matching your search.' : 'No cases found.'}
        </Alert>
      ) : (
        <Box 
          display="grid" 
          gridTemplateColumns={{ xs: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' }} 
          gap={3}
          data-testid="cases-grid"
        >
          {filteredCases.map((case_) => (
            <Box key={case_.id}>
              <Card 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  flexDirection: 'column',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease-in-out',
                  border: '1px solid transparent',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: (theme) => theme.shadows[8],
                    borderColor: (theme) => theme.palette.primary.main,
                  }
                }}
                onClick={(event) => handleCardClick(case_.id, event)}
                title={`Click to view details for ${case_.title}`}
                data-testid="case-card"
                role="button"
                tabIndex={0}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                    <Typography 
                      variant="h6" 
                      component="h3" 
                      gutterBottom
                      sx={{ 
                        color: 'primary.main',
                        '&:hover': {
                          textDecoration: 'underline'
                        }
                      }}
                      data-testid="case-title"
                    >
                      {case_.title}
                    </Typography>
                    <Chip
                      label={case_.status}
                      color={getStatusColor(case_.status) as any}
                      size="small"
                      data-testid="case-status"
                      data-status={case_.status}
                    />
                  </Box>

                  {/* Enhanced Metadata Display */}
                  <Box display="flex" alignItems="center" mb={1}>
                    <PersonIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="body2" color="text.secondary" data-testid="case-client">
                      {case_.client_name}
                    </Typography>
                  </Box>

                  <Box display="flex" alignItems="center" mb={1}>
                    <GavelIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="body2" color="text.secondary" data-testid="case-type">
                      {case_.case_type}
                    </Typography>
                  </Box>

                  <Box display="flex" alignItems="center" mb={1}>
                    <ScheduleIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="body2" color="text.secondary" data-testid="case-created-date">
                      Created: {formatDate(case_.created_date)}
                    </Typography>
                  </Box>

                  {/* Key Parties */}
                  {case_.key_parties && case_.key_parties.length > 0 && (
                    <Box display="flex" alignItems="flex-start" mb={1}>
                      <GroupIcon color="primary" sx={{ mr: 1, fontSize: 20, mt: 0.2 }} />
                      <Typography variant="body2" color="text.secondary" data-testid="case-parties">
                        Parties: {case_.key_parties.slice(0, 2).join(', ')}
                        {case_.key_parties.length > 2 && ` (+${case_.key_parties.length - 2} more)`}
                      </Typography>
                    </Box>
                  )}

                  {/* Document Count */}
                  <Box display="flex" alignItems="center" mb={1}>
                    <DocumentIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="body2" color="text.secondary" data-testid="case-document-count">
                      {case_.documents?.length || 0} document{(case_.documents?.length || 0) !== 1 ? 's' : ''}
                    </Typography>
                  </Box>

                  {/* Playbook Assignment Indicator */}
                  <Box display="flex" alignItems="center" mb={2}>
                    <PlaybookIcon color="primary" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="body2" color="text.secondary" data-testid="case-playbook">
                      Playbook: {getPlaybookName(case_.playbook_id)}
                    </Typography>
                  </Box>

                  <Typography variant="body2" color="text.secondary" paragraph data-testid="case-summary">
                    {case_.summary.length > 120
                      ? `${case_.summary.substring(0, 120)}...`
                      : case_.summary
                    }
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>
      )}
    </SharedLayout>
  );
};

export default CaseList;