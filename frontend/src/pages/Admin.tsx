import React, { useState } from 'react';
import {
  Container,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Box,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Storage as StorageIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';

interface RegenerationResult {
  success: boolean;
  message: string;
  total_documents: number;
  research_areas: string[];
  legal_concepts_count: number;
  last_updated: string;
}

const Admin: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RegenerationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRegenerateIndex = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await apiClient.post<RegenerationResult>('/api/corpus/regenerate-index');
      setResult(response.data);
    } catch (err: any) {
      console.error('Failed to regenerate corpus index:', err);
      setError(err.response?.data?.detail || 'Failed to regenerate corpus index');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Typography variant="h4" component="h1" color="primary" gutterBottom>
          System Administration
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Administrative functions for managing the legal AI system
        </Typography>

        {/* Corpus Index Management */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <StorageIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Research Corpus Index
              </Typography>
            </Box>
            
            <Typography variant="body1" color="text.secondary" paragraph>
              The corpus index organizes all legal documents, templates, and precedents for search and analysis. 
              Regenerate the index after adding new legal documents or updating existing ones.
            </Typography>

            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                What the corpus index includes:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Document Metadata" 
                    secondary="Titles, descriptions, categories, and research areas"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Legal Concept Mapping" 
                    secondary="Links documents to relevant legal concepts for intelligent search"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Document Relationships" 
                    secondary="Connections between related legal materials and precedents"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <InfoIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Search Optimization" 
                    secondary="Enables concept-based search and document discovery"
                  />
                </ListItem>
              </List>
            </Box>

            <Divider sx={{ my: 3 }} />

            {/* Action Button */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Button
                variant="contained"
                color="primary"
                size="large"
                startIcon={loading ? <CircularProgress size={20} /> : <RefreshIcon />}
                onClick={handleRegenerateIndex}
                disabled={loading}
              >
                {loading ? 'Regenerating Index...' : 'Regenerate Corpus Index'}
              </Button>
              
              {loading && (
                <Typography variant="body2" color="text.secondary">
                  This may take a few moments...
                </Typography>
              )}
            </Box>

            {/* Error Display */}
            {error && (
              <Alert severity="error" sx={{ mb: 3 }} icon={<ErrorIcon />}>
                <Typography variant="body2">
                  <strong>Error:</strong> {error}
                </Typography>
              </Alert>
            )}

            {/* Success Result */}
            {result && result.success && (
              <Alert severity="success" sx={{ mb: 3 }} icon={<CheckIcon />}>
                <Typography variant="body2" gutterBottom>
                  <strong>Success:</strong> {result.message}
                </Typography>
                
                <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  <Chip 
                    label={`${result.total_documents} Documents`} 
                    color="success" 
                    size="small" 
                  />
                  <Chip 
                    label={`${result.legal_concepts_count} Legal Concepts`} 
                    color="success" 
                    size="small" 
                  />
                  <Chip 
                    label={`${result.research_areas.length} Research Areas`} 
                    color="success" 
                    size="small" 
                  />
                </Box>

                {result.research_areas.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="caption" color="text.secondary" display="block">
                      Research Areas:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                      {result.research_areas.map((area) => (
                        <Chip
                          key={area}
                          label={area}
                          size="small"
                          variant="outlined"
                          color="secondary"
                        />
                      ))}
                    </Box>
                  </Box>
                )}

                <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
                  Last updated: {new Date(result.last_updated).toLocaleString()}
                </Typography>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Future Admin Functions */}
        <Card>
          <CardContent>
            <Typography variant="h5" component="h2" gutterBottom>
              Additional Admin Functions
            </Typography>
            <Typography variant="body2" color="text.secondary">
              More administrative functions will be available here in future updates, including:
            </Typography>
            <List dense sx={{ mt: 1 }}>
              <ListItem>
                <ListItemText 
                  primary="• Document Analysis Management" 
                  secondary="Bulk reprocess AI analysis for case documents"
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="• System Health Monitoring" 
                  secondary="View system status and performance metrics"
                />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="• Data Export/Import" 
                  secondary="Backup and restore system data"
                />
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Admin;