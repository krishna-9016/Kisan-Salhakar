import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import axios from 'axios';
import { 
    Paper, Typography, FormControl, InputLabel, Select, MenuItem, 
    Box, Button, TextField, CircularProgress, Alert 
} from '@mui/material';

const punjabDistricts = ["Amritsar", "Ludhiana", "Jalandhar", "Patiala", "Bathinda"];

const SendNotificationPage = () => {
    const [selectedDistrict, setSelectedDistrict] = useState('');
    const [weatherData, setWeatherData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [message, setMessage] = useState('');
    const { token } = useSelector((state) => state.auth);

    const handleDistrictChange = async (district) => {
        setSelectedDistrict(district);
        setWeatherData(null);
        setError('');
        setSuccess('');
        if (!district) return;

        try {
            setLoading(true);
            const response = await axios.get(`http://localhost:5000/api/v1/weather/${district}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setWeatherData(response.data);
        } catch (err) {
            setError(`Could not fetch weather for ${district}.`);
        } finally {
            setLoading(false);
        }
    };
    
    const handleSendAlert = async () => {
        if (!message || !selectedDistrict) {
            alert('Please select a district and write a message.');
            return;
        }
        setLoading(true);
        setError('');
        setSuccess('');

        try {
            const response = await axios.post(
                'http://localhost:5000/api/v1/notifications/send',
                { district: selectedDistrict, message: message },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setSuccess(response.data.message || 'Alerts sent successfully!');
            setMessage('');
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to send the alert.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Paper className="dashboard-paper-card">
            <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                Weather Alerts & Notifications
            </Typography>
            <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>Select District</InputLabel>
                <Select
                    value={selectedDistrict}
                    label="Select District"
                    onChange={(e) => handleDistrictChange(e.target.value)}
                >
                    {punjabDistricts.map(d => <MenuItem key={d} value={d}>{d}</MenuItem>)}
                </Select>
            </FormControl>

            {loading && <CircularProgress sx={{ mb: 2 }} />}
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
            {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

            {weatherData && (
                <Box sx={{ mb: 3, p: 2, backgroundColor: '#f7f9fc', borderRadius: '8px' }}>
                    <Typography variant="h6" sx={{ mb: 1 }}>Current Weather in {weatherData.name}</Typography>
                    <Typography><b>Temperature:</b> {weatherData.main.temp}°C</Typography>
                    <Typography><b>Condition:</b> {weatherData.weather[0].description}</Typography>
                    <Typography><b>Humidity:</b> {weatherData.main.humidity}%</Typography>
                </Box>
            )}

            <TextField
                label="Alert Message"
                multiline
                rows={4}
                fullWidth
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="e.g., Heavy rainfall expected. Farmers are advised to take necessary precautions."
                sx={{ mb: 2 }}
                disabled={loading}
            />

            <Button 
                variant="contained" 
                size="large"
                onClick={handleSendAlert}
                disabled={!selectedDistrict || !message || loading}
            >
                {loading ? 'Sending...' : 'Send Alert to Farmers'}
            </Button>
        </Paper>
    );
};

export default SendNotificationPage;
