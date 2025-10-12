import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  Person as PersonIcon,
  Gavel as GavelIcon,
  Schedule as ScheduleIcon,
  Group as GroupIcon,
  MenuBook as PlaybookIcon
} from '@mui/icons-material';
import { Case } from '../../../types/api';

interface CaseOverviewTabProps {
  caseData: Case;
}

const CaseOverviewTab: React.FC<CaseOverviewTabProps> = ({ caseData }) => {
  const getPlaybookName = (playbookId: string) => {
    const playbookNames: Record<string, string> = {
      'employment-dispute': 'Employment Law Playbook',
      'contract-breach': 'Contract Breach Playbook',
      'debt-claim': 'Debt Collection Playbook',
      'personal-injury': 'Personal Injury Playbook',
      'intellectual-property': 'IP Protection Playbook'
    };
    return playbookNames[playbookId] || 'General Playbook';
  };

  return (
    <Box>
      {/* Essential Case Information */}
      <Card sx={{ mb: 4 }} data-testid="case-overview">
        <CardContent>
          <Typography variant="h5" component="h2" gutterBottom>
            Case Overview
          </Typography>
          <Divider sx={{ mb: 3 }} />

          <Box display="flex" flexDirection="column" gap={3}>
            <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={3}>
              <Box flex={1}>
                <Box display="flex" alignItems="center" mb={2}>
                  <PersonIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Client</Typography>
                </Box>
                <Typography variant="body1" color="text.secondary" data-testid="case-client">
                  {caseData.client_name}
                </Typography>
              </Box>

              <Box flex={1}>
                <Box display="flex" alignItems="center" mb={2}>
                  <GavelIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Case Type</Typography>
                </Box>
                <Typography variant="body1" color="text.secondary" data-testid="case-type">
                  {caseData.case_type}
                </Typography>
              </Box>
            </Box>

            <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={3}>
              <Box flex={1}>
                <Box display="flex" alignItems="center" mb={2}>
                  <ScheduleIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Created Date</Typography>
                </Box>
                <Typography variant="body1" color="text.secondary" data-testid="case-created-date">
                  {new Date(caseData.created_date).toLocaleDateString('en-GB')}
                </Typography>
              </Box>

              <Box flex={1}>
                <Box display="flex" alignItems="center" mb={2}>
                  <PlaybookIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Assigned Playbook</Typography>
                </Box>
                <Typography variant="body1" color="text.secondary" data-testid="case-playbook">
                  {getPlaybookName(caseData.playbook_id)}
                </Typography>
              </Box>
            </Box>

            <Box>
              <Typography variant="h6" gutterBottom>
                Summary
              </Typography>
              <Typography variant="body1" color="text.secondary" data-testid="case-summary">
                {caseData.summary}
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Key Parties */}
      {caseData.key_parties && caseData.key_parties.length > 0 && (
        <Card sx={{ mb: 4 }} data-testid="key-parties-section">
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <GroupIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="h5" component="h2">
                Key Parties
              </Typography>
            </Box>
            <Divider sx={{ mb: 3 }} />
            <List>
              {caseData.key_parties.map((party, index) => (
                <ListItem key={index} divider={index < caseData.key_parties.length - 1}>
                  <ListItemIcon>
                    <PersonIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary={party} />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default CaseOverviewTab;