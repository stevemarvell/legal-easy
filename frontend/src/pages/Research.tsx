import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Link,
  Container,
  Button
} from '@mui/material';
import {
  Search as SearchIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';
import { LegalSearchResult } from '../types/api';

const Research = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<LegalSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const queryParam = searchParams.get('q');
    if (queryParam) {
      setSearchQuery(queryParam);
      performSearch(queryParam);
    }
  }, [searchParams]);

  const performSearch = async (query?: string) => {
    const searchTerm = query || searchQuery;
    if (!searchTerm.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.post<{ results: LegalSearchResult[] }>('/api/legal-research/search', {
        query: searchTerm.trim()
      });
      setSearchResults(response.data.results || []);
    } catch (err) {
      console.error('Search failed:', err);
      setError('Failed to perform search. Please try again.');
      setSearchResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setSearchParams({ q: searchQuery.trim() });
      performSearch();
    }
  };

  return (
    <Container maxWidth="lg">
      <Box>
        {/* Header */}
        <Box mb={4}>
          <Typography variant="h4" component="h1" color="primary" gutterBottom>
            Legal Research
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Search legal documents and case law
          </Typography>
        </Box>

        {/* Search Section */}
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box component="form" onSubmit={handleSearchSubmit}>
              <Box display="flex" gap={2}>
                <TextField
                  fullWidth
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search legal documents..."
                  variant="outlined"
                />
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading || !searchQuery.trim()}
                  startIcon={<SearchIcon />}
                >
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </Box>
            </Box>
          </CardContent>
        </Card>

        {/* Loading State */}
        {loading && (
          <Box display="flex" flexDirection="column" alignItems="center" py={4}>
            <CircularProgress />
            <Typography variant="body1" sx={{ mt: 2 }}>
              Searching...
            </Typography>
          </Box>
        )}

        {/* Error State */}
        {error && (
          <Alert
            severity="error"
            sx={{ mb: 4 }}
            action={
              <Button onClick={() => performSearch()}>
                Try Again
              </Button>
            }
          >
            {error}
          </Alert>
        )}

        {/* Search Results */}
        {searchResults.length > 0 && (
          <Box mb={4}>
            <Typography variant="h5" component="h2" gutterBottom>
              Search Results ({searchResults.length})
            </Typography>
            <Grid container spacing={3}>
              {searchResults.map((result) => (
                <Grid item xs={12} key={result.id}>
                  <Card>
                    <CardContent>
                      <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                        <Typography variant="h6" component="h3" sx={{ flexGrow: 1, mr: 2 }}>
                          {result.title}
                        </Typography>
                        <Box display="flex" gap={1}>
                          <Chip
                            label={result.document_type}
                            color="primary"
                            size="small"
                          />
                          <Chip
                            label={`${Math.round(result.relevance_score * 100)}% match`}
                            color="success"
                            size="small"
                          />
                        </Box>
                      </Box>

                      <Typography variant="body1" paragraph>
                        {result.content}
                      </Typography>

                      <Box display="flex" gap={2} mb={2} flexWrap="wrap">
                        <Typography variant="caption" color="text.secondary">
                          Source: {result.source}
                        </Typography>
                        {result.jurisdiction && (
                          <Typography variant="caption" color="text.secondary">
                            Jurisdiction: {result.jurisdiction}
                          </Typography>
                        )}
                        {result.date && (
                          <Typography variant="caption" color="text.secondary">
                            Date: {new Date(result.date).toLocaleDateString()}
                          </Typography>
                        )}
                      </Box>

                      {result.url && (
                        <Link
                          href={result.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          color="primary"
                        >
                          View Full Document
                        </Link>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {/* Empty State */}
        {!loading && !error && searchResults.length === 0 && searchQuery && (
          <Card>
            <CardContent>
              <Typography variant="body1" color="text.secondary" textAlign="center">
                No results found for "{searchQuery}". Try different search terms.
              </Typography>
            </CardContent>
          </Card>
        )}

        {/* Welcome State */}
        {!loading && !error && searchResults.length === 0 && !searchQuery && (
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 6 }}>
              <SearchIcon color="primary" sx={{ fontSize: 64, mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Search Legal Documents
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Enter a search term above to find relevant legal documents and case law.
              </Typography>
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  );
};

export default Research;