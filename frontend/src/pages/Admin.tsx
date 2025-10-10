import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Container,
  Grid
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Settings as AdminIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';

const Admin = () => {
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const handleAction = async (action: string) => {
    try {
      setActionLoading(action);
      setError(null);

      let response;
      if (action === 'initialize-corpus') {
        response = await apiClient.post('/api/admin/actions/initialize-corpus');
      } else if (action === 'reindex-all') {
        response = await apiClient.post('/api/admin/actions/reindex-all');
      } else if (action === 'clear-index') {
        response = await apiClient.post('/api/admin/actions/clear-index');
      } else if (action === 'test-search') {
        response = await apiClient.post('/api/admin/actions/test-rag-search?query=employment contract');
      } else if (action === 'index-case-documents') {
        response = await apiClient.post('/api/admin/actions/index-case-documents');
      }

      if (response?.data.success) {
        // Show success message briefly
        setError(`✅ ${response.data.message}`);
        setTimeout(() => setError(null), 3000);
      }
    } catch (err: any) {
      console.error(`Action ${action} failed:`, err);
      setError(`❌ Action failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box>
        {/* Header */}
        <Box mb={4}>
          <Box display="flex" alignItems="center" gap={2} mb={2}>
            <AdminIcon color="primary" />
            <Typography variant="h4" component="h1" color="primary">
              Admin
            </Typography>
          </Box>
          <Typography variant="body1" color="text.secondary">
            Index documents for search functionality
          </Typography>
        </Box>

        {/* Error/Success Alert */}
        {error && (
          <Alert 
            severity={error.startsWith('✅') ? 'success' : 'error'} 
            sx={{ mb: 3 }}
          >
            {error}
          </Alert>
        )}

        {/* Indexing Actions */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🔍 Build Search Index
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Index legal documents for research functionality.
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<PlayIcon />}
                  onClick={() => handleAction('initialize-corpus')}
                  disabled={!!actionLoading}
                  fullWidth
                >
                  {actionLoading === 'initialize-corpus' ? (
                    <>
                      <CircularProgress size={16} sx={{ mr: 1 }} />
                      Indexing...
                    </>
                  ) : (
                    'Build Index'
                  )}
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📁 Index Case Documents
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Index case documents for search.
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<PlayIcon />}
                  onClick={() => handleAction('index-case-documents')}
                  disabled={!!actionLoading}
                  fullWidth
                >
                  {actionLoading === 'index-case-documents' ? (
                    <>
                      <CircularProgress size={16} sx={{ mr: 1 }} />
                      Indexing...
                    </>
                  ) : (
                    'Index Cases'
                  )}
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🔄 Reindex All
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Rebuild complete search index.
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<PlayIcon />}
                  onClick={() => handleAction('reindex-all')}
                  disabled={!!actionLoading}
                  fullWidth
                >
                  {actionLoading === 'reindex-all' ? (
                    <>
                      <CircularProgress size={16} sx={{ mr: 1 }} />
                      Reindexing...
                    </>
                  ) : (
                    'Reindex All'
                  )}
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🧪 Test Search
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Test search functionality.
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<PlayIcon />}
                  onClick={() => handleAction('test-search')}
                  disabled={!!actionLoading}
                  fullWidth
                >
                  {actionLoading === 'test-search' ? (
                    <>
                      <CircularProgress size={16} sx={{ mr: 1 }} />
                      Testing...
                    </>
                  ) : (
                    'Test Search'
                  )}
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom color="error">
                  🗑️ Clear Index
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Clear all search indexes. Use before rebuilding.
                </Typography>
                <Button
                  variant="outlined"
                  color="error"
                  startIcon={<PlayIcon />}
                  onClick={() => handleAction('clear-index')}
                  disabled={!!actionLoading}
                >
                  {actionLoading === 'clear-index' ? (
                    <>
                      <CircularProgress size={16} sx={{ mr: 1 }} />
                      Clearing...
                    </>
                  ) : (
                    'Clear Index'
                  )}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Admin;