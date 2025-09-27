import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Button } from '@mui/material';
import { logOut } from '../features/auth/authSlice';

const AppBar = () => {
  const { user } = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logOut());
    navigate('/login');
  };

  return (
    <div className="dashboard-header">
      <Typography variant="h6" component="h1" sx={{ color: '#2c3e50' }}>
        Punjab Smart Crop Advisory
      </Typography>
      {user && (
        <Box>
          <Typography component="span" sx={{ marginRight: 2 }}>
            Welcome, {user.name}
          </Typography>
          <Button variant="outlined" onClick={handleLogout}>
            Logout
          </Button>
        </Box>
      )}
    </div>
  );
};

export default AppBar;
