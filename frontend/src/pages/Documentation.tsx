import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CardActionArea,
  Breadcrumbs,
  Link,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  Paper
} from '@mui/material';
import {
  Home as HomeIcon,
  MenuBook as DocsIcon,
  Business as BusinessIcon,
  Code as TechnicalIcon,
  Gavel as LegalIcon,
  Storage as DataIcon,
  ArrowForward as ArrowIcon,
  ArrowBack as BackIcon
} from '@mui/icons-material';

interface DocSection {
  id: string;
  title: string;
  description: string;
  audience: string;
  icon: React.ReactNode;
  color: string;
  features: string[];
  path: string;
}

interface DocContent {
  title: string;
  content: string;
}

const Documentation: React.FC = () => {
  const navigate = useNavigate();
  const { section } = useParams<{ section?: string }>();
  const selectedSection = section || null;

  const docSections: DocSection[] = [
    {
      id: 'overview',
      title: 'Demo Overview',
      description: 'What actually works in this legal platform demo.',
      audience: 'All users',
      icon: <LegalIcon sx={{ fontSize: 40 }} />,
      color: '#744EFD',
      features: [
        'Legal playbooks with rule engine',
        'Case management (demo data)',
        'Document viewer (demo data)',
        'Basic legal research'
      ],
      path: '/docs/overview'
    },
    {
      id: 'technical',
      title: 'Technical Details',
      description: 'How the demo is built and what technologies are used.',
      audience: 'Developers',
      icon: <TechnicalIcon sx={{ fontSize: 40 }} />,
      color: '#4CAF50',
      features: [
        'React + TypeScript frontend',
        'FastAPI + Python backend',
        'Static JSON data files',
        'Basic REST API endpoints'
      ],
      path: '/docs/technical'
    },
    {
      id: 'data',
      title: 'Demo Data',
      description: 'Sample data used in the demonstration.',
      audience: 'All users',
      icon: <DataIcon sx={{ fontSize: 40 }} />,
      color: '#FF9800',
      features: [
        '6 sample legal cases',
        'Mock document analysis',
        'Legal playbook rules',
        'Demo legal corpus for search'
      ],
      path: '/docs/data'
    }
  ];

  const getDocumentationContent = (sectionId: string): DocContent => {
    switch (sectionId) {
      case 'overview':
        return {
          title: 'Demo Overview',
          content: `
# Legal Platform Demo

## What Works
- Legal playbooks with rule engine
- Case management (demo data only)
- Document viewer (demo data only)  
- Basic search (demo data only)

## What Doesn't Work
- Document upload
- Real AI analysis
- User authentication
- External integrations

This is a UI demo with static JSON data.
          `
        };
      case 'technical':
        return {
          title: 'Technical Details',
          content: `
# Tech Stack

- Frontend: React + TypeScript + Material-UI
- Backend: FastAPI + Python  
- Data: Static JSON files (no database)

# Running

\`\`\`bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload
\`\`\`
          `
        };
      case 'data':
        return {
          title: 'Demo Data',
          content: `
# Demo Data

## Cases
6 sample cases: Employment disputes, contract breaches, debt claims

## Documents  
Mock analysis with fake extracted dates, parties, clauses

## Playbooks
3 rule sets: Employment, Contract, Debt

## Search Corpus
Sample UK legal content for search demo

All data is fake for demonstration purposes.
          `
        };
      default:
        return {
          title: 'Documentation',
          content: 'Select a section to view documentation.'
        };
    }
  };

  const handleSectionSelect = (sectionId: string) => {
    navigate(`/docs/${sectionId}`);
  };



  const handleBreadcrumbNavigation = (path: string) => {
    navigate(path);
  };

  const handleBackNavigation = () => {
    if (selectedSection) {
      // If viewing a section, go back to documentation main page
      navigate('/docs');
    } else {
      // If on main documentation page, go back to previous page in history
      try {
        navigate(-1);
      } catch (error) {
        // Fallback to dashboard if navigation fails
        navigate('/');
      }
    }
  };

  if (selectedSection) {
    const content = getDocumentationContent(selectedSection);
    return (
      <Container maxWidth="xl">
        <Box>
          {/* Header with Navigation */}
          <Box mb={4}>
            <Button
              variant="outlined"
              startIcon={<BackIcon />}
              onClick={handleBackNavigation}
              sx={{ mb: 2 }}
            >
              Back
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
                onClick={() => navigate('/docs')}
                sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
              >
                <DocsIcon sx={{ mr: 0.5 }} fontSize="inherit" />
                Documentation
              </Link>
              <Typography color="text.primary" variant="body2">
                {content.title}
              </Typography>
            </Breadcrumbs>

            <Typography variant="h3" component="h1" color="primary">
              {content.title}
            </Typography>
          </Box>

          {/* Content */}
          <Paper sx={{ p: 4 }}>
            <Typography component="div" sx={{ whiteSpace: 'pre-line' }}>
              {content.content}
            </Typography>
          </Paper>
        </Box>
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
            startIcon={<BackIcon />}
            onClick={handleBackNavigation}
            sx={{ mb: 2 }}
          >
            Back
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
            <Typography color="text.primary" variant="body2">
              Documentation
            </Typography>
          </Breadcrumbs>

          <Typography variant="h3" component="h1" color="primary" gutterBottom>
            Demo Documentation
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Honest documentation about what actually works in this legal platform demo
          </Typography>
        </Box>

        {/* Documentation Sections */}
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {docSections.map((section) => (
            <Card key={section.id} sx={{ transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-2px)' } }}>
              <CardActionArea onClick={() => handleSectionSelect(section.id)}>
                <CardContent sx={{ p: 3 }}>
                  <Box display="flex" alignItems="flex-start" gap={3}>
                    <Box sx={{ color: section.color }}>
                      {section.icon}
                    </Box>
                    <Box flex={1}>
                      <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
                        <Typography variant="h5" component="h2" color="primary">
                          {section.title}
                        </Typography>
                        <ArrowIcon color="action" />
                      </Box>
                      <Typography variant="body1" color="text.secondary" paragraph>
                        {section.description}
                      </Typography>
                      <Chip
                        label={section.audience}
                        size="small"
                        sx={{ mb: 2, backgroundColor: section.color, color: 'white' }}
                      />
                      <Divider sx={{ my: 2 }} />
                      <List dense>
                        {section.features.map((feature, index) => (
                          <ListItem key={index} sx={{ py: 0.5 }}>
                            <ListItemIcon sx={{ minWidth: 32 }}>
                              <Box
                                sx={{
                                  width: 6,
                                  height: 6,
                                  borderRadius: '50%',
                                  backgroundColor: section.color
                                }}
                              />
                            </ListItemIcon>
                            <ListItemText
                              primary={feature}
                              primaryTypographyProps={{ variant: 'body2' }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  </Box>
                </CardContent>
              </CardActionArea>
            </Card>
          ))}
        </Box>
      </Box>
    </Container>
  );
};

export default Documentation;