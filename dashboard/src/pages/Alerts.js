import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Badge
} from '@mui/material';
import {
  Warning,
  Error,
  Info,
  CheckCircle,
  NotificationsActive,
  Send
} from '@mui/icons-material';
import { getAlerts, getAlertStats } from '../services/apiService';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({ total_active_alerts: 0, by_severity: {} });

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [alertsData, statsData] = await Promise.all([
        getAlerts(),
        getAlertStats()
      ]);
      setAlerts(alertsData);
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load alerts data:', error);
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical': return <Error color="error" />;
      case 'high': return <Warning color="warning" />;
      case 'medium': return <Info color="info" />;
      case 'low': return <CheckCircle color="success" />;
      default: return <Info />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const handleResolveAlert = async (id) => {
    try {
      await fetch(`http://localhost:8000/api/alerts/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: false })
      });
      loadData(); // Refresh data
    } catch (error) {
      console.error('Failed to resolve alert:', error);
    }
  };

  const handleSendNotification = (alert) => {
    console.log('Sending notification for:', alert.title);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom sx={{ color: 'white', mb: 3 }}>
            Alert Management System
          </Typography>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Badge badgeContent={stats.active} color="error">
                <NotificationsActive sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
              </Badge>
              <Typography variant="h6">Active Alerts</Typography>
              <Typography variant="h3" color="error">{stats.total_active_alerts || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Error sx={{ fontSize: 40, color: 'error.main', mb: 2 }} />
              <Typography variant="h6">Critical Alerts</Typography>
              <Typography variant="h3" color="error">{stats.by_severity?.critical || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <CheckCircle sx={{ fontSize: 40, color: 'success.main', mb: 2 }} />
              <Typography variant="h6">Resolved</Typography>
              <Typography variant="h3" color="success.main">{alerts.filter(a => !a.is_active).length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Response Rate</Typography>
              <Typography variant="h3" color="primary">
                {alerts.length > 0 ? ((alerts.filter(a => !a.is_active).length / alerts.length) * 100).toFixed(1) : 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Active Alerts</Typography>
            <List>
              {alerts.filter(alert => alert.is_active).map((alert) => (
                <ListItem
                  key={alert.id}
                  sx={{
                    mb: 2,
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: 2,
                    backgroundColor: 'rgba(255,255,255,0.05)'
                  }}
                >
                  <ListItemIcon>
                    {getSeverityIcon(alert.severity)}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <span style={{ fontSize: '1.25rem', fontWeight: 500 }}>Alert #{alert.id}</span>
                        <Chip
                          label={alert.severity}
                          color={getSeverityColor(alert.severity)}
                          size="small"
                        />
                      </div>
                    }
                    secondary={
                      <>
                        <div style={{ marginTop: 8, fontSize: '0.875rem' }}>
                          {alert.severity} severity alert from mobile app
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.7)', marginTop: 4 }}>
                          {new Date(alert.created_at).toLocaleString()}
                        </div>
                      </>
                    }
                  />
                  <div style={{ display: 'flex', gap: 8 }}>
                    <IconButton
                      color="primary"
                      onClick={() => handleSendNotification(alert)}
                      title="Send Notification"
                    >
                      <Send />
                    </IconButton>
                    <IconButton
                      color="success"
                      onClick={() => handleResolveAlert(alert.id)}
                      title="Mark as Resolved"
                    >
                      <CheckCircle />
                    </IconButton>
                  </div>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Recent Resolved Alerts</Typography>
            <List>
              {alerts.filter(alert => !alert.is_active).map((alert) => (
                <ListItem key={alert.id} sx={{ opacity: 0.7 }}>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary={`Alert #${alert.id}`}
                    secondary={`${alert.severity} severity alert - Resolved on ${new Date(alert.created_at).toLocaleString()}`}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Alerts;