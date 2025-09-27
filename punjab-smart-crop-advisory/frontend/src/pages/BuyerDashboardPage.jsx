import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { Link, Outlet } from 'react-router-dom'; // Outlet will render nested routes

const BuyerDashboardLayout = () => {
  return (
    <Box sx={{ display: 'flex' }}>
      {/* Sidebar */}
      <Box sx={{ width: 240, p: 2, borderRight: '1px solid #ddd' }}>
        <Typography variant="h5" gutterBottom>Buyer Portal</Typography>
        <Button component={Link} to="/buyer/marketplace" fullWidth sx={{ mb: 1 }}>Marketplace</Button>
        <Button component={Link} to="/buyer/active-orders" fullWidth sx={{ mb: 1 }}>Active Orders</Button>
        <Button component={Link} to="/buyer/order-history" fullWidth>Order History</Button>
      </Box>

      {/* Main Content */}
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Outlet /> {/* Nested pages will render here */}
      </Box>
    </Box>
  );
};

export default BuyerDashboardLayout;
