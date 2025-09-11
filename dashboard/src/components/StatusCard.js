import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat
} from '@mui/icons-material';

const StatusCard = ({ 
  title, 
  value, 
  subtitle, 
  icon, 
  color = 'primary.main',
  trend,
  progress,
  status,
  variant = 'default'
}) => {
  const getTrendIcon = (trendValue) => {
    if (trendValue > 0) return <TrendingUp sx={{ fontSize: 16 }} />;
    if (trendValue < 0) return <TrendingDown sx={{ fontSize: 16 }} />;
    return <TrendingFlat sx={{ fontSize: 16 }} />;
  };

  const getTrendColor = (trendValue) => {
    if (trendValue > 0) return 'success.main';
    if (trendValue < 0) return 'error.main';
    return 'text.secondary';
  };

  return (
    <Card 
      sx={{ 
        height: '100%',
        position: 'relative',
        overflow: 'visible',
        transition: 'all 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: 3
        },
        '&::before': variant === 'accent' ? {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 4,
          background: color,
          borderRadius: '12px 12px 0 0'
        } : {}
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box sx={{ flex: 1 }}>
            <Typography 
              variant="body2" 
              color="text.secondary"
              sx={{ 
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                fontSize: '0.75rem',
                mb: 1
              }}
            >
              {title}
            </Typography>
            <Typography 
              variant="h3" 
              sx={{ 
                fontWeight: 700,
                color: 'text.primary',
                lineHeight: 1,
                mb: 1
              }}
            >
              {value}
            </Typography>
          </Box>
          
          {icon && (
            <Box sx={{ 
              p: 1.5, 
              borderRadius: 2, 
              backgroundColor: `${color}15`,
              color: color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              {icon}
            </Box>
          )}
        </Box>

        {subtitle && (
          <Typography 
            variant="body2" 
            color="text.secondary"
            sx={{ fontWeight: 500, mb: 1 }}
          >
            {subtitle}
          </Typography>
        )}

        {progress !== undefined && (
          <Box sx={{ mb: 2 }}>
            <LinearProgress 
              variant="determinate" 
              value={progress} 
              sx={{ 
                height: 6, 
                borderRadius: 3,
                backgroundColor: 'grey.200',
                '& .MuiLinearProgress-bar': {
                  backgroundColor: color
                }
              }}
            />
            <Typography 
              variant="caption" 
              color="text.secondary"
              sx={{ mt: 0.5, display: 'block' }}
            >
              {progress}% Complete
            </Typography>
          </Box>
        )}

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {trend !== undefined && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <Box sx={{ color: getTrendColor(trend), display: 'flex', alignItems: 'center' }}>
                {getTrendIcon(trend)}
              </Box>
              <Typography 
                variant="body2" 
                sx={{ 
                  color: getTrendColor(trend),
                  fontWeight: 600
                }}
              >
                {trend > 0 ? '+' : ''}{trend}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                vs last period
              </Typography>
            </Box>
          )}

          {status && (
            <Chip 
              label={status} 
              size="small"
              color={status === 'Active' ? 'success' : status === 'Warning' ? 'warning' : 'default'}
              variant="outlined"
              sx={{ fontWeight: 600, fontSize: '0.7rem' }}
            />
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatusCard;