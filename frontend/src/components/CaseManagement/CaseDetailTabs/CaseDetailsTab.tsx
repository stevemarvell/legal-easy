import React from 'react';
import ReactMarkdown from 'react-markdown';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Divider
} from '@mui/material';
import {
  Assignment as AssignmentIcon
} from '@mui/icons-material';
import { Case } from '../../../types/api';

interface CaseDetailsTabProps {
  caseData: Case;
}

const CaseDetailsTab: React.FC<CaseDetailsTabProps> = ({ caseData }) => {
  return (
    <Card sx={{ mb: 4 }} data-testid="case-details">
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
         Case Details
        </Typography>
        <Divider sx={{ mb: 3 }} />

        {caseData.description ? (
          <Box
            data-testid="case-full-description"
            sx={{
              '& h2': {
                color: 'primary.main',
                fontSize: '1.5rem',
                fontWeight: 600,
                mt: 3,
                mb: 2,
                '&:first-of-type': { mt: 0 }
              },
              '& h3': {
                color: 'primary.dark',
                fontSize: '1.25rem',
                fontWeight: 500,
                mt: 2.5,
                mb: 1.5
              },
              '& p': {
                lineHeight: 1.8,
                textAlign: 'justify',
                mb: 2,
                fontSize: '1rem'
              },
              '& ul, & ol': {
                mb: 2,
                pl: 3
              },
              '& li': {
                mb: 0.5,
                lineHeight: 1.6
              },
              '& strong': {
                color: 'text.primary',
                fontWeight: 600
              },
              '& em': {
                fontStyle: 'italic',
                color: 'text.secondary'
              }
            }}
          >
            <ReactMarkdown>{caseData.description}</ReactMarkdown>
          </Box>
        ) : (
          <Box textAlign="center" py={4}>
            <AssignmentIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
            <Typography variant="body2" color="text.secondary" gutterBottom>
              No detailed description available for this case
            </Typography>
            <Typography variant="caption" color="text.secondary">
              The case summary is available in the Overview tab
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default CaseDetailsTab;