// The complete code for: frontend/src/pages/MarketplacePage.jsx

import React, { useState } from 'react';
import { 
    Box, Typography, Container, Paper, Grid, TextField, 
    Card, CardContent, CardActions, Button, Alert 
} from '@mui/material';

// Initial static data for the marketplace listings with the typo corrected
const initialListings = [
  { id: 'prod-1', produceName: "Basmati Rice (Ludhiana)", quantity: 500, pricePerKg: 120 },
  { id: 'prod-2', produceName: "Organic Wheat (Amritsar)", quantity: 1000, pricePerKg: 35 },
  { id: 'prod-3', produceName: "Sugarcane (Jalandhar)", quantity: 2500, pricePerKg: 4 },
  // --- THIS IS THE CORRECTED LINE ---
  { id: 'prod-4', produceName: "Cotton (Bathinda)", quantity: 800, pricePerKg: 60 },
  { id: 'prod-5', produceName: "Maize (Hoshiarpur)", quantity: 1200, pricePerKg: 20 },
];

const MarketplacePage = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [success, setSuccess] = useState('');
    const [listings, setListings] = useState(initialListings);
    
    const handlePurchase = (orderId, produceName) => {
        setSuccess(`Purchase initiated for "${produceName}"! This would be tracked in your active orders.`);
        setListings(prevListings => prevListings.filter(item => item.id !== orderId));
    };

    const filteredListings = listings.filter(item =>
        // Added a check to prevent errors if produceName is missing
        item.produceName && item.produceName.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <Box sx={{ minHeight: '100vh', background: '#f4f6f8' }}>
            <Container maxWidth="lg" sx={{ py: 4 }}>
                <Typography variant="h4" sx={{ mb: 2, fontWeight: 'bold' }}>
                    Produce Marketplace
                </Typography>
                <TextField
                    fullWidth
                    label="Search by Crop Name"
                    variant="outlined"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    sx={{ mb: 4, background: 'white' }}
                />

                {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>{success}</Alert>}
                
                {filteredListings.length === 0 && (
                    <Paper sx={{p: 4, textAlign: 'center'}}>
                        <Typography variant="h6">No More Listings Available</Typography>
                        <Typography color="text.secondary">All available produce has been purchased or your search returned no results.</Typography>
                    </Paper>
                )}

                <Grid container spacing={3}>
                    {filteredListings.map((item) => (
                        <Grid item xs={12} sm={6} md={4} key={item.id}>
                            <Card sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                                <CardContent sx={{ flexGrow: 1 }}>
                                    <Typography variant="h6" component="div">{item.produceName}</Typography>
                                    <Typography sx={{ mt: 2, fontWeight: 'bold', fontSize: '1.2rem' }}>
                                        ₹{item.pricePerKg.toLocaleString('en-IN')} / kg
                                    </Typography>
                                    <Typography>Available: {item.quantity} kg</Typography>
                                </CardContent>
                                <CardActions>
                                    <Button 
                                        size="small" 
                                        variant="contained" 
                                        fullWidth
                                        onClick={() => handlePurchase(item.id, item.produceName)}
                                    >
                                        Initiate Purchase
                                    </Button>
                                </CardActions>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Container>
        </Box>
    );
};

export default MarketplacePage;
