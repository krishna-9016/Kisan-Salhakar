import React, { useState } from 'react';
import { Box, Typography, Button, Paper, TextField } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../features/auth/authSlice'; // Ensure this path is correct
import './LoginPage.css';

const OfficerLoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const handlePrototypeLogin = (e) => {
        e.preventDefault();
        
        const officerUser = { name: 'Officer Krishna', email: email || 'officer@gov.in', role: 'officer' };
        const dummyToken = 'prototype-officer-jwt-token';
        
        dispatch(setCredentials({ user: officerUser, token: dummyToken }));
        
        // --- THIS IS THE FIX ---
        navigate('/officer'); 
        // -----------------------
    };

    return (
        <div className="login-container">
            <div className="login-art-panel">
                <Typography variant="h2" component="h1" className="main-title-login">Official Portal</Typography>
                <Typography variant="h6" className="subtitle-login">Punjab Smart Crop Advisory</Typography>
            </div>
            <div className="login-form-panel">
                <Paper component="form" onSubmit={handlePrototypeLogin} className="form-box" elevation={12}>
                    <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>Officer Login (Prototype)</Typography>
                    <TextField 
                        fullWidth 
                        margin="normal" 
                        label="Enter email" 
                        value={email} 
                        onChange={e => setEmail(e.target.value)} 
                        variant="filled" 
                    />
                    <TextField 
                        fullWidth 
                        margin="normal" 
                        label="Enter password" 
                        type="password" 
                        value={password} 
                        onChange={e => setPassword(e.target.value)} 
                        variant="filled" 
                    />
                    <Button type="submit" fullWidth variant="contained" className="login-button" sx={{ mt: 2 }}>
                        Login
                    </Button>
                    <Button 
                        fullWidth 
                        variant="outlined" 
                        color="secondary" 
                        sx={{ mt: 2 }} 
                        onClick={() => navigate('/')}
                    >
                        Back to Home
                    </Button>
                </Paper>
            </div>
        </div>
    );
};

export default OfficerLoginPage;
