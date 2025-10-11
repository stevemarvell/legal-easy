import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import { APP_NAME, COLORS } from '../../constants/branding';

const Footer: React.FC = () => {
  return (
    <Box 
      component="footer" 
      sx={{ 
        backgroundColor: COLORS.BACKGROUND, 
        borderTop: `1px solid ${COLORS.BORDER}`,
        py: 2,
        mt: 'auto'
      }}
    >
      <Container maxWidth="xl">
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body2" color="text.secondary">
            © 2024 {APP_NAME}. All rights reserved.
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Intelligent Legal Case Analysis Platform
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;