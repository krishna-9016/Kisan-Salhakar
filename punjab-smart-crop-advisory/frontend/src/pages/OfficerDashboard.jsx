import React from 'react';
import {
    AppBar, Toolbar, Typography, Box, Grid, Paper, Avatar, List, ListItem, ListItemText, ListItemAvatar,
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, IconButton, Chip, Divider
} from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import PersonIcon from '@mui/icons-material/Person';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import MapIcon from '@mui/icons-material/Map';
import NotificationsIcon from '@mui/icons-material/Notifications';
import './DashboardPage.css'; // You'll create this CSS file for custom styles

// --- Mock Data (replace with API calls) ---
const summaryData = {
    totalFarmers: 1250,
    pendingApprovals: 15,
    activeAdvisories: 42,
    calamityReports: 8,
};

const cropDistributionData = [
    { name: 'Wheat', value: 400 },
    { name: 'Rice', value: 300 },
    { name: 'Cotton', value: 300 },
    { name: 'Maize', value: 200 },
];
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const recentActivities = [
    { id: 1, user: 'Ranjit Singh', action: 'registered.', timestamp: '5 mins ago', avatar: '/path/to/avatar1.jpg' },
    { id: 2, user: 'System', action: 'sent a weather alert for Ludhiana.', timestamp: '30 mins ago', avatar: null },
    { id: 3, user: 'Gurpreet Kaur', action: 'submitted a crop loss report.', timestamp: '1 hour ago', avatar: '/path/to/avatar2.jpg' },
    { id: 4, user: 'Officer Singh', action: 'approved farmer ID #789.', timestamp: '2 hours ago', avatar: null },
];

const pendingFarmers = [
    { id: '#1245', name: 'Ranjit Singh', district: 'Amritsar', date: '2025-09-11' },
    { id: '#1244', name: 'Priya Sharma', district: 'Patiala', date: '2025-09-11' },
    { id: '#1242', name: 'Amit Kumar', district: 'Jalandhar', date: '2025-09-10' },
];

// --- Main Dashboard Component ---
const OfficerDashboard = () => {
    return (
        <Box className="officer-dashboard">
            {/* Header */}
            <AppBar position="static" color="primary" elevation={0} sx={{ borderBottom: '1px solid #e0e0e0' }}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        Officer Command Center
                    </Typography>
                    <IconButton color="inherit"><NotificationsIcon /></IconButton>
                    <Avatar sx={{ ml: 2, bgcolor: 'secondary.main' }}>OS</Avatar>
                </Toolbar>
            </AppBar>

            {/* Main Content */}
            <Box sx={{ p: 3 }}>
                <Grid container spacing={3}>
                    {/* Summary Cards */}
                    <Grid item xs={12} sm={6} md={3}><SummaryCard title="Total Farmers" value={summaryData.totalFarmers} icon={<PersonIcon />} /></Grid>
                    <Grid item xs={12} sm={6} md={3}><SummaryCard title="Pending Approvals" value={summaryData.pendingApprovals} icon={<CheckCircleIcon />} color="warning.main" /></Grid>
                    <Grid item xs={12} sm={6} md={3}><SummaryCard title="Active Advisories" value={summaryData.activeAdvisories} icon={<MapIcon />} /></Grid>
                    <Grid item xs={12} sm={6} md={3}><SummaryCard title="Calamity Reports" value={summaryData.calamityReports} icon={<NotificationsIcon />} color="error.main" /></Grid>

                    {/* Pending Farmer Approvals Table */}
                    <Grid item xs={12} lg={8}>
                        <Paper className="dashboard-paper" sx={{ p: 2 }}>
                            <Typography variant="h6" gutterBottom>Farmer Approval Queue</Typography>
                            <TableContainer>
                                <Table size="small">
                                    <TableHead>
                                        <TableRow>
                                            <TableCell>Farmer ID</TableCell>
                                            <TableCell>Name</TableCell>
                                            <TableCell>District</TableCell>
                                            <TableCell>Registration Date</TableCell>
                                            <TableCell align="right">Actions</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {pendingFarmers.map((farmer) => (
                                            <TableRow key={farmer.id}>
                                                <TableCell>{farmer.id}</TableCell>
                                                <TableCell>{farmer.name}</TableCell>
                                                <TableCell>{farmer.district}</TableCell>
                                                <TableCell>{farmer.date}</TableCell>
                                                <TableCell align="right">
                                                    <Button variant="contained" size="small" sx={{ mr: 1 }}>View</Button>
                                                    <Button variant="outlined" size="small" color="success">Approve</Button>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </Paper>
                    </Grid>
                    
                    {/* Recent Activities Feed */}
                    <Grid item xs={12} lg={4}>
                        <Paper className="dashboard-paper" sx={{ p: 2 }}>
                            <Typography variant="h6" gutterBottom>Recent Activity</Typography>
                            <List sx={{ width: '100%', bgcolor: 'background.paper' }}>
                                {recentActivities.map((activity, index) => (
                                    <React.Fragment key={activity.id}>
                                        <ListItem alignItems="flex-start">
                                            <ListItemAvatar>
                                                <Avatar>{activity.user.charAt(0)}</Avatar>
                                            </ListItemAvatar>
                                            <ListItemText
                                                primary={activity.user}
                                                secondary={<>{activity.action} <Typography variant="caption" color="text.secondary">{activity.timestamp}</Typography></>}
                                            />
                                        </ListItem>
                                        {index < recentActivities.length - 1 && <Divider variant="inset" component="li" />}
                                    </React.Fragment>
                                ))}
                            </List>
                        </Paper>
                    </Grid>

                    {/* Crop Distribution Chart */}
                    <Grid item xs={12} md={6}>
                         <Paper className="dashboard-paper" sx={{ p: 2, height: 400 }}>
                            <Typography variant="h6" gutterBottom>Regional Crop Distribution</Typography>
                            <ResponsiveContainer>
                                <PieChart>
                                    <Pie data={cropDistributionData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={120} fill="#8884d8" label>
                                        {cropDistributionData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                                    </Pie>
                                    <Tooltip />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                         </Paper>
                    </Grid>
                    
                    {/* Placeholder for another chart or map */}
                    <Grid item xs={12} md={6}>
                        <Paper className="dashboard-paper" sx={{ p: 2, height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
                             <MapIcon color="disabled" sx={{ fontSize: 80, mb: 2 }} />
                             <Typography variant="h6" color="text.secondary">Farmer Distribution Map</Typography>
                             <Typography color="text.secondary">Map component will be integrated here</Typography>
                        </Paper>
                    </Grid>

                </Grid>
            </Box>
        </Box>
    );
};

// Helper component for summary cards
const SummaryCard = ({ title, value, icon, color = 'text.secondary' }) => (
    <Paper className="dashboard-paper summary-card" sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
        <Avatar sx={{ bgcolor: color, mr: 2, width: 56, height: 56 }}>{icon}</Avatar>
        <Box>
            <Typography variant="h4" component="p" sx={{ color: color }}>{value}</Typography>
            <Typography color="text.secondary">{title}</Typography>
        </Box>
    </Paper>
);

export default OfficerDashboard;
