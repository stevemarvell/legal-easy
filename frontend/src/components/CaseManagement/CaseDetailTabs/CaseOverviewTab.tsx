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

          <Typography variant="body1" color="text.secondary" data-testid="case-summary" sx={{ mb: 3 }}>
            {caseData.summary}
          </Typography>

          <Divider sx={{ mb: 3 }} />

          <Box display="flex" flexDirection="column" gap={3}>
            <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={3}>
              <Box flex={1}>
                <Box display="flex" alignItems="center" mb={2}>
                  <PersonIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Key Parties</Typography>
                </Box>
                <List>
                  {caseData.key_parties.map((party, index) => (
                    <ListItem key={index} divider={index < caseData.key_parties.length - 1}>
                      <ListItemText primary={party} />
                    </ListItem>
                  ))}
                </List>
              </Box>

              <Box flex={1}>
                <Box display="flex" alignItems="center" mb={2}>
                  <GavelIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Case Type</Typography>
                </Box>
                <Typography variant="body1" color="text.secondary" data-testid="case-type" sx={{ mb: 3 }}>
                  {caseData.case_type}
                </Typography>

                <Box display="flex" alignItems="center" mb={2}>
                  <PlaybookIcon color="primary" sx={{ mr: 1 }} />
                  <Typography variant="h6">Assigned Playbook</Typography>
                </Box>
                <Typography variant="body1" color="text.secondary" data-testid="case-playbook">
                  {getPlaybookName(caseData.playbook_id)}
                </Typography>
              </Box>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CaseOverviewTab;