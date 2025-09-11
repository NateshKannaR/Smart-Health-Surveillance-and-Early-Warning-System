import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  AlertTitle
} from '@mui/material';
import {
  HealthAndSafety,
  Delete,
  CheckCircle,
  Person,
  LocationOn,
  CalendarToday,
  Refresh
} from '@mui/icons-material';
import LoadingScreen from '../components/LoadingScreen';
import StatusCard from '../components/StatusCard';

const HealthReports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReports();
    const interval = setInterval(fetchReports, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchReports = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/health/reports');
      if (response.ok) {
        const data = await response.json();
        setReports(data);
      }
    } catch (error) {
      console.error('Error fetching reports:', error);
    } finally {
      setLoading(false);
    }
  };

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [cureDialogOpen, setCureDialogOpen] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null);

  const handleDeleteClick = (report) => {
    setSelectedReport(report);
    setDeleteDialogOpen(true);
  };

  const handleCureClick = (report) => {
    setSelectedReport(report);
    setCureDialogOpen(true);
  };

  const deleteReport = async () => {
    if (!selectedReport) return;
    
    const id = selectedReport.id;
    
    try {
      const response = await fetch(`http://localhost:8000/api/health/reports/${id}`, {
        method: 'DELETE'
      });
      
      const result = await response.json();
      
      if (response.ok && result.status === 'success') {
        setReports(reports.filter(r => r.id !== id));
        setTimeout(() => fetchReports(), 500);
      }
    } catch (error) {
      console.error('Delete error:', error);
    } finally {
      setDeleteDialogOpen(false);
      setSelectedReport(null);
    }
  };

  const markCured = async () => {
    if (!selectedReport) return;
    
    const id = selectedReport.id;
    
    try {
      const response = await fetch(`http://localhost:8000/api/health/reports/${id}/cure`, {
        method: 'PUT'
      });
      
      const result = await response.json();
      
      if (response.ok && result.status === 'success') {
        setReports(reports.filter(r => r.id !== id));
        setTimeout(() => fetchReports(), 500);
      }
    } catch (error) {
      console.error('Cure error:', error);
    } finally {
      setCureDialogOpen(false);
      setSelectedReport(null);
    }
  };

  if (loading) return <LoadingScreen message="Loading Health Reports" />;

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'error';
      case 'severe': return 'error';
      case 'high': return 'warning';
      case 'moderate': return 'warning';
      case 'medium': return 'info';
      case 'mild': return 'success';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const criticalReports = reports.filter(r => ['critical', 'severe'].includes(r.severity?.toLowerCase()));
  const highReports = reports.filter(r => ['high', 'moderate'].includes(r.severity?.toLowerCase()));
  const mediumReports = reports.filter(r => r.severity?.toLowerCase() === 'medium');
  const lowReports = reports.filter(r => ['mild', 'low'].includes(r.severity?.toLowerCase()));

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
              <HealthAndSafety color="primary" />
              Health Reports Management
            </Typography>
            <Typography 
              variant="body1" 
              color="text.secondary"
              sx={{ fontWeight: 500 }}
            >
              Monitor and manage active health cases and patient records
            </Typography>
          </Box>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchReports}
            sx={{ fontWeight: 600 }}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Critical Cases"
            value={criticalReports.length}
            color="#ef4444"
            icon={<HealthAndSafety sx={{ fontSize: 28 }} />}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="High Priority"
            value={highReports.length}
            color="#f59e0b"
            icon={<HealthAndSafety sx={{ fontSize: 28 }} />}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Medium Cases"
            value={mediumReports.length}
            color="#06b6d4"
            icon={<HealthAndSafety sx={{ fontSize: 28 }} />}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Mild Cases"
            value={lowReports.length}
            color="#10b981"
            icon={<HealthAndSafety sx={{ fontSize: 28 }} />}
            variant="accent"
          />
        </Grid>
      </Grid>
      
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
          Active Health Cases ({reports.length})
        </Typography>
        
        {reports.length === 0 ? (
          <Alert severity="info" sx={{ textAlign: 'center' }}>
            <AlertTitle>No Active Cases</AlertTitle>
            No active health reports found in the system
          </Alert>
        ) : (
          <Grid container spacing={2}>
            {reports.map(report => (
              <Grid item xs={12} key={report.id}>
                <Card 
                  sx={{ 
                    border: '1px solid',
                    borderColor: `${getSeverityColor(report.severity)}.light`,
                    borderLeftWidth: 4,
                    borderLeftColor: `${getSeverityColor(report.severity)}.main`
                  }}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <Box sx={{ flex: 1 }}>
                        <Box sx={{ display: 'flex', gap: 2, mb: 2, alignItems: 'center' }}>
                          <Chip
                            label={report.severity?.toUpperCase()}
                            color={getSeverityColor(report.severity)}
                            variant="outlined"
                            sx={{ fontWeight: 600 }}
                          />
                          <Chip
                            label={`ID: ${report.id}`}
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
                            color: 'text.primary'
                          }}
                        >
                          {report.disease?.replace('_', ' ').toUpperCase()}
                        </Typography>
                        
                        <Grid container spacing={2}>
                          <Grid item xs={12} sm={4}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                              <LocationOn color="action" sx={{ fontSize: 18 }} />
                              <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                                Location
                              </Typography>
                            </Box>
                            <Typography variant="body2" sx={{ fontWeight: 500 }}>
                              {report.location}
                            </Typography>
                          </Grid>
                          <Grid item xs={12} sm={4}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                              <Person color="action" sx={{ fontSize: 18 }} />
                              <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                                Patient
                              </Typography>
                            </Box>
                            <Typography variant="body2" sx={{ fontWeight: 500 }}>
                              Age: {report.patient_age || 'N/A'}, Gender: {report.patient_gender || 'N/A'}
                            </Typography>
                          </Grid>
                          <Grid item xs={12} sm={4}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                              <CalendarToday color="action" sx={{ fontSize: 18 }} />
                              <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600 }}>
                                Reported
                              </Typography>
                            </Box>
                            <Typography variant="body2" sx={{ fontWeight: 500 }}>
                              {new Date(report.reported_at).toLocaleDateString()}
                            </Typography>
                          </Grid>
                        </Grid>
                      </Box>
                      
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, ml: 2 }}>
                        <Button
                          variant="contained"
                          color="success"
                          size="small"
                          startIcon={<CheckCircle />}
                          onClick={() => handleCureClick(report)}
                          sx={{ fontWeight: 600, fontSize: '0.75rem' }}
                        >
                          Mark Cured
                        </Button>
                        
                        <IconButton
                          color="error"
                          onClick={() => handleDeleteClick(report)}
                          sx={{ 
                            '&:hover': {
                              backgroundColor: 'error.light',
                              color: 'white'
                            }
                          }}
                        >
                          <Delete />
                        </IconButton>
                      </Box>
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
        <DialogTitle>Delete Health Report</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this health report? This action cannot be undone.
          </Typography>
          {selectedReport && (
            <Box sx={{ mt: 2, p: 2, backgroundColor: 'grey.100', borderRadius: 1 }}>
              <Typography variant="body2" color="text.secondary">
                <strong>Report ID:</strong> {selectedReport.id}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Disease:</strong> {selectedReport.disease?.replace('_', ' ')}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Location:</strong> {selectedReport.location}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={deleteReport} color="error" variant="contained">
            Delete Report
          </Button>
        </DialogActions>
      </Dialog>

      {/* Cure Confirmation Dialog */}
      <Dialog open={cureDialogOpen} onClose={() => setCureDialogOpen(false)}>
        <DialogTitle>Mark Patient as Cured</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to mark this patient as cured? This will remove the case from active reports.
          </Typography>
          {selectedReport && (
            <Box sx={{ mt: 2, p: 2, backgroundColor: 'success.light', borderRadius: 1 }}>
              <Typography variant="body2" color="success.dark">
                <strong>Patient:</strong> Age {selectedReport.patient_age}, {selectedReport.patient_gender}
              </Typography>
              <Typography variant="body2" color="success.dark">
                <strong>Disease:</strong> {selectedReport.disease?.replace('_', ' ')}
              </Typography>
              <Typography variant="body2" color="success.dark">
                <strong>Location:</strong> {selectedReport.location}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCureDialogOpen(false)}>Cancel</Button>
          <Button onClick={markCured} color="success" variant="contained">
            Mark as Cured
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default HealthReports;