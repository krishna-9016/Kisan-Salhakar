import React, { useState } from 'react';
import { Box, Typography, Button, Container, Paper, TextField, CircularProgress, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const FarmerLoginPage = () => {
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSendOtp = async (e) => {
    e.preventDefault();
    if (!/^\d{10}$/.test(phone)) {
      setError("Please enter a valid 10-digit phone number.");
      return;
    }
    setLoading(true);
    setError('');
    
    await new Promise(res => setTimeout(res, 1000));
    
    navigate('/verify-otp', { state: { phone: phone } });
  };

  return (
    <div className="login-container">
      <div className="login-art-panel">
        <Typography variant="h2" component="h1" className="main-title-login">Farmer Portal</Typography>
        <Typography variant="h6" className="subtitle-login">Empowering Punjab's Agriculture.</Typography>
      </div>
      <div className="login-form-panel">
        <Paper component="form" onSubmit={handleSendOtp} className="form-box" elevation={12}>
          <Typography variant="h5" sx={{ mb: 1, fontWeight: 'bold' }}>Kisan Login</Typography>
          <Typography color="text.secondary" paragraph>Enter your mobile number to get a verification code.</Typography>
          <TextField fullWidth required margin="normal" id="phone" label="10-Digit Mobile Number" value={phone} onChange={e => setPhone(e.target.value)} variant="filled" />
          {error && <Alert severity="error" sx={{ mt: 1 }}>{error}</Alert>}
          <Button type="submit" fullWidth variant="contained" className="login-button" sx={{ mt: 2 }} disabled={loading}>
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Send Verification Code'}
          </Button>
        </Paper>
      </div>
    </div>
  );
};

export default FarmerLoginPage;
