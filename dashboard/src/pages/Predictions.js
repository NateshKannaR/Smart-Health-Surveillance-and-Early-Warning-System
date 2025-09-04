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
    // Mock prediction data
    const mockPredictions = [
      {
        id: 1,
        disease: 'Cholera',
        location: 'Village B',
        riskScore: 85,
        predictedCases: 12,
        confidence: 92,
        factors: ['High rainfall', 'Poor sanitation', 'Water contamination'],
        timeframe: '7 days'
      },
      {
        id: 2,
        disease: 'Diarrhea',
        location: 'Village A',
        riskScore: 65,
        predictedCases: 8,
        confidence: 78,
        factors: ['Seasonal pattern', 'Population density'],
        timeframe: '14 days'
      },
      {
        id: 3,
        disease: 'Typhoid',
        location: 'Village C',
        riskScore: 45,
        predictedCases: 5,
        confidence: 85,
        factors: ['Historical data', 'Water quality decline'],
        timeframe: '21 days'
      }
    ];

    const mockTrendData = [
      { date: '2024-01-01', cholera: 2, diarrhea: 5, typhoid: 1 },
      { date: '2024-01-08', cholera: 3, diarrhea: 7, typhoid: 2 },
      { date: '2024-01-15', cholera: 5, diarrhea: 9, typhoid: 3 },
      { date: '2024-01-22', cholera: 8, diarrhea: 12, typhoid: 4 },
      { date: '2024-01-29', cholera: 12, diarrhea: 15, typhoid: 5 },
    ];

    setPredictions(mockPredictions);
    setTrendData(mockTrendData);
    setRiskScore(Math.max(...mockPredictions.map(p => p.riskScore)));
  }, []);

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
          <Alert severity="warning" sx={{ mb: 3 }}>
            <Typography variant="h6">High Risk Alert</Typography>
            Cholera outbreak predicted in Village B with 85% risk score. Immediate preventive measures recommended.
          </Alert>
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