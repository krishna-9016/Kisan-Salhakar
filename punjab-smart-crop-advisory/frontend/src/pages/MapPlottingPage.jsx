import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import axios from 'axios';
import { 
    Paper, Typography, FormControl, InputLabel, Select, MenuItem, 
    Alert, Box, CircularProgress 
} from '@mui/material';
import { 
    MapContainer, TileLayer, FeatureGroup, GeoJSON 
} from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import L from 'leaflet';

import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import './OfficerDashboard.css';

// Fix for a common issue with Leaflet icons in React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const punjabCenter = [31.1471, 75.3412];

const MapPlottingPage = () => {
  const [farmers, setFarmers] = useState([]);
  const [selectedFarmer, setSelectedFarmer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token } = useSelector((state) => state.auth);

  useEffect(() => {
    const fetchFarmers = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        const response = await axios.get('http://localhost:5000/api/v1/farmers', {
          headers: { Authorization: `Bearer ${token}` },
        });
        
        const fetchedFarmers = response.data;
        setFarmers(fetchedFarmers);

        // --- THIS IS THE FIX ---
        // If farmers are loaded, automatically select the first one.
        if (fetchedFarmers && fetchedFarmers.length > 0) {
          setSelectedFarmer(fetchedFarmers[0]);
        }
        // --------------------

        setError('');
      } catch (err) {
        setError('Could not load farmer data. Ensure backend is running.');
        console.error("API Error fetching farmers:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchFarmers();
  }, [token]);

  const handleNewPlot = (e) => {
    // Logic for creating a new plot
  };

  const handleFarmerSelection = (farmerId) => {
    const farmer = farmers.find(f => f.id === farmerId);
    setSelectedFarmer(farmer);
  };

  return (
    <Box sx={{ height: 'calc(100vh - 120px)' }}> 
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      <Paper 
        className="dashboard-paper-card" 
        sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
      >
        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
          Farmer Plot Management
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Select a farmer to view their plots or draw a new one on the map.
        </Typography>

        <FormControl fullWidth sx={{ mb: 2 }} disabled={loading}>
          <InputLabel>Select a Farmer</InputLabel>
          <Select
            value={selectedFarmer?.id || ''}
            label="Select a Farmer"
            onChange={(e) => handleFarmerSelection(e.target.value)}
          >
            {loading ? (
                <MenuItem disabled><em>Loading farmers...</em></MenuItem>
            ) : (
              farmers.map(farmer => (
                <MenuItem key={farmer.id} value={farmer.id}>
                  {farmer.name} ({farmer.phone})
                </MenuItem>
              ))
            )}
          </Select>
        </FormControl>

        <Box sx={{ flexGrow: 1, borderRadius: '12px', overflow: 'hidden', position: 'relative' }}>
          <MapContainer 
              center={punjabCenter} 
              zoom={8} 
              style={{ height: "100%", width: "100%" }}
          >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <FeatureGroup>
              <EditControl
                position="topright"
                onCreated={handleNewPlot}
                draw={{ rectangle: false, circle: false, circlemarker: false, marker: false, polyline: false }}
              />
              {/* This will now render the plots of the automatically selected farmer */}
              {selectedFarmer && selectedFarmer.farms?.map(farm => (
                <GeoJSON key={farm.id} data={farm.plotGeoJson} style={{ color: 'blue', weight: 2 }} />
              ))}
            </FeatureGroup>
          </MapContainer>
        </Box>
      </Paper>
    </Box>
  );
};

export default MapPlottingPage;
