import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, TextField, Button, Paper, Alert } from '@mui/material';
import axios from 'axios';
import './BuyerLoginPage.css'; // Make sure you have created this CSS file

const BuyerLoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const { data } = await axios.post('http://localhost:5000/api/v1/auth/login-buyer', {
                email,
                password,
            });
            
            localStorage.setItem('buyerToken', data.token);
            navigate('/buyer/marketplace');

        } catch (err) {
            setError(err.response?.data?.message || 'Login failed. Please try again.');
        }
    };

    return (
        <div className="login-container">
            <div className="login-art-panel">
                <Typography variant="h1" className="main-title-login">
                    Access the <br />Future of Produce.
                </Typography>
                <Typography variant="h5" className="subtitle-login">
                    Directly connect with farmers and source with confidence.
                </Typography>
            </div>
            <div className="login-form-panel">
                <Paper className="form-box" elevation={0}>
                    <Typography component="h1" variant="h4" sx={{ fontWeight: '700', mb: 1 }}>
                        Buyer Portal
                    </Typography>
                    <Typography color="text.secondary" sx={{ mb: 3 }}>
                        Sign in to access the marketplace.
                    </Typography>
                    <Box component="form" onSubmit={handleLogin}>
                        {error && <Alert severity="error" sx={{ width: '100%', mb: 2 }}>{error}</Alert>}
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoFocus
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            className="login-button"
                            sx={{ mt: 2 }}
                        >
                            Sign In
                        </Button>
                    </Box>
                </Paper>
            </div>
        </div>
    );
};

export default BuyerLoginPage;
