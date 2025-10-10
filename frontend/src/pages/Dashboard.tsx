import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Chip,
    CircularProgress,
    Alert,
    Container,
    Paper,
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
import { Button } from '@mui/material';

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
            navigate(`/research?q=${encodeURIComponent(searchQuery.trim())}`);
        }
    };

    const handleCaseClick = (caseId: string) => {
        navigate(`/cases/${caseId}`);
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
        );
    }

    return (
        <Container maxWidth="xl">
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
                <Box display="flex" gap={2} mb={4} sx={{ flexWrap: 'wrap' }}>
                    <Card sx={{ flex: 1, minWidth: 200 }}>
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

                    <Card sx={{ flex: 1, minWidth: 200 }}>
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

                    <Card sx={{ flex: 1, minWidth: 200 }}>
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

                    <Card sx={{ flex: 1, minWidth: 200 }}>
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

                    <Card sx={{ flex: 1, minWidth: 200 }}>
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
                </Box>

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
                                    variant="contained"
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

                {/* Legal Playbooks */}
                <Card sx={{ mb: 4 }}>
                    <CardContent>
                        <Typography variant="h5" component="h2" gutterBottom>
                            Legal Playbooks
                        </Typography>
                        <Typography variant="body1" color="text.secondary" paragraph>
                            AI-powered legal decision frameworks and rule sets for different case types
                        </Typography>
                        <Box display="flex" justifyContent="space-between" alignItems="center">
                            <Typography variant="body2" color="text.secondary">
                                Access comprehensive playbooks that guide case assessment, provide decision frameworks,
                                and offer strategic recommendations for various legal matters.
                            </Typography>
                            <Button
                                variant="contained"
                                onClick={() => navigate('/playbooks')}
                                sx={{ ml: 2, minWidth: 'fit-content' }}
                            >
                                View Playbooks
                            </Button>
                        </Box>
                    </CardContent>
                </Card>

                {/* Documentation */}
                <Card sx={{ mb: 4 }}>
                    <CardContent>
                        <Typography variant="h5" component="h2" gutterBottom>
                            Documentation
                        </Typography>
                        <Typography variant="body1" color="text.secondary" paragraph>
                            Comprehensive guides for different audiences - from executive overviews to technical implementation
                        </Typography>
                        <Box display="flex" justifyContent="space-between" alignItems="center">
                            <Typography variant="body2" color="text.secondary">
                                Access platform documentation, AI technology guides, demo data explanations, and technical references.
                            </Typography>
                            <Button
                                variant="contained"
                                onClick={() => navigate('/docs')}
                                sx={{ ml: 2, minWidth: 'fit-content' }}
                            >
                                View Documentation
                            </Button>
                        </Box>
                    </CardContent>
                </Card>
            </Box>
        </Container>
    );
};

export default Dashboard;