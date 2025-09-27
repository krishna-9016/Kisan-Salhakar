import React, { useState } from 'react';
import { Box, Typography, Paper, TextField, Button, Grid, CircularProgress } from '@mui/material';

const SellPanel = () => {
  const [cropName, setCropName] = useState('');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleSubmitListing = async () => {
    if (!cropName || !quantity || !price) {
      alert("Please fill in all fields.");
      return;
    }
    setLoading(true);

    // --- Blockchain & Backend Simulation ---
    // In a real application, this is the point where you would:
    // 1. Upload the files (proof of harvest) to a decentralized storage like IPFS.
    // 2. Call a function on your smart contract to create a new "Produce" asset,
    //    storing the IPFS hashes, crop name, quantity, and price.
    //    This would require the user to sign the transaction with their wallet (e.g., MetaMask).
    
    console.log("Creating listing for:", { cropName, quantity, price, files });
    
    // Simulate the process
    setTimeout(() => {
      alert(`Your ${cropName} has been successfully listed on the marketplace!`);
      // Clear the form
      setCropName('');
      setQuantity('');
      setPrice('');
      setFiles([]);
      setLoading(false);
    }, 2000);
  };

  return (
    <Box sx={{ p: { xs: 2, md: 3 } }}>
      <Typography variant="h5" gutterBottom>
        List Your Produce on the Marketplace
      </Typography>
      <Paper elevation={3} sx={{ p: 3, borderRadius: 2 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Crop Name (e.g., Basmati Rice)"
              value={cropName}
              onChange={(e) => setCropName(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Quantity (in Quintals)"
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Price per Quintal (₹)"
              type="number"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <Button variant="outlined" component="label" fullWidth>
              Upload Proof of Harvest (Images/Videos)
              <input type="file" hidden multiple accept="image/*,video/*" onChange={handleFileChange} />
            </Button>
            {files.length > 0 && (
              <Typography sx={{ mt: 1 }}>{files.length} file(s) selected.</Typography>
            )}
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={handleSubmitListing}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} color="inherit" /> : 'List on Blockchain'}
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default SellPanel;
