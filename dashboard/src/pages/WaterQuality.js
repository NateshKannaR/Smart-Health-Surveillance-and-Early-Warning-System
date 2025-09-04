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

function WaterQuality() {
  const [waterData, setWaterData] = useState([]);
  const [stats, setStats] = useState({ safe: 0, contaminated: 0, total: 0 });

  useEffect(() => {
    // Mock water quality data
    const mockData = [
      { id: 1, location: 'Well A', ph: 7.2, turbidity: 2.1, bacteria: 45, temp: 24, status: 'safe', lastTest: '2024-01-15' },
      { id: 2, location: 'River B', ph: 6.8, turbidity: 8.5, bacteria: 150, temp: 22, status: 'contaminated', lastTest: '2024-01-14' },
      { id: 3, location: 'Pond C', ph: 7.5, turbidity: 3.2, bacteria: 80, temp: 26, status: 'safe', lastTest: '2024-01-13' },
      { id: 4, location: 'Tap D', ph: 5.9, turbidity: 12.0, bacteria: 200, temp: 25, status: 'contaminated', lastTest: '2024-01-12' },
    ];
    
    setWaterData(mockData);
    setStats({
      total: mockData.length,
      safe: mockData.filter(d => d.status === 'safe').length,
      contaminated: mockData.filter(d => d.status === 'contaminated').length
    });
  }, []);

  const getStatusColor = (status) => {
    return status === 'safe' ? 'success' : 'error';
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
              <Typography variant="h3" color="primary">{stats.total}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Science sx={{ fontSize: 40, color: 'success.main', mb: 2 }} />
              <Typography variant="h6">Safe Sources</Typography>
              <Typography variant="h3" color="success.main">{stats.safe}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Warning sx={{ fontSize: 40, color: 'error.main', mb: 2 }} />
              <Typography variant="h6">Contaminated</Typography>
              <Typography variant="h3" color="error.main">{stats.contaminated}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Safety Rate</Typography>
              <Typography variant="h3" color="primary">
                {((stats.safe / stats.total) * 100).toFixed(1)}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={(stats.safe / stats.total) * 100} 
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
                      <TableCell>{source.location}</TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          {source.ph}
                          <Chip
                            size="small"
                            label={getParameterStatus(source.ph, 6.5, 8.5).status}
                            color={getParameterStatus(source.ph, 6.5, 8.5).color}
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
                          {source.bacteria}
                          <Chip
                            size="small"
                            label={getParameterStatus(source.bacteria, 0, 100).status}
                            color={getParameterStatus(source.bacteria, 0, 100).color}
                            sx={{ ml: 1 }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Thermostat sx={{ mr: 1, verticalAlign: 'middle' }} />
                        {source.temp}
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={source.status}
                          color={getStatusColor(source.status)}
                          variant="filled"
                        />
                      </TableCell>
                      <TableCell>{source.lastTest}</TableCell>
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