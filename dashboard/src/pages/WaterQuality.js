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
  AlertTitle,
  LinearProgress
} from '@mui/material';
import {
  WaterDrop,
  Delete,
  Science,
  Thermostat,
  LocationOn,
  CalendarToday,
  Refresh,
  CheckCircle,
  Warning
} from '@mui/icons-material';
import LoadingScreen from '../components/LoadingScreen';
import StatusCard from '../components/StatusCard';

const WaterQuality = () => {
  const [waterSources, setWaterSources] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWaterSources();
    const interval = setInterval(fetchWaterSources, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchWaterSources = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/water/sources');
      if (response.ok) {
        const data = await response.json();
        setWaterSources(data);
      }
    } catch (error) {
      console.error('Error fetching water sources:', error);
    } finally {
      setLoading(false);
    }
  };

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedSource, setSelectedSource] = useState(null);

  const handleDeleteClick = (source) => {
    setSelectedSource(source);
    setDeleteDialogOpen(true);
  };

  const deleteWaterSource = async () => {
    if (!selectedSource) return;
    
    const id = selectedSource.id;
    
    try {
      const response = await fetch(`http://localhost:8000/api/water/sources/${id}`, {
        method: 'DELETE'
      });
      
      const result = await response.json();
      
      if (response.ok && result.status === 'success') {
        setWaterSources(waterSources.filter(w => w.id !== id));
        setTimeout(() => fetchWaterSources(), 500);
      }
    } catch (error) {
      console.error('Delete error:', error);
    } finally {
      setDeleteDialogOpen(false);
      setSelectedSource(null);
    }
  };

  const getPHColor = (ph) => {
    if (ph >= 6.5 && ph <= 8.5) return 'success';
    return 'error';
  };

  const getTurbidityColor = (turbidity) => {
    if (turbidity <= 5) return 'success';
    return 'error';
  };

  const getBacteriaColor = (count) => {
    if (count <= 10) return 'success';
    return 'error';
  };

  if (loading) return <LoadingScreen message="Loading Water Quality Data" />;

  const safeWater = waterSources.filter(w => w.is_safe);
  const contaminatedWater = waterSources.filter(w => !w.is_safe);

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
              <WaterDrop color="primary" />
              Water Quality Management
            </Typography>
            <Typography 
              variant="body1" 
              color="text.secondary"
              sx={{ fontWeight: 500 }}
            >
              Monitor water source safety and quality parameters across all locations
            </Typography>
          </Box>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchWaterSources}
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
            title="Safe Water Sources"
            value={safeWater.length}
            color="#10b981"
            icon={<CheckCircle sx={{ fontSize: 28 }} />}
            progress={waterSources.length > 0 ? (safeWater.length / waterSources.length) * 100 : 0}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Contaminated Sources"
            value={contaminatedWater.length}
            color="#ef4444"
            icon={<Warning sx={{ fontSize: 28 }} />}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Total Sources Monitored"
            value={waterSources.length}
            color="#06b6d4"
            icon={<WaterDrop sx={{ fontSize: 28 }} />}
            variant="accent"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <StatusCard
            title="Safety Rate"
            value={`${waterSources.length > 0 ? ((safeWater.length / waterSources.length) * 100).toFixed(1) : 0}%`}
            color="#3b82f6"
            icon={<Science sx={{ fontSize: 28 }} />}
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
          Water Source Reports ({waterSources.length})
        </Typography>
        
        {waterSources.length === 0 ? (
          <Alert severity="info" sx={{ textAlign: 'center' }}>
            <AlertTitle>No Data Available</AlertTitle>
            No water source reports found in the system
          </Alert>
        ) : (
          <Grid container spacing={2}>
            {waterSources.map(source => (
              <Grid item xs={12} key={source.id}>
                <Card 
                  sx={{ 
                    border: '1px solid',
                    borderColor: source.is_safe ? 'success.light' : 'error.light',
                    borderLeftWidth: 4,
                    borderLeftColor: source.is_safe ? 'success.main' : 'error.main'
                  }}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <Box sx={{ flex: 1 }}>
                        <Box sx={{ display: 'flex', gap: 2, mb: 2, alignItems: 'center' }}>
                          <Chip
                            icon={source.is_safe ? <CheckCircle /> : <Warning />}
                            label={source.is_safe ? 'SAFE' : 'CONTAMINATED'}
                            color={source.is_safe ? 'success' : 'error'}
                            variant="outlined"
                            sx={{ fontWeight: 600 }}
                          />
                          <Chip
                            label={`ID: ${source.id}`}
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
                          <LocationOn color="action" sx={{ fontSize: 20 }} />
                          {source.location}
                        </Typography>
                        
                        <Grid container spacing={2}>
                          <Grid item xs={12} sm={6} md={2}>
                            <Box sx={{ textAlign: 'center', p: 1.5, backgroundColor: 'grey.50', borderRadius: 1 }}>
                              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                pH LEVEL
                              </Typography>
                              <Typography 
                                variant="h6" 
                                sx={{ 
                                  fontWeight: 700,
                                  color: `${getPHColor(source.ph_level)}.main`
                                }}
                              >
                                {source.ph_level}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                (Safe: 6.5-8.5)
                              </Typography>
                            </Box>
                          </Grid>
                          <Grid item xs={12} sm={6} md={2}>
                            <Box sx={{ textAlign: 'center', p: 1.5, backgroundColor: 'grey.50', borderRadius: 1 }}>
                              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                TURBIDITY
                              </Typography>
                              <Typography 
                                variant="h6" 
                                sx={{ 
                                  fontWeight: 700,
                                  color: `${getTurbidityColor(source.turbidity)}.main`
                                }}
                              >
                                {source.turbidity}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                NTU (Safe: ≤5)
                              </Typography>
                            </Box>
                          </Grid>
                          <Grid item xs={12} sm={6} md={2}>
                            <Box sx={{ textAlign: 'center', p: 1.5, backgroundColor: 'grey.50', borderRadius: 1 }}>
                              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                BACTERIA
                              </Typography>
                              <Typography 
                                variant="h6" 
                                sx={{ 
                                  fontWeight: 700,
                                  color: `${getBacteriaColor(source.bacterial_count)}.main`
                                }}
                              >
                                {source.bacterial_count}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                CFU/ml (Safe: ≤10)
                              </Typography>
                            </Box>
                          </Grid>
                          <Grid item xs={12} sm={6} md={2}>
                            <Box sx={{ textAlign: 'center', p: 1.5, backgroundColor: 'grey.50', borderRadius: 1 }}>
                              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                TEMPERATURE
                              </Typography>
                              <Typography variant="h6" sx={{ fontWeight: 700, color: 'text.primary' }}>
                                {source.temperature}°C
                              </Typography>
                            </Box>
                          </Grid>
                          <Grid item xs={12} sm={6} md={2}>
                            <Box sx={{ textAlign: 'center', p: 1.5, backgroundColor: 'grey.50', borderRadius: 1 }}>
                              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                SOURCE TYPE
                              </Typography>
                              <Typography variant="body2" sx={{ fontWeight: 600, color: 'text.primary' }}>
                                {source.source_type?.toUpperCase()}
                              </Typography>
                            </Box>
                          </Grid>
                          <Grid item xs={12} sm={6} md={2}>
                            <Box sx={{ textAlign: 'center', p: 1.5, backgroundColor: 'grey.50', borderRadius: 1 }}>
                              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                                TESTED DATE
                              </Typography>
                              <Typography variant="body2" sx={{ fontWeight: 600, color: 'text.primary' }}>
                                {new Date(source.tested_at).toLocaleDateString()}
                              </Typography>
                            </Box>
                          </Grid>
                        </Grid>
                      </Box>
                      
                      <IconButton
                        onClick={() => handleDeleteClick(source)}
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
        <DialogTitle>Delete Water Source Report</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this water source report? This action cannot be undone.
          </Typography>
          {selectedSource && (
            <Box sx={{ mt: 2, p: 2, backgroundColor: 'grey.100', borderRadius: 1 }}>
              <Typography variant="body2" color="text.secondary">
                <strong>Source ID:</strong> {selectedSource.id}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Location:</strong> {selectedSource.location}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Status:</strong> {selectedSource.is_safe ? 'Safe' : 'Contaminated'}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={deleteWaterSource} color="error" variant="contained">
            Delete Report
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default WaterQuality;