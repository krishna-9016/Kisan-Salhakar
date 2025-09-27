import React from 'react';
import { Grid, Paper, Typography, Box, Avatar, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button } from '@mui/material';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import PersonIcon from '@mui/icons-material/Person';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import MapIcon from '@mui/icons-material/Map';
import NotificationsIcon from '@mui/icons-material/Notifications';
import './OfficerDashboard.css'; // Make sure the CSS is imported

// --- Mock Data ---
const summaryData = [
    { title: 'Total Farmers', value: '1,250', icon: <PersonIcon /> },
    { title: 'Pending Approvals', value: '15', icon: <CheckCircleIcon /> },
    { title: 'Active Advisories', value: '42', icon: <MapIcon /> },
    { title: 'Calamity Reports', value: '8', icon: <NotificationsIcon /> },
];

const pieData = [{ name: 'Wheat', value: 400 }, { name: 'Rice', value: 300 }, { name: 'Cotton', value: 240 }];
const PIE_COLORS = ['#2e7d32', '#66bb6a', '#a5d6a7'];

const pendingFarmers = [
    { id: '#1245', name: 'Ranjit Singh', district: 'Amritsar', date: '2025-09-11' },
    { id: '#1244', name: 'Priya Sharma', district: 'Patiala', date: '2025-09-11' },
    { id: '#1242', name: 'Amit Kumar', district: 'Jalandhar', date: '2025-09-10' },
];

// --- Sub-components for clarity ---
const SummaryCard = ({ item }) => (
    <Paper className="dashboard-paper-card">
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar className="summary-card-avatar">{item.icon}</Avatar>
            <Box>
                <Typography variant="h4" className="summary-card-value">{item.value}</Typography>
                <Typography color="text.secondary">{item.title}</Typography>
            </Box>
        </Box>
    </Paper>
);

const DashboardHomePage = () => {
    return (
        <Grid container spacing={3}>
            {/* Summary Cards */}
            {summaryData.map(item => (
                <Grid item xs={12} sm={6} md={3} key={item.title}>
                    <SummaryCard item={item} />
                </Grid>
            ))}

            {/* Farmer Approval Queue */}
            <Grid item xs={12} lg={8}>
                <Paper className="dashboard-paper-card">
                    <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>Farmer Approval Queue</Typography>
                    <TableContainer>
                        <Table className="dashboard-table" aria-label="pending approvals table">
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
                                    <TableRow key={farmer.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                        <TableCell>{farmer.id}</TableCell>
                                        <TableCell sx={{ fontWeight: 500 }}>{farmer.name}</TableCell>
                                        <TableCell>{farmer.district}</TableCell>
                                        <TableCell>{farmer.date}</TableCell>
                                        <TableCell align="right">
                                            <Button variant="contained" size="small" sx={{ mr: 1, bgcolor: 'var(--primary-green)' }}>View</Button>
                                            <Button variant="outlined" size="small" color="secondary">Approve</Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Paper>
            </Grid>

            {/* Regional Crop Distribution */}
            <Grid item xs={12} lg={4}>
                <Paper className="dashboard-paper-card">
                    <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>Regional Crop Distribution</Typography>
                    <ResponsiveContainer width="100%" height={280}>
                        <PieChart>
                            <Pie data={pieData} cx="50%" cy="50%" labelLine={false} innerRadius={60} outerRadius={85} dataKey="value">
                                {pieData.map((entry, index) => <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />)}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </Paper>
            </Grid>
        </Grid>
    );
};

export default DashboardHomePage;
