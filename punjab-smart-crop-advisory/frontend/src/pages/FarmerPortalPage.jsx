import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import FarmerChatbot from '../components/FarmerChatbot.jsx';
import './FarmerPortalPage.css';

const FarmerPortalPage = () => {
  return (
    <div className="farmer-portal-container">
      <Box className="farmer-portal-content">
        <Typography variant="h4" gutterBottom align="center">
          Farmer Advisory Portal
        </Typography>
        <FarmerChatbot />
      </Box>
    </div>
  );
};

export default FarmerPortalPage;
