import React, { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import {
    AppBar, Toolbar, IconButton, Typography, Box, CssBaseline, Drawer,
    List, ListItem, ListItemButton, ListItemIcon, ListItemText, Avatar
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Dashboard';
import MapIcon from '@mui/icons-material/Map';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import NotificationsIcon from '@mui/icons-material/Notifications';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import '../pages/OfficerDashboard.css'; // Your final CSS file

const drawerWidth = 260;

const DashboardLayout = () => {
    const [mobileOpen, setMobileOpen] = useState(false);

    const handleDrawerToggle = () => setMobileOpen(!mobileOpen);

    const drawerContent = (
        <div>
            <Toolbar sx={{ justifyContent: 'center' }}>
                <Typography variant="h6" noWrap className="drawer-header">
                    <AgricultureIcon /> Kisan Salahkar
                </Typography>
            </Toolbar>
            <Box sx={{ p: 1 }}>
                <List>
                    <ListItem disablePadding>
                        <ListItemButton component={NavLink} to="/officer" className="drawer-list-item-button" end>
                            <ListItemIcon><HomeIcon /></ListItemIcon>
                            <ListItemText primary="Dashboard" />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component={NavLink} to="/officer/map-plotting" className="drawer-list-item-button">
                            <ListItemIcon><MapIcon /></ListItemIcon>
                            <ListItemText primary="Map Plotting" />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component={NavLink} to="/officer/send-notification" className="drawer-list-item-button">
                            <ListItemIcon><NotificationsIcon /></ListItemIcon>
                            <ListItemText primary="Send Alert" />
                        </ListItemButton>
                    </ListItem>
                     {/* <ListItem disablePadding>
                        <ListItemButton component={NavLink} to="/officer/approvals" className="drawer-list-item-button">
                            <ListItemIcon><PersonAddIcon /></ListItemIcon>
                            <ListItemText primary="Farmer Approvals" />
                        </ListItemButton>
                    </ListItem> */}
                </List>
            </Box>
        </div>
    );

    return (
        <Box className="officer-dashboard-layout">
            <CssBaseline />
            <AppBar position="fixed" className="officer-appbar" sx={{ width: { sm: `calc(100% - ${drawerWidth}px)` }, ml: { sm: `${drawerWidth}px` } }}>
                <Toolbar>
                    <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        edge="start"
                        onClick={handleDrawerToggle}
                        sx={{ mr: 2, display: { sm: 'none' } }}
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
                        Officer Dashboard
                    </Typography>
                    <Avatar sx={{ bgcolor: 'var(--primary-green)' }}>OS</Avatar>
                </Toolbar>
            </AppBar>
            <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
                <Drawer
                    variant="temporary" open={mobileOpen} onClose={handleDrawerToggle}
                    classes={{ paper: 'officer-drawer' }}
                    sx={{ display: { xs: 'block', sm: 'none' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth } }}
                >
                    {drawerContent}
                </Drawer>
                <Drawer
                    variant="permanent"
                    classes={{ paper: 'officer-drawer' }}
                    sx={{ display: { xs: 'none', sm: 'block' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth } }}
                    open
                >
                    {drawerContent}
                </Drawer>
            </Box>
            <Box component="main" className="officer-content-area">
                <Toolbar />
                <Outlet />
            </Box>
        </Box>
    );
};

export default DashboardLayout;
