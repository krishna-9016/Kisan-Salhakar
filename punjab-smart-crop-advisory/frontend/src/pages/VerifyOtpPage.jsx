import React, { useState, useEffect } from 'react';
import { Box, Typography, Button, Paper, TextField, CircularProgress } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../features/auth/authSlice';
import './LoginPage.css'; // We will still use the beautiful styles

const VerifyOtpPage = () => {
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const location = useLocation();
  
  const phone = location.state?.phone;

  useEffect(() => {
    if (!phone) {
      navigate('/farmer-login'); 
    }
  }, [phone, navigate]);
  
  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    setLoading(true);

    // No validation! Just a short delay.
    await new Promise(res => setTimeout(res, 500));
    
    // --- THIS IS THE DUMMY LOGIN ---
    // It accepts any input and logs the user in.
    const dummyUser = { name: "Sample Farmer", phone: phone, role: "farmer" };
    const dummyToken = "dummy-farmer-jwt-token";
    dispatch(setCredentials({ user: dummyUser, token: dummyToken }));
    
    // Navigate to the dashboard
    navigate('/farmer-dashboard');
  };

  return (
    <div className="login-container">
       <div className="login-art-panel">
        <Typography variant="h2" component="h1" className="main-title-login">Verify Login</Typography>
        <Typography variant="h6" className="subtitle-login">Prototype Mode</Typography>
      </div>
      <div className="login-form-panel">
        <Paper component="form" onSubmit={handleVerifyOtp} className="form-box" elevation={12}>
          <Typography variant="h5" sx={{ mb: 1 }}>Final Step</Typography>
          <Typography color="text.secondary" paragraph>Click verify to continue</Typography>
          
          {/* A simple text field instead of the complex OTP input */}
          <TextField 
            fullWidth 
            margin="normal" 
            label="Enter the Otp" 
            value={otp} 
            onChange={e => setOtp(e.target.value)} 
            variant="filled" 
          />
          
          <Button type="submit" fullWidth variant="contained" className="login-button" sx={{ mt: 2 }} disabled={loading}>
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Verify & Enter'}
          </Button>
        </Paper>
      </div>
    </div>
  );
};

export default VerifyOtpPage;
