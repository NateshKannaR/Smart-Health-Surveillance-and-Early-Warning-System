import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Box,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import {
  WaterDrop,
  Science,
  Thermostat,
  Warning
} from '@mui/icons-material';
import { getWaterQualityReports, getWaterQualityStats } from '../services/apiService';

function WaterQuality() {
  const [waterData, setWaterData] = useState([]);
  const [stats, setStats] = useState({ safe_sources: 0, contaminated_sources: 0, total_sources: 0 });

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [reportsData, statsData] = await Promise.all([
        getWaterQualityReports(),
        getWaterQualityStats()
      ]);
      setWaterData(reportsData);
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load water quality data:', error);
    }
  };



  const getParameterStatus = (value, min, max) => {
    if (value >= min && value <= max) return { color: 'success', status: 'Normal' };
    return { color: 'error', status: 'Alert' };
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom sx={{ color: 'white', mb: 3 }}>
            Water Quality Monitoring
          </Typography>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <WaterDrop sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6">Total Sources</Typography>
              <Typography variant="h3" color="primary">{stats.total_sources || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Science sx={{ fontSize: 40, color: 'success.main', mb: 2 }} />
              <Typography variant="h6">Safe Sources</Typography>
              <Typography variant="h3" color="success.main">{stats.safe_sources || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Warning sx={{ fontSize: 40, color: 'error.main', mb: 2 }} />
              <Typography variant="h6">Contaminated</Typography>
              <Typography variant="h3" color="error.main">{stats.contaminated_sources || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Safety Rate</Typography>
              <Typography variant="h3" color="primary">
                {stats.total_sources > 0 ? ((stats.safe_sources / stats.total_sources) * 100).toFixed(1) : 0}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={stats.total_sources > 0 ? (stats.safe_sources / stats.total_sources) * 100 : 0} 
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Water Quality Parameters</Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Location</TableCell>
                    <TableCell>pH Level</TableCell>
                    <TableCell>Turbidity (NTU)</TableCell>
                    <TableCell>Bacteria Count</TableCell>
                    <TableCell>Temperature (°C)</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Last Test</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {waterData.map((source) => (
                    <TableRow key={source.id}>
                      <TableCell>Source {source.id}</TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          {source.ph_level}
                          <Chip
                            size="small"
                            label={getParameterStatus(source.ph_level, 6.5, 8.5).status}
                            color={getParameterStatus(source.ph_level, 6.5, 8.5).color}
                            sx={{ ml: 1 }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          {source.turbidity}
                          <Chip
                            size="small"
                            label={getParameterStatus(source.turbidity, 0, 5).status}
                            color={getParameterStatus(source.turbidity, 0, 5).color}
                            sx={{ ml: 1 }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          {source.bacterial_count}
                          <Chip
                            size="small"
                            label={getParameterStatus(source.bacterial_count, 0, 100).status}
                            color={getParameterStatus(source.bacterial_count, 0, 100).color}
                            sx={{ ml: 1 }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Thermostat sx={{ mr: 1, verticalAlign: 'middle' }} />
                        {source.temperature}
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={source.is_safe ? 'safe' : 'contaminated'}
                          color={source.is_safe ? 'success' : 'error'}
                          variant="filled"
                        />
                      </TableCell>
                      <TableCell>{new Date(source.tested_at).toLocaleDateString()}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default WaterQuality;