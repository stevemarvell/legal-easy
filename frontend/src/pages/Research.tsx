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
  Paper,
  Link,
  Container
} from '@mui/material';
import {
  Search as SearchIcon,
  Description as DescriptionIcon,
  Analytics as AnalyticsIcon,
  Gavel as GavelIcon,
  Settings as ProcessingIcon,
  Category as CategoryIcon,
  Link as LinkIcon,
  GetApp as ExtractIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';
import { apiClient } from '../services/api';
import { LegalSearchResult } from '../types/api';
import { Button } from '@mui/material';

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
    <Container maxWidth="xl">
      <Box>
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h3" component="h1" color="primary" gutterBottom>
          Legal Research
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Search and analyze legal documents, precedents, and case law
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
                placeholder="Search legal documents, cases, or ask a question..."
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

      {/* Search Results */}
      {searchResults.length > 0 && (
        <Box mb={4}>
          <Typography variant="h5" component="h2" gutterBottom>
            Search Results
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

      {/* Loading State */}
      {loading && (
        <Box display="flex" flexDirection="column" alignItems="center" py={4}>
          <CircularProgress />
          <Typography variant="body1" sx={{ mt: 2 }}>
            Searching legal database...
          </Typography>
        </Box>
      )}

      {/* Empty State */}
      {!loading && !error && searchResults.length === 0 && searchQuery && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="body1" color="text.secondary" textAlign="center">
              No results found for "{searchQuery}". Try different search terms.
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Research Tools */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <DescriptionIcon color="primary" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" component="h3" gutterBottom>
                Document Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Analyze legal documents and extract key information
              </Typography>
              <Button variant="outlined">View Documents</Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <GavelIcon color="primary" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" component="h3" gutterBottom>
                Case Law Search
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Search through precedents and case law with semantic matching
              </Typography>
              <Button variant="outlined">Search Cases</Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <AnalyticsIcon color="primary" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" component="h3" gutterBottom>
                Legal Analytics
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Generate insights and reports from legal case data
              </Typography>
              <Button variant="outlined">View Analytics</Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Research Features */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" component="h2" gutterBottom textAlign="center">
            Legal Research Features
          </Typography>
          <Grid container spacing={3}>
            {[
              { icon: ProcessingIcon, title: 'Document Processing', desc: 'Process and analyze legal documents in various formats' },
              { icon: AnalyticsIcon, title: 'Text Analysis', desc: 'Extract and structure information from legal texts' },
              { icon: CategoryIcon, title: 'Classification', desc: 'Categorize documents by legal domain and content type' },
              { icon: LinkIcon, title: 'Relationship Mapping', desc: 'Identify connections between cases, precedents, and statutes' },
              { icon: ExtractIcon, title: 'Information Extraction', desc: 'Extract key facts, dates, parties, and legal concepts' },
              { icon: CheckIcon, title: 'Relevance Scoring', desc: 'Rank search results by relevance and legal significance' }
            ].map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Box textAlign="center" p={2}>
                  <feature.icon color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="h6" component="h4" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.desc}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Recent Research */}
      <Card>
        <CardContent>
          <Typography variant="h5" component="h3" gutterBottom>
            Recent Research
          </Typography>
          <Grid container spacing={2}>
            {[
              { title: 'Employment Law Precedents Analysis', desc: 'Analysis of recent employment law cases and their implications', time: '2 hours ago' },
              { title: 'Contract Clause Extraction', desc: 'Extracted key clauses from 15 service agreements', time: '1 day ago' },
              { title: 'Regulatory Compliance Review', desc: 'Comprehensive review of new data protection regulations', time: '3 days ago' }
            ].map((item, index) => (
              <Grid item xs={12} key={index}>
                <Paper sx={{ p: 2, borderLeft: 4, borderColor: 'primary.main' }}>
                  <Typography variant="h6" component="h4" gutterBottom>
                    {item.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {item.desc}
                  </Typography>
                  <Chip label={item.time} size="small" color="primary" variant="outlined" />
                </Paper>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>
      </Box>
    </Container>
  );
};

export default Research;