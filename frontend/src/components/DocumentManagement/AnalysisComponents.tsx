import React from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Chip,
    Divider,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Accordion,
    AccordionSummary,
    AccordionDetails,
    Paper
} from '@mui/material';
import {
    Event as DateIcon,
    Person as PersonIcon,
    Gavel as LegalIcon,
    ExpandMore as ExpandMoreIcon
} from '@mui/icons-material';

interface PartiesComponentProps {
    parties: string[];
    variant?: 'accordion' | 'paper';
}

interface KeyDatesComponentProps {
    dates: string[];
    variant?: 'accordion' | 'paper';
}

interface KeyClausesComponentProps {
    clauses: string[];
    variant?: 'accordion' | 'paper';
}

const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

export const PartiesComponent: React.FC<PartiesComponentProps> = ({
    parties,
    variant = 'accordion'
}) => {
    const content = (
        <>
            {parties.length > 0 ? (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {parties.map((party, index) => (
                        <Chip
                            key={index}
                            icon={<PersonIcon />}
                            label={party}
                            color="secondary"
                            variant="outlined"
                        />
                    ))}
                </Box>
            ) : (
                <Typography variant="body2" color="text.secondary">
                    No parties identified
                </Typography>
            )}
        </>
    );

    if (variant === 'paper') {
        return (
            <Paper variant="outlined" sx={{ p: 2, height: '100%' }}>
                <Box display="flex" alignItems="center" mb={2}>
                    <PersonIcon color="primary" sx={{ mr: 1 }} />
                    <Typography variant="subtitle1" fontWeight="bold">
                        Parties ({parties.length})
                    </Typography>
                </Box>
                {content}
            </Paper>
        );
    }

    return (
        <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Box display="flex" alignItems="center" gap={1}>
                    <PersonIcon color="primary" />
                    <Typography variant="subtitle1">
                        Parties Involved ({parties.length})
                    </Typography>
                </Box>
            </AccordionSummary>
            <AccordionDetails>
                {content}
            </AccordionDetails>
        </Accordion>
    );
};

export const KeyDatesComponent: React.FC<KeyDatesComponentProps> = ({
    dates,
    variant = 'accordion'
}) => {
    const content = (
        <>
            {dates.length > 0 ? (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {dates.map((date, index) => (
                        <Chip
                            key={index}
                            icon={<DateIcon />}
                            label={formatDate(date)}
                            color="primary"
                            variant="outlined"
                        />
                    ))}
                </Box>
            ) : (
                <Typography variant="body2" color="text.secondary">
                    No key dates identified
                </Typography>
            )}
        </>
    );

    if (variant === 'paper') {
        return (
            <Paper variant="outlined" sx={{ p: 2, height: '100%' }}>
                <Box display="flex" alignItems="center" mb={2}>
                    <DateIcon color="primary" sx={{ mr: 1 }} />
                    <Typography variant="subtitle1" fontWeight="bold">
                        Key Dates ({dates.length})
                    </Typography>
                </Box>
                {content}
            </Paper>
        );
    }

    return (
        <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Box display="flex" alignItems="center" gap={1}>
                    <DateIcon color="primary" />
                    <Typography variant="subtitle1">
                        Key Dates ({dates.length})
                    </Typography>
                </Box>
            </AccordionSummary>
            <AccordionDetails>
                {content}
            </AccordionDetails>
        </Accordion>
    );
};

export const KeyClausesComponent: React.FC<KeyClausesComponentProps> = ({
    clauses,
    variant = 'accordion'
}) => {
    const content = (
        <>
            {clauses.length > 0 ? (
                <List dense>
                    {clauses.map((clause, index) => (
                        <ListItem key={index}>
                            <ListItemIcon>
                                <LegalIcon fontSize="small" color="primary" />
                            </ListItemIcon>
                            <ListItemText
                                primary={
                                    <Paper
                                        variant="outlined"
                                        sx={{
                                            p: 1.5,
                                            backgroundColor: 'background.paper',
                                            borderColor: 'divider',
                                            borderWidth: 1,
                                            '&:hover': {
                                                backgroundColor: 'action.hover'
                                            }
                                        }}
                                    >
                                        <Typography variant="body2" fontWeight="medium">
                                            {clause}
                                        </Typography>
                                    </Paper>
                                }
                            />
                        </ListItem>
                    ))}
                </List>
            ) : (
                <Typography variant="body2" color="text.secondary">
                    No key clauses identified
                </Typography>
            )}
        </>
    );

    if (variant === 'paper') {
        return (
            <Paper variant="outlined" sx={{ p: 2 }}>
                <Box display="flex" alignItems="center" mb={2}>
                    <LegalIcon color="primary" sx={{ mr: 1 }} />
                    <Typography variant="subtitle1" fontWeight="bold">
                        Key Clauses ({clauses.length})
                    </Typography>
                </Box>
                {content}
            </Paper>
        );
    }

    return (
        <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Box display="flex" alignItems="center" gap={1}>
                    <LegalIcon color="primary" />
                    <Typography variant="subtitle1">
                        Key Clauses ({clauses.length})
                    </Typography>
                </Box>
            </AccordionSummary>
            <AccordionDetails>
                {content}
            </AccordionDetails>
        </Accordion>
    );
};