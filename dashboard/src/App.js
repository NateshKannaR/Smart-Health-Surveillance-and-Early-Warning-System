import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import HealthReports from './pages/HealthReports';
import WaterQuality from './pages/WaterQuality';
import Alerts from './pages/Alerts';
import Predictions from './pages/Predictions';
import Maps from './pages/Maps';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00E676',
    },
    secondary: {
      main: '#FF4081',
    },
    background: {
      default: '#0a0e27',
      paper: 'rgba(30, 41, 59, 0.8)',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b0bec5',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9))',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9))',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App" style={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #0c1445 0%, #1a237e 50%, #000051 100%)',
          backgroundAttachment: 'fixed'
        }}>
          <Navbar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/health-reports" element={<HealthReports />} />
            <Route path="/water-quality" element={<WaterQuality />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/maps" element={<Maps />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;