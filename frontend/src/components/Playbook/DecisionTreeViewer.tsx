import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Paper,
  Divider,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  AccountTree as TreeIcon,
  PlayArrow as ArrowIcon,
  CheckCircle as CheckIcon,
  RadioButtonUnchecked as NodeIcon,
  TrendingUp as SuccessIcon,
  Warning as WarningIcon,
  Error as ErrorIcon
} from '@mui/icons-material';

interface DecisionNode {
  question?: string;
  options?: Record<string, string>;
  result?: string;
  recommended_actions?: string[];
  monetary_range?: string;
}

interface DecisionTree {
  root: string;
  nodes: Record<string, DecisionNode>;
}

interface DecisionTreeViewerProps {
  decisionTree: DecisionTree;
  className?: string;
}

const DecisionTreeViewer: React.FC<DecisionTreeViewerProps> = ({ decisionTree, className }) => {
  const [selectedPath, setSelectedPath] = useState<string[]>([]);
  const [currentNode, setCurrentNode] = useState<string>(decisionTree.root || '');

  // Early return if no decision tree data
  if (!decisionTree || !decisionTree.nodes || !decisionTree.root) {
    return (
      <Card className={className}>
        <CardContent>
          <Alert severity="info">
            No decision tree data available for this playbook.
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const getCurrentNodeData = (): DecisionNode => {
    return decisionTree.nodes[currentNode] || {};
  };

  const handleOptionSelect = (option: string, nextNode: string) => {
    setSelectedPath([...selectedPath, `${currentNode}:${option}`]);
    setCurrentNode(nextNode);
  };

  const resetTree = () => {
    setSelectedPath([]);
    setCurrentNode(decisionTree.root);
  };

  const getAssessmentColor = (nodeId: string) => {
    if (nodeId.includes('strong')) return 'success';
    if (nodeId.includes('moderate')) return 'warning';
    if (nodeId.includes('weak')) return 'error';
    return 'primary';
  };

  const getAssessmentIcon = (nodeId: string) => {
    if (nodeId.includes('strong')) return <SuccessIcon />;
    if (nodeId.includes('moderate')) return <WarningIcon />;
    if (nodeId.includes('weak')) return <ErrorIcon />;
    return <NodeIcon />;
  };

  const isAssessmentNode = (nodeId: string) => {
    return nodeId.includes('assessment');
  };

  const formatNodeTitle = (nodeId: string) => {
    return nodeId
      .replace(/_/g, ' ')
      .replace(/([a-z])([A-Z])/g, '$1 $2')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const formatOptionText = (option: string) => {
    return option
      .replace(/_/g, ' ')
      .replace(/([a-z])([A-Z])/g, '$1 $2')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const currentNodeData = getCurrentNodeData();
  const isCurrentAssessment = isAssessmentNode(currentNode);

  return (
    <Box className={className}>
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
            <Box display="flex" alignItems="center" gap={1}>
              <TreeIcon color="primary" />
              <Typography variant="h5">
                Decision Tree Logic
              </Typography>
            </Box>
            {selectedPath.length > 0 && (
              <Button
                variant="outlined"
                size="small"
                onClick={resetTree}
              >
                Reset to Start
              </Button>
            )}
          </Box>

          <Typography variant="body2" color="text.secondary" paragraph>
            This decision tree shows how the playbook evaluates cases and determines recommendations.
            Follow the path by selecting options to see how different case facts lead to different outcomes.
          </Typography>

          {selectedPath.length === 0 && (
            <Alert severity="info" sx={{ mb: 3 }}>
              <Typography variant="body2">
                <strong>Start here:</strong> This is the root decision point. Select an option below to navigate through the decision tree.
              </Typography>
            </Alert>
          )}

          {/* Path Breadcrumb */}
          {selectedPath.length > 0 && (
            <Paper sx={{ p: 2, mb: 3, backgroundColor: 'grey.50' }}>
              <Typography variant="subtitle2" gutterBottom>
                Decision Path:
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {selectedPath.map((pathStep, index) => {
                  const [nodeId, option] = pathStep.split(':');
                  return (
                    <Chip
                      key={index}
                      label={formatOptionText(option)}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  );
                })}
              </Box>
            </Paper>
          )}

          {/* Current Node */}
          <Card variant="outlined" sx={{ mb: 3 }}>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2} mb={2}>
                {getAssessmentIcon(currentNode)}
                <Typography variant="h6" color={isCurrentAssessment ? getAssessmentColor(currentNode) : 'primary'}>
                  {formatNodeTitle(currentNode)}
                </Typography>
                {isCurrentAssessment && (
                  <Chip
                    label="Final Assessment"
                    color={getAssessmentColor(currentNode) as any}
                    size="small"
                  />
                )}
              </Box>

              {/* Question Node */}
              {currentNodeData.question && (
                <Box>
                  <Typography variant="body1" fontWeight="bold" gutterBottom>
                    {currentNodeData.question}
                  </Typography>
                  
                  {currentNodeData.options && (
                    <Box display="flex" flexDirection="column" gap={2} mt={2}>
                      {Object.entries(currentNodeData.options).map(([option, nextNode]) => (
                        <Button
                          key={option}
                          variant="outlined"
                          startIcon={<ArrowIcon />}
                          onClick={() => handleOptionSelect(option, nextNode)}
                          sx={{
                            justifyContent: 'flex-start',
                            textAlign: 'left',
                            p: 2
                          }}
                        >
                          {formatOptionText(option)}
                        </Button>
                      ))}
                    </Box>
                  )}
                </Box>
              )}

              {/* Assessment Node */}
              {currentNodeData.result && (
                <Box>
                  <Alert 
                    severity={getAssessmentColor(currentNode) as any} 
                    sx={{ mb: 3 }}
                    icon={getAssessmentIcon(currentNode)}
                  >
                    <Typography variant="body1" fontWeight="bold">
                      {currentNodeData.result}
                    </Typography>
                  </Alert>

                  {/* Recommended Actions */}
                  {currentNodeData.recommended_actions && currentNodeData.recommended_actions.length > 0 && (
                    <Box mb={3}>
                      <Typography variant="h6" gutterBottom>
                        Recommended Actions:
                      </Typography>
                      <List dense>
                        {currentNodeData.recommended_actions.map((action, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <CheckIcon color="primary" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={action} />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}

                  {/* Monetary Range */}
                  {currentNodeData.monetary_range && (
                    <Box>
                      <Typography variant="h6" gutterBottom>
                        Monetary Assessment Range:
                      </Typography>
                      <Chip
                        label={`${currentNodeData.monetary_range.charAt(0).toUpperCase() + currentNodeData.monetary_range.slice(1)} Range`}
                        color={getAssessmentColor(currentNode) as any}
                        sx={{ textTransform: 'capitalize' }}
                      />
                    </Box>
                  )}
                </Box>
              )}
            </CardContent>
          </Card>

          {/* Tree Overview */}
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Decision Tree Overview
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                This playbook contains {Object.keys(decisionTree.nodes).length} decision nodes:
              </Typography>
              
              <Box display="flex" flexWrap="wrap" gap={1}>
                {Object.keys(decisionTree.nodes).map((nodeId) => {
                  const isAssessment = isAssessmentNode(nodeId);
                  const isCurrent = nodeId === currentNode;
                  
                  return (
                    <Chip
                      key={nodeId}
                      label={formatNodeTitle(nodeId)}
                      size="small"
                      color={isCurrent ? 'primary' : (isAssessment ? getAssessmentColor(nodeId) as any : 'default')}
                      variant={isCurrent ? 'filled' : 'outlined'}
                      onClick={() => setCurrentNode(nodeId)}
                      sx={{ cursor: 'pointer' }}
                    />
                  );
                })}
              </Box>
            </CardContent>
          </Card>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DecisionTreeViewer;