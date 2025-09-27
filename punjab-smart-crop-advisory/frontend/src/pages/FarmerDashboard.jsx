import React, { useState } from 'react';
import { Box, Paper, BottomNavigation, BottomNavigationAction, Typography, Button } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { logOut } from '../features/auth/authSlice';

import ChatPanel from '../components/farmer-dashboard/ChatPanel';
import WeatherPanel from '../components/farmer-dashboard/WeatherPanel';
import MarketPanel from '../components/farmer-dashboard/MarketPanel';
import SellPanel from '../components/farmer-dashboard/SellPanel';
import ChatIcon from '@mui/icons-material/Chat';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import StorefrontIcon from '@mui/icons-material/Storefront';
import SellIcon from '@mui/icons-material/Sell';
import LogoutIcon from '@mui/icons-material/Logout';

const FarmerDashboard = () => {
  const [value, setValue] = useState(0);
  const { user } = useSelector((state) => state.auth);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(logOut());
    navigate('/', { replace: true });
  };

  const renderPanel = () => {
    switch (value) {
      case 0: return <ChatPanel />;
      case 1: return <WeatherPanel />;
      case 2: return <MarketPanel />;
      case 3: return <SellPanel />;
      default: return <ChatPanel />;
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', bgcolor: 'background.default' }}>
      <Paper sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }} elevation={2}>
        <Typography variant="h6">Welcome, {user?.name || 'Farmer'}</Typography>
        <Button startIcon={<LogoutIcon />} onClick={handleLogout} color="primary">Logout</Button>
      </Paper>
      
      <Box sx={{ flexGrow: 1, overflowY: 'auto' }}>{renderPanel()}</Box>
      
      <Paper sx={{ position: 'sticky', bottom: 0, left: 0, right: 0 }} elevation={3}>
        <BottomNavigation showLabels value={value} onChange={(e, val) => setValue(val)}>
          <BottomNavigationAction label="Chat" icon={<ChatIcon />} />
          <BottomNavigationAction label="Weather" icon={<WbSunnyIcon />} />
          <BottomNavigationAction label="Market" icon={<StorefrontIcon />} />
          <BottomNavigationAction label="Sell Produce" icon={<SellIcon />} />
        </BottomNavigation>
      </Paper>
    </Box>
  );
};

export default FarmerDashboard;
