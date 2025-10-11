import React, { useState } from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import SharedLayout from './SharedLayout';
import { commonStyles } from '../../theme/styleUtils';

const SharedLayoutExample: React.FC = () => {
  const [searchValue, setSearchValue] = useState('');

  const handleSearchChange = (value: string) => {
    setSearchValue(value);
  };

  const handleBackClick = () => {
    console.log('Back button clicked');
  };

  return (
    <SharedLayout
      title="Example Page"
      subtitle="This demonstrates the SharedLayout component with consistent navigation and styling"
      showSearchBar={true}
      searchPlaceholder="Search examples..."
      searchValue={searchValue}
      onSearchChange={handleSearchChange}
      showBackButton={true}
      backButtonLabel="Back to Dashboard"
      onBackClick={handleBackClick}
      breadcrumbs={[
        {
          label: 'Dashboard',
          path: '/',
          icon: undefined
        },
        {
          label: 'Examples',
          path: '/examples'
        },
        {
          label: 'SharedLayout Demo'
        }
      ]}
    >
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {/* Example Cards */}
        <Card sx={commonStyles.card}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Consistent Navigation
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              This page demonstrates the SharedLayout component which provides:
            </Typography>
            <Box component="ul" sx={{ pl: 2, mb: 2 }}>
              <Typography component="li" variant="body2">
                Consistent breadcrumb navigation
              </Typography>
              <Typography component="li" variant="body2">
                Optional search bar functionality
              </Typography>
              <Typography component="li" variant="body2">
                Back button with customizable label
              </Typography>
              <Typography component="li" variant="body2">
                Standardized page titles and subtitles
              </Typography>
            </Box>
          </CardContent>
        </Card>

        <Card sx={commonStyles.interactiveCard}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Central Style Management
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              The StyleProvider component ensures consistent styling across all components:
            </Typography>
            <Box component="ul" sx={{ pl: 2, mb: 2 }}>
              <Typography component="li" variant="body2">
                Centralized design tokens for colors, spacing, and typography
              </Typography>
              <Typography component="li" variant="body2">
                Consistent theme application via ThemeProvider
              </Typography>
              <Typography component="li" variant="body2">
                Global styles for scrollbars, focus states, and accessibility
              </Typography>
              <Typography component="li" variant="body2">
                Reusable style utilities and mixins
              </Typography>
            </Box>
          </CardContent>
        </Card>

        <Box sx={commonStyles.twoColumnLayout}>
          <Box sx={commonStyles.sidebar}>
            <Card sx={commonStyles.card}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Search Results
                </Typography>
                {searchValue ? (
                  <Typography variant="body2">
                    Searching for: "{searchValue}"
                  </Typography>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    Type in the search bar to see results
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Box>

          <Box sx={commonStyles.mainContent}>
            <Card sx={commonStyles.card}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Main Content Area
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  This demonstrates the two-column layout utility from the style system.
                  The sidebar is fixed width while the main content area is flexible.
                </Typography>
                <Button variant="contained" sx={{ mt: 2 }}>
                  Example Action
                </Button>
              </CardContent>
            </Card>
          </Box>
        </Box>
      </Box>
    </SharedLayout>
  );
};

export default SharedLayoutExample;