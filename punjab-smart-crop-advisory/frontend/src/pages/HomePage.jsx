import React, { useState } from 'react';
import { Typography, Button, Box, Menu, MenuItem, useMediaQuery, useTheme } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import FarmerChatbot from '../components/FarmerChatbot';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import './HomePage.css';


const HomePage = () => {
    const navigate = useNavigate();
    const [isChatOpen, setChatOpen] = useState(false);
    const [anchorEl, setAnchorEl] = useState(null);
    const isMenuOpen = Boolean(anchorEl);
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));


    const handleMenuOpen = (event) => {
        setAnchorEl(event.currentTarget);
    };


    const handleMenuClose = () => {
        setAnchorEl(null);
    };


    const handleNavigate = (path) => {
        navigate(path);
        handleMenuClose();
    };


    return (
        <div className="home-page-container">
            <video autoPlay muted loop className="background-video">
                <source src="/farming-video.mp4" type="video/mp4" />
                Your browser does not support the video tag.
            </video>
            <div className="video-overlay"></div>


            <header className="home-header">
                <div className="header-content">
                    <Box sx={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }} onClick={() => navigate('/')}>
                        <AgricultureIcon sx={{ mr: 1 }} />
                        <Typography variant="h5" component="div" sx={{ fontWeight: 'bold' }}>
                            किसान सलाहकार
                        </Typography>
                    </Box>


                    <nav className={isMobile ? 'mobile-nav' : ''}>
                        <Button color="inherit" onClick={() => navigate('/marketplace')}>Marketplace</Button>
                        <Button color="inherit" onClick={() => navigate('/crop-doctor')}>Crop Doctor</Button>
                        <Button color="inherit" onClick={() => navigate('/location-advisory')}>Location Advisory</Button>
                        <Button color="inherit" onClick={() => navigate('/satellite-view')}>Satellite View</Button>
                        
                        <Box
                            onMouseEnter={isMobile ? null : handleMenuOpen}
                            onMouseLeave={isMobile ? null : handleMenuClose}
                            className="login-menu-container"
                        >
                            <Button
                                variant="outlined"
                                color="inherit"
                                onClick={handleMenuOpen}
                                aria-controls={isMenuOpen ? 'login-menu' : undefined}
                                aria-haspopup="true"
                                aria-expanded={isMenuOpen ? 'true' : undefined}
                            >
                                Login
                            </Button>
                            <Menu
                                id="login-menu"
                                anchorEl={anchorEl}
                                open={isMenuOpen}
                                onClose={handleMenuClose}
                                MenuListProps={{ onMouseLeave: handleMenuClose }}
                            >
                                <MenuItem onClick={() => handleNavigate('/farmer-login')}>Farmer Login</MenuItem>
                                <MenuItem onClick={() => handleNavigate('/officer-login')}>Officer Login</MenuItem>
                                {/* --- THIS IS THE NEWLY ADDED LINE --- */}
                                <MenuItem onClick={() => handleNavigate('/buyer-login')}>Buyer Login</MenuItem>
                            </Menu>
                        </Box>
                    </nav>
                </div>
            </header>


            <main className="home-main-content">
                <Typography variant="h2" component="h1" className="main-title">
                    Modern Farming, Timeless Tradition
                </Typography>
                <Typography variant="h5" className="main-subtitle">
                    Instant, AI-powered advice for the farmers of Punjab. Right here, right now.
                </Typography>
            </main>


            <Box className="chatbot-area">
                {isChatOpen && <FarmerChatbot />}
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => setChatOpen(!isChatOpen)}
                    className="chatbot-toggle-button"
                >
                    {isChatOpen ? 'Close Chat' : 'Chat with AgriBot'}
                </Button>
            </Box>
        </div>
    );
};


export default HomePage;
