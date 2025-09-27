import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, Container, Paper, CircularProgress, Alert, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './SatelliteViewPage.css'; // New dedicated CSS file

const SatelliteViewPage = () => {
  const navigate = useNavigate();
  const [location, setLocation] = useState(null);
  const [locationError, setLocationError] = useState('');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);

  // --- Get User's Location on Page Load ---
  useEffect(() => {
    if (!navigator.geolocation) {
      setLocationError("Geolocation is not supported by your browser.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        });
        setLocationError('');
      },
      () => {
        setLocationError("Unable to retrieve your location. Please enable location permissions in your browser settings.");
      }
    );
  }, []);

  const handleFetchReport = () => {
    if (!location) return;
    setLoading(true);
    setReport(null);

    setTimeout(() => {
      setReport({
        period: "June 1, 2025 - August 31, 2025",
        vegetationIndex: {
          value: "0.78 (Healthy)",
          trend: "Increased by 15% over the period, indicating strong crop growth.",
        },
        waterStress: {
          value: "Low",
          trend: "Consistent water levels detected, with two significant irrigation events noted in early July and mid-August.",
        },
        summary: "The field has shown robust and healthy growth over the last 3 months. The vegetation density peaked in late August. No significant stress or anomalies were detected from the satellite imagery.",
      });
      setLoading(false);
    }, 2500); 
  };

  return (
    <div className="satellite-view-container">
      <header className="satellite-header">
        <Typography variant="h4" component="h1">Satellite Field Analysis</Typography>
        <Button variant="outlined" onClick={() => navigate('/')}>Back to Home</Button>
      </header>

      <Container maxWidth="md" className="satellite-main">
        <Paper elevation={3} className="location-display-panel">
          <Typography variant="h5" gutterBottom>Your Current Location</Typography>
          {location && (
            <Typography variant="h6" color="primary">
              Lat: {location.lat.toFixed(4)}, Lon: {location.lon.toFixed(4)}
            </Typography>
          )}
          {locationError && <Alert severity="error">{locationError}</Alert>}
          {!location && !locationError && <CircularProgress />}
          {location && (
            <Button
              variant="contained"
              size="large"
              onClick={handleFetchReport}
              disabled={loading}
              sx={{ mt: 2 }}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : 'Get 3-Month Field Report'}
            </Button>
          )}
        </Paper>

        {report && (
          <Paper elevation={3} className="report-panel">
            <Typography variant="h5" gutterBottom>Field History Report</Typography>
            <Typography variant="subtitle1" color="textSecondary" gutterBottom>
              Analysis Period: {report.period}
            </Typography>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <Typography variant="h6">Vegetation Index (NDVI)</Typography>
                <Typography className="report-value">{report.vegetationIndex.value}</Typography>
                <Typography>{report.vegetationIndex.trend}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="h6">Water Stress Index</Typography>
                <Typography className="report-value">{report.waterStress.value}</Typography>
                <Typography>{report.waterStress.trend}</Typography>
              </Grid>
              <Grid item xs={12} sx={{ mt: 2 }}>
                <Typography variant="h6">Summary of Activity</Typography>
                <Typography>{report.summary}</Typography>
              </Grid>
            </Grid>
          </Paper>
        )}
      </Container>
    </div>
  );
};

export default SatelliteViewPage;
