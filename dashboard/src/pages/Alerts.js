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
  DialogActions
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
import LoadingScreen from '../components/LoadingScreen';
import StatusCard from '../components/StatusCard';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/alerts');
      if (response.ok) {
        const data = await response.json();
        setAlerts(data);
      }
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [alertToDelete, setAlertToDelete] = useState(null);

  const handleDeleteClick = (alert) => {
    setAlertToDelete(alert);
    setDeleteDialogOpen(true);
  };

  const deleteAlert = async () => {
    if (!alertToDelete) return;
    
    const id = alertToDelete.id;
    
    try {
      const response = await fetch(`http://localhost:8000/api/alerts/${id}`, {
        method: 'DELETE'
      });
      
      const result = await response.json();
      
      if (response.ok && result.status === 'success') {
        setAlerts(alerts.filter(a => a.id !== id));
        setTimeout(() => fetchAlerts(), 500);
      }
    } catch (error) {
      console.error('Delete error:', error);
    } finally {
      setDeleteDialogOpen(false);
      setAlertToDelete(null);
    }
  };

  if (loading) return <LoadingScreen message="Loading Alerts" />;

  const criticalAlerts = alerts.filter(a => a.severity === 'critical');
  const highAlerts = alerts.filter(a => a.severity === 'high');
  const mediumAlerts = alerts.filter(a => a.severity === 'medium');
  const lowAlerts = alerts.filter(a => a.severity === 'low');

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

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
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
      
      {/* Alert Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Critical Alerts"
            value={criticalAlerts.length}
            color="#ef4444"
            icon={<Error sx={{ fontSize: 28 }} />}
            status={criticalAlerts.length > 0 ? 'Active' : 'Clear'}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="High Priority"
            value={highAlerts.length}
            color="#f59e0b"
            icon={<Warning sx={{ fontSize: 28 }} />}
            status={highAlerts.length > 0 ? 'Warning' : 'Clear'}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Medium Priority"
            value={mediumAlerts.length}
            color="#06b6d4"
            icon={<Info sx={{ fontSize: 28 }} />}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Low Priority"
            value={lowAlerts.length}
            color="#10b981"
            icon={<CheckCircle sx={{ fontSize: 28 }} />}
            variant="accent"
          />
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
                            label={alert.severity?.toUpperCase()}
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
                          📅 Created: {new Date(alert.created_at).toLocaleString()}
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