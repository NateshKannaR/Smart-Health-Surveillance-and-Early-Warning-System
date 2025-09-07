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
  TableRow,
  Alert
} from '@mui/material';
import {
  TrendingUp,
  Psychology,
  Timeline,
  Analytics
} from '@mui/icons-material';
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

function Predictions() {
  const [predictions, setPredictions] = useState([]);
  const [trendData, setTrendData] = useState([]);
  const [riskScore, setRiskScore] = useState(0);

  useEffect(() => {
    fetchPredictions();
    fetchTrendData();
  }, []);

  const fetchPredictions = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/ai/predictions');
      const data = await response.json();
      
      const formattedPredictions = data.map((pred, index) => ({
        id: pred.id || index + 1,
        disease: pred.disease || 'Unknown',
        location: pred.location || 'Unknown',
        riskScore: pred.riskScore || 0,
        predictedCases: pred.predictedCases || 0,
        confidence: pred.confidence || 0,
        factors: pred.factors || [],
        timeframe: pred.timeframe || '7-14 days'
      }));
      
      setPredictions(formattedPredictions);
      if (formattedPredictions.length > 0) {
        setRiskScore(Math.max(...formattedPredictions.map(p => p.riskScore)));
      }
    } catch (error) {
      console.error('Error fetching predictions:', error);
      setPredictions([]);
    }
  };

  const fetchTrendData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/health/reports');
      const reports = await response.json();
      
      // Group reports by week and disease
      const weeklyData = {};
      reports.forEach(report => {
        const date = new Date(report.reported_at);
        const weekStart = new Date(date.setDate(date.getDate() - date.getDay()));
        const weekKey = weekStart.toISOString().split('T')[0];
        
        if (!weeklyData[weekKey]) {
          weeklyData[weekKey] = { date: weekKey, cholera: 0, diarrhea: 0, typhoid: 0, other: 0 };
        }
        
        const disease = report.disease?.toLowerCase() || 'other';
        if (weeklyData[weekKey][disease] !== undefined) {
          weeklyData[weekKey][disease]++;
        } else {
          weeklyData[weekKey].other++;
        }
      });
      
      const trendArray = Object.values(weeklyData).sort((a, b) => new Date(a.date) - new Date(b.date));
      setTrendData(trendArray.slice(-8)); // Last 8 weeks
    } catch (error) {
      console.error('Error fetching trend data:', error);
      setTrendData([]);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 80) return 'error';
    if (score >= 60) return 'warning';
    if (score >= 40) return 'info';
    return 'success';
  };

  const getRiskLevel = (score) => {
    if (score >= 80) return 'Critical';
    if (score >= 60) return 'High';
    if (score >= 40) return 'Medium';
    return 'Low';
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom sx={{ color: 'white', mb: 3 }}>
            AI/ML Outbreak Predictions
          </Typography>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Psychology sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6">AI Models Active</Typography>
              <Typography variant="h3" color="primary">3</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <TrendingUp sx={{ fontSize: 40, color: 'warning.main', mb: 2 }} />
              <Typography variant="h6">Risk Score</Typography>
              <Typography variant="h3" color={getRiskColor(riskScore) + '.main'}>
                {riskScore}
              </Typography>
              <Chip
                label={getRiskLevel(riskScore)}
                color={getRiskColor(riskScore)}
                size="small"
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Timeline sx={{ fontSize: 40, color: 'info.main', mb: 2 }} />
              <Typography variant="h6">Predictions</Typography>
              <Typography variant="h3" color="info">{predictions.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Analytics sx={{ fontSize: 40, color: 'success.main', mb: 2 }} />
              <Typography variant="h6">Accuracy</Typography>
              <Typography variant="h3" color="success.main">87%</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          {predictions.some(p => p.riskScore >= 60) && (
            <Alert severity="warning" sx={{ mb: 3 }}>
              <Typography variant="h6">High Risk Alert</Typography>
              {predictions.filter(p => p.riskScore >= 60).map(p => 
                `${p.disease} outbreak predicted in ${p.location} with ${p.riskScore}% risk score. Immediate preventive measures recommended.`
              ).join(' ')}
            </Alert>
          )}
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>Disease Trend Prediction</Typography>
            <ResponsiveContainer width="100%" height="90%">
              <AreaChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="cholera"
                  stackId="1"
                  stroke="#ff4444"
                  fill="#ff4444"
                  fillOpacity={0.6}
                />
                <Area
                  type="monotone"
                  dataKey="diarrhea"
                  stackId="1"
                  stroke="#ffaa00"
                  fill="#ffaa00"
                  fillOpacity={0.6}
                />
                <Area
                  type="monotone"
                  dataKey="typhoid"
                  stackId="1"
                  stroke="#00aaff"
                  fill="#00aaff"
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>Risk Factors</Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" gutterBottom>Water Quality</Typography>
              <LinearProgress variant="determinate" value={75} color="error" sx={{ mb: 2 }} />
              
              <Typography variant="body2" gutterBottom>Sanitation Level</Typography>
              <LinearProgress variant="determinate" value={45} color="warning" sx={{ mb: 2 }} />
              
              <Typography variant="body2" gutterBottom>Population Density</Typography>
              <LinearProgress variant="determinate" value={60} color="info" sx={{ mb: 2 }} />
              
              <Typography variant="body2" gutterBottom>Seasonal Factors</Typography>
              <LinearProgress variant="determinate" value={80} color="error" sx={{ mb: 2 }} />
              
              <Typography variant="body2" gutterBottom>Healthcare Access</Typography>
              <LinearProgress variant="determinate" value={30} color="success" sx={{ mb: 2 }} />
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Outbreak Predictions</Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Disease</TableCell>
                    <TableCell>Location</TableCell>
                    <TableCell>Risk Score</TableCell>
                    <TableCell>Predicted Cases</TableCell>
                    <TableCell>Confidence</TableCell>
                    <TableCell>Timeframe</TableCell>
                    <TableCell>Key Factors</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {predictions.map((prediction) => (
                    <TableRow key={prediction.id}>
                      <TableCell>{prediction.disease}</TableCell>
                      <TableCell>{prediction.location}</TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          {prediction.riskScore}
                          <Chip
                            label={getRiskLevel(prediction.riskScore)}
                            color={getRiskColor(prediction.riskScore)}
                            size="small"
                            sx={{ ml: 1 }}
                          />
                        </Box>
                      </TableCell>
                      <TableCell>{prediction.predictedCases}</TableCell>
                      <TableCell>{prediction.confidence}%</TableCell>
                      <TableCell>{prediction.timeframe}</TableCell>
                      <TableCell>
                        {prediction.factors.map((factor, index) => (
                          <Chip
                            key={index}
                            label={factor}
                            size="small"
                            variant="outlined"
                            sx={{ mr: 0.5, mb: 0.5 }}
                          />
                        ))}
                      </TableCell>
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

export default Predictions;