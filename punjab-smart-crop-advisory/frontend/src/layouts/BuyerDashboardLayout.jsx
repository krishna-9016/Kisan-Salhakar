import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { Link, Outlet, useNavigate } from 'react-router-dom';

const BuyerDashboardLayout = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('buyerToken');
    navigate('/buyer-login');
  };

  return (
    <Box sx={{ display: 'flex' }}>
      {/* Sidebar Navigation */}
      <Paper elevation={3} sx={{ width: 250, height: '100vh', p: 2, display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
          Buyer Portal
        </Typography>
        <Button component={Link} to="/buyer/marketplace" fullWidth sx={{ mb: 1, justifyContent: 'flex-start' }}>
          Marketplace
        </Button>
        <Button component={Link} to="/buyer/active-orders" fullWidth sx={{ mb: 1, justifyContent: 'flex-start' }}>
          Active Orders
        </Button>
        {/* Spacer to push logout to the bottom */}
        <Box sx={{ flexGrow: 1 }} />
        <Button variant="outlined" color="error" onClick={handleLogout} fullWidth>
          Logout
        </Button>
      </Paper>

      {/* Main Content Area */}
      <Box component="main" sx={{ flexGrow: 1, p: 3, background: '#f4f6f8' }}>
        <Outlet /> {/* This is where MarketplacePage and ActiveOrdersPage will render */}
      </Box>
    </Box>
  );
};

export default BuyerDashboardLayout;
