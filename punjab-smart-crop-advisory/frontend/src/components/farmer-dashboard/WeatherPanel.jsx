import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import CloudQueueIcon from '@mui/icons-material/CloudQueue';
import GrainIcon from '@mui/icons-material/Grain';

// This is simulated data. In a real app, this would come from your FastAPI backend.
const weatherData = {
  current: { temp: 34, condition: 'Sunny', humidity: 65, wind: 12 },
  forecast: [
    { day: 'Tomorrow', temp: 35, condition: 'Sunny', icon: <WbSunnyIcon sx={{ fontSize: 32 }} /> },
    { day: 'Wed', temp: 36, condition: 'Partly Cloudy', icon: <CloudQueueIcon sx={{ fontSize: 32 }} /> },
    { day: 'Thu', temp: 33, condition: 'Light Rain', icon: <GrainIcon sx={{ fontSize: 32 }} /> },
  ],
};

const WeatherPanel = () => {
  return (
    <Box sx={{ p: { xs: 2, md: 3 } }}>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
        Hyperlocal Weather Forecast
      </Typography>
      <Paper 
        elevation={4} 
        sx={{ 
          p: 3, 
          borderRadius: 3, 
          mb: 4,
          background: 'linear-gradient(to right, #6dd5ed, #2193b0)', 
          color: 'white' 
        }}
      >
        <Grid container alignItems="center">
          <Grid item xs={7}>
            <Typography variant="h2" sx={{ fontWeight: 'bold' }}>
              {weatherData.current.temp}°C
            </Typography>
            <Typography variant="h6">
              {weatherData.current.condition}
            </Typography>
          </Grid>
          <Grid item xs={5} sx={{ textAlign: 'center' }}>
            <WbSunnyIcon sx={{ fontSize: 60, opacity: 0.8 }} />
          </Grid>
        </Grid>
        <Grid container sx={{ mt: 2 }}>
            <Grid item xs={6}><Typography>Humidity: {weatherData.current.humidity}%</Typography></Grid>
            <Grid item xs={6}><Typography>Wind: {weatherData.current.wind} km/h</Typography></Grid>
        </Grid>
      </Paper>

      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
        Next 3 Days
      </Typography>
      <Grid container spacing={2}>
        {weatherData.forecast.map((day) => (
          <Grid item xs={12} sm={4} key={day.day}>
            <Paper sx={{ p: 2, textAlign: 'center', borderRadius: 2 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>{day.day}</Typography>
              {day.icon}
              <Typography variant="h6">{day.temp}°C</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default WeatherPanel;
