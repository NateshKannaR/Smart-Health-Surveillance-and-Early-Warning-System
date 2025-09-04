import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Card,
  CardContent,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel
} from '@mui/material';
import { Add, LocalHospital, TrendingUp } from '@mui/icons-material';

function HealthReports() {
  const [reports, setReports] = useState([]);
  const [open, setOpen] = useState(false);
  const [newReport, setNewReport] = useState({ disease: '', severity: '', location: '' });

  useEffect(() => {
    // Mock data for demonstration
    setReports([
      { id: 1, disease: 'Diarrhea', severity: 'mild', location: 'Village A', date: '2024-01-15', reporter: 'Dr. Smith' },
      { id: 2, disease: 'Cholera', severity: 'severe', location: 'Village B', date: '2024-01-14', reporter: 'Nurse Jane' },
      { id: 3, disease: 'Typhoid', severity: 'moderate', location: 'Village C', date: '2024-01-13', reporter: 'Health Worker' },
    ]);
  }, []);

  const handleSubmit = () => {
    const report = {
      id: reports.length + 1,
      ...newReport,
      date: new Date().toISOString().split('T')[0],
      reporter: 'Current User'
    };
    setReports([...reports, report]);
    setNewReport({ disease: '', severity: '', location: '' });
    setOpen(false);
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'mild': return 'success';
      case 'moderate': return 'warning';
      case 'severe': return 'error';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" gutterBottom sx={{ color: 'white', mb: 3 }}>
            Health Reports Management
          </Typography>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <LocalHospital sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6">Total Reports</Typography>
              <Typography variant="h3" color="primary">{reports.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <TrendingUp sx={{ fontSize: 40, color: 'secondary.main', mb: 2 }} />
              <Typography variant="h6">This Week</Typography>
              <Typography variant="h3" color="secondary">12</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Severe Cases</Typography>
              <Typography variant="h3" color="error">
                {reports.filter(r => r.severity === 'severe').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Recent Health Reports</Typography>
              <Button
                variant="contained"
                startIcon={<Add />}
                onClick={() => setOpen(true)}
              >
                Add Report
              </Button>
            </div>
            
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Disease</TableCell>
                    <TableCell>Severity</TableCell>
                    <TableCell>Location</TableCell>
                    <TableCell>Date</TableCell>
                    <TableCell>Reporter</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {reports.map((report) => (
                    <TableRow key={report.id}>
                      <TableCell>{report.disease}</TableCell>
                      <TableCell>
                        <Chip
                          label={report.severity}
                          color={getSeverityColor(report.severity)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{report.location}</TableCell>
                      <TableCell>{report.date}</TableCell>
                      <TableCell>{report.reporter}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add New Health Report</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Disease</InputLabel>
                <Select
                  value={newReport.disease}
                  onChange={(e) => setNewReport({...newReport, disease: e.target.value})}
                >
                  <MenuItem value="Diarrhea">Diarrhea</MenuItem>
                  <MenuItem value="Cholera">Cholera</MenuItem>
                  <MenuItem value="Typhoid">Typhoid</MenuItem>
                  <MenuItem value="Hepatitis A">Hepatitis A</MenuItem>
                  <MenuItem value="Dysentery">Dysentery</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Severity</InputLabel>
                <Select
                  value={newReport.severity}
                  onChange={(e) => setNewReport({...newReport, severity: e.target.value})}
                >
                  <MenuItem value="mild">Mild</MenuItem>
                  <MenuItem value="moderate">Moderate</MenuItem>
                  <MenuItem value="severe">Severe</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Location"
                value={newReport.location}
                onChange={(e) => setNewReport({...newReport, location: e.target.value})}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">Submit Report</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default HealthReports;