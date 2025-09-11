import React from 'react';
import { Box, CircularProgress, Typography, Container } from '@mui/material';
import { LocalHospital } from '@mui/icons-material';

const LoadingScreen = ({ message = 'Loading...' }) => {
  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
          textAlign: 'center',
          gap: 3
        }}
      >
        <Box
          sx={{
            position: 'relative',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <CircularProgress
            size={80}
            thickness={3}
            sx={{
              color: 'primary.main',
              animationDuration: '1.5s'
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 80,
              height: 80
            }}
          >
            <LocalHospital
              sx={{
                fontSize: 32,
                color: 'primary.main'
              }}
            />
          </Box>
        </Box>
        
        <Box>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 600,
              color: 'text.primary',
              mb: 1
            }}
          >
            {message}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ fontWeight: 500 }}
          >
            Please wait while we load your health surveillance data
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default LoadingScreen;