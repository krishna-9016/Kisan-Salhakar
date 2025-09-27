import React, { useState } from 'react';
import { Box, Typography, Paper, TextField, Button, Alert, Grid } from '@mui/material';

// 1. Initial static data to start with
const initialListings = [
  { id: 1, produceName: "Basmati Rice (Sample)", quantity: 500, pricePerKg: 120 },
  { id: 2, produceName: "Organic Wheat (Sample)", quantity: 1000, pricePerKg: 35 },
];

const MarketPanel = () => {
    // State for the form inputs
    const [produceName, setProduceName] = useState('');
    const [quantity, setQuantity] = useState('');
    const [pricePerKg, setPricePerKg] = useState('');
    
    // State to show success/error messages
    const [success, setSuccess] = useState('');
    
    // 2. Local state to hold the list of produce, initialized with our static data
    const [listings, setListings] = useState(initialListings);

    // 3. Simplified handleSubmit function that only works with local state
    const handleSubmit = (e) => {
        e.preventDefault();
        
        // Basic validation
        if (!produceName || !quantity || !pricePerKg) {
            return;
        }

        // Create a new listing object
        const newListing = {
            id: Date.now(), // Use a timestamp for a unique key
            produceName,
            quantity: parseFloat(quantity),
            pricePerKg: parseFloat(pricePerKg),
        };

        // Add the new listing to our local array
        setListings(prevListings => [newListing, ...prevListings]);

        setSuccess(`Successfully added "${produceName}" to the list!`);

        // Clear the form fields
        setProduceName('');
        setQuantity('');
        setPricePerKg('');
    };

    return (
        <Box sx={{ p: { xs: 2, md: 3 } }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
                List Your Produce for Sale (Demo Mode)
            </Typography>

            {/* --- The Form to Add New Items --- */}
            <Paper component="form" onSubmit={handleSubmit} elevation={3} sx={{ p: 3, borderRadius: 2, mb: 4 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>New Marketplace Listing</Typography>
                <TextField
                    label="Produce Name (e.g., Basmati Rice)"
                    fullWidth
                    required
                    value={produceName}
                    onChange={(e) => setProduceName(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <TextField
                    label="Quantity (in kg)"
                    type="number"
                    fullWidth
                    required
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <TextField
                    label="Price per kg (in ₹)"
                    type="number"
                    fullWidth
                    required
                    value={pricePerKg}
                    onChange={(e) => setPricePerKg(e.target.value)}
                    sx={{ mb: 2 }}
                />
                <Button type="submit" variant="contained" fullWidth>
                    Add to Local List
                </Button>
                {success && <Alert severity="success" sx={{ mt: 2 }} onClose={() => setSuccess('')}>{success}</Alert>}
            </Paper>

            {/* --- The Display of Current Listings --- */}
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
                Current Listings
            </Typography>
            <Grid container spacing={3}>
                {listings.map((item) => (
                    <Grid item xs={12} sm={6} md={4} key={item.id}>
                        <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
                            <Typography variant="h6">{item.produceName}</Typography>
                            <Typography color="text.secondary">Available: {item.quantity} kg</Typography>
                            <Typography sx={{ fontWeight: 'bold', mt: 1 }}>
                                ₹{item.pricePerKg.toLocaleString('en-IN')} / kg
                            </Typography>
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default MarketPanel;
