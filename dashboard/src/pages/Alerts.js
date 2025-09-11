import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Chip,
  Button,
  Alert,
  AlertTitle,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle,
  Delete,
  Refresh,
  NotificationsActive
} from '@mui/icons-material';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [alertToDelete, setAlertToDelete] = useState(null);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = async () => {
    try {
      setError(null);
      const response = await fetch('http://localhost:8000/api/alerts');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Fetched alerts:', data);
      setAlerts(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching alerts:', error);
      setError(error.message);
      setAlerts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (alert) => {
    setAlertToDelete(alert);
    setDeleteDialogOpen(true);
  };

  const deleteAlert = async () => {
    if (!alertToDelete) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/alerts/${alertToDelete.id}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        setAlerts(alerts.filter(a => a.id !== alertToDelete.id));
        setTimeout(() => fetchAlerts(), 500);
      }
    } catch (error) {
      console.error('Delete error:', error);
    } finally {
      setDeleteDialogOpen(false);
      setAlertToDelete(null);
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return <Error />;
      case 'high': return <Warning />;
      case 'medium': return <Info />;
      case 'low': return <CheckCircle />;
      default: return <Info />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>Loading Alerts...</Typography>
        </Box>
      </Container>
    );
  }

  const criticalAlerts = alerts.filter(a => a.severity === 'critical');
  const highAlerts = alerts.filter(a => a.severity === 'high');
  const mediumAlerts = alerts.filter(a => a.severity === 'medium');
  const lowAlerts = alerts.filter(a => a.severity === 'low');

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <Typography 
              variant="h4" 
              sx={{ 
                fontWeight: 700, 
                color: 'text.primary',
                mb: 1,
                display: 'flex',
                alignItems: 'center',
                gap: 1
              }}
            >
              <NotificationsActive color="primary" />
              Alert Management System
            </Typography>
            <Typography 
              variant="body1" 
              color="text.secondary"
              sx={{ fontWeight: 500 }}
            >
              Monitor and manage health surveillance alerts in real-time
            </Typography>
          </Box>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchAlerts}
            sx={{ fontWeight: 600 }}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          <AlertTitle>Connection Error</AlertTitle>
          {error} - Please check if the backend server is running.
        </Alert>
      )}
      
      {/* Alert Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} lg={3}>
          <Card sx={{ bgcolor: '#fef2f2', border: '1px solid #fecaca' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Error sx={{ fontSize: 32, color: '#dc2626' }} />
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: '#dc2626' }}>
                    {criticalAlerts.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Critical Alerts
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <Card sx={{ bgcolor: '#fef3c7', border: '1px solid #fcd34d' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Warning sx={{ fontSize: 32, color: '#d97706' }} />
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: '#d97706' }}>
                    {highAlerts.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    High Priority
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <Card sx={{ bgcolor: '#e0f2fe', border: '1px solid #81d4fa' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Info sx={{ fontSize: 32, color: '#0277bd' }} />
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: '#0277bd' }}>
                    {mediumAlerts.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Medium Priority
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <Card sx={{ bgcolor: '#f0fdf4', border: '1px solid #86efac' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <CheckCircle sx={{ fontSize: 32, color: '#16a34a' }} />
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700, color: '#16a34a' }}>
                    {lowAlerts.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Low Priority
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Active Alerts */}
      <Paper sx={{ p: 3 }}>
        <Typography 
          variant="h6" 
          sx={{ 
            fontWeight: 600, 
            mb: 3,
            display: 'flex',
            alignItems: 'center',
            gap: 1
          }}
        >
          Active Alerts ({alerts.length})
        </Typography>
        
        {alerts.length === 0 ? (
          <Alert severity="success" sx={{ textAlign: 'center' }}>
            <AlertTitle>All Clear</AlertTitle>
            No active alerts - All systems are operating normally
          </Alert>
        ) : (
          <Grid container spacing={2}>
            {alerts.map(alert => (
              <Grid item xs={12} key={alert.id}>
                <Card 
                  sx={{ 
                    border: '1px solid',
                    borderColor: `${getSeverityColor(alert.severity)}.light`,
                    borderLeftWidth: 4,
                    borderLeftColor: `${getSeverityColor(alert.severity)}.main`
                  }}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <Box sx={{ flex: 1 }}>
                        <Box sx={{ display: 'flex', gap: 2, mb: 2, alignItems: 'center' }}>
                          <Chip
                            icon={getSeverityIcon(alert.severity)}
                            label={alert.severity?.toUpperCase() || 'UNKNOWN'}
                            color={getSeverityColor(alert.severity)}
                            variant="outlined"
                            sx={{ fontWeight: 600 }}
                          />
                          <Chip
                            label={`ID: ${alert.id}`}
                            variant="outlined"
                            size="small"
                            sx={{ fontWeight: 500 }}
                          />
                          {alert.is_active && (
                            <Chip
                              label="ACTIVE"
                              color="success"
                              size="small"
                              sx={{ fontWeight: 600 }}
                            />
                          )}
                        </Box>
                        
                        <Typography 
                          variant="h6" 
                          sx={{ 
                            fontWeight: 600, 
                            mb: 2,
                            display: 'flex',
                            alignItems: 'center',
                            gap: 1
                          }}
                        >
                          📍 {alert.location || 'System Alert'}
                        </Typography>
                        
                        <Alert 
                          severity={getSeverityColor(alert.severity)} 
                          sx={{ mb: 2 }}
                        >
                          <AlertTitle>Alert Message</AlertTitle>
                          {alert.message || 'No message provided'}
                        </Alert>
                        
                        <Typography 
                          variant="body2" 
                          color="text.secondary"
                          sx={{ fontWeight: 500 }}
                        >
                          📅 Created: {alert.created_at ? new Date(alert.created_at).toLocaleString() : 'Unknown'}
                        </Typography>
                      </Box>
                      
                      <IconButton
                        onClick={() => handleDeleteClick(alert)}
                        color="error"
                        sx={{ 
                          ml: 2,
                          '&:hover': {
                            backgroundColor: 'error.light',
                            color: 'white'
                          }
                        }}
                      >
                        <Delete />
                      </IconButton>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Paper>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Resolve Alert</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to resolve this alert? This action cannot be undone.
          </Typography>
          {alertToDelete && (
            <Box sx={{ mt: 2, p: 2, backgroundColor: 'grey.100', borderRadius: 1 }}>
              <Typography variant="body2" color="text.secondary">
                <strong>Alert ID:</strong> {alertToDelete.id}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Location:</strong> {alertToDelete.location}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={deleteAlert} color="error" variant="contained">
            Resolve Alert
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Alerts;