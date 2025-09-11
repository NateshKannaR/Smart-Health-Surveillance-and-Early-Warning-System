import React from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Container, 
  Paper,
  Alert,
  AlertTitle
} from '@mui/material';
import { 
  ErrorOutline, 
  Refresh 
} from '@mui/icons-material';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Container maxWidth="md" sx={{ mt: 8 }}>
          <Paper 
            sx={{ 
              p: 4, 
              textAlign: 'center',
              border: '1px solid',
              borderColor: 'error.light'
            }}
          >
            <Box sx={{ mb: 3 }}>
              <ErrorOutline 
                sx={{ 
                  fontSize: 64, 
                  color: 'error.main',
                  mb: 2
                }} 
              />
              <Typography 
                variant="h4" 
                sx={{ 
                  fontWeight: 700,
                  color: 'text.primary',
                  mb: 2
                }}
              >
                Something went wrong
              </Typography>
              <Typography 
                variant="body1" 
                color="text.secondary"
                sx={{ mb: 3, maxWidth: 500, mx: 'auto' }}
              >
                We encountered an unexpected error while loading the Health Surveillance System. 
                Please try refreshing the page or contact support if the problem persists.
              </Typography>
            </Box>

            <Alert severity="error" sx={{ mb: 3, textAlign: 'left' }}>
              <AlertTitle>Error Details</AlertTitle>
              {this.state.error?.message || 'An unexpected error occurred'}
            </Alert>

            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button
                variant="contained"
                startIcon={<Refresh />}
                onClick={this.handleRetry}
                sx={{ fontWeight: 600 }}
              >
                Retry
              </Button>
              <Button
                variant="outlined"
                onClick={() => window.location.href = '/'}
                sx={{ fontWeight: 600 }}
              >
                Go to Home
              </Button>
            </Box>
          </Paper>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;