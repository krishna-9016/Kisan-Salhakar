import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Button, Paper, CircularProgress, Alert,
  MenuItem, Select, InputLabel, FormControl, TextField,
  Card, CardContent, Chip, List, ListItem, ListItemText, Divider, IconButton
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from 'react-leaflet';
import L from 'leaflet';
import { cropAdvisoryService } from '../services/cropAdvisoryApi';
import CloseIcon from '@mui/icons-material/Close';
import './LocationAdvisoryPage.css';


// --- Map Setup (No changes) ---
const punjabLocations = {
    "Amritsar": [31.6340, 74.8723], "Barnala": [30.3781, 75.5426], "Bathinda": [30.2110, 74.9455],
    "Faridkot": [30.6753, 74.7543], "Fatehgarh Sahib": [30.6433, 76.3933], "Fazilka": [30.4036, 74.0254],
    "Ferozepur": [30.9248, 74.6042], "Gurdaspur": [32.0404, 75.4042], "Hoshiarpur": [31.5300, 75.9100],
    "Jalandhar": [31.3260, 75.5762], "Kapurthala": [31.3833, 75.3833], "Ludhiana": [30.9010, 75.8573],
    "Malerkotla": [30.5235, 75.8880], "Mansa": [29.9833, 75.3833], "Moga": [30.8058, 75.1734],
    "Pathankot": [32.2683, 75.6493], "Patiala": [30.3398, 76.3869], "Rupnagar": [30.9667, 76.5333],
    "Sahibzada Ajit Singh Nagar (Mohali)": [30.7046, 76.7179], "Sangrur": [30.2558, 75.8433],
    "Shahid Bhagat Singh Nagar": [31.0900, 76.1200], "Sri Muktsar Sahib": [30.4739, 74.5122], "Tarn Taran": [31.4503, 74.9252],
};
const punjabCenter = [31.1471, 75.3412];


delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});


// --- Map Utility Components ---
const ChangeView = ({ center, zoom }) => { const map = useMap(); useEffect(() => { map.setView(center, zoom); }, [center, zoom, map]); return null; };
const MapClickHandler = ({ onMapClick }) => { useMapEvents({ click(e) { onMapClick(e.latlng); } }); return null; };


// --- Main Component ---
const LocationAdvisoryPage = () => {
    const navigate = useNavigate();
    const [selectedLocation, setSelectedLocation] = useState(null);
    const [selectedCity, setSelectedCity] = useState("");
    const [mapCenter, setMapCenter] = useState(punjabCenter);
    const [mapZoom, setMapZoom] = useState(8);
    const [loading, setLoading] = useState(false);
    const [isLocating, setIsLocating] = useState(false);
    const [selectedCrop, setSelectedCrop] = useState("");
    const [farmSize, setFarmSize] = useState("");
    const [supportedCrops, setSupportedCrops] = useState([]);
    const [predictionResult, setPredictionResult] = useState(null);
    const [apiError, setApiError] = useState(null);
    const [previousCrop, setPreviousCrop] = useState("");
    const [previousCropWarning, setPreviousCropWarning] = useState('');


    useEffect(() => {
        const loadSupportedCrops = async () => {
            try {
                const cropsData = await cropAdvisoryService.getSupportedCrops();
                setSupportedCrops(cropsData.crops || ['wheat', 'rice', 'cotton', 'maize', 'sugarcane']);
            } catch (error) {
                console.error('Failed to load crops:', error);
                setSupportedCrops(['wheat', 'rice', 'cotton', 'maize', 'sugarcane']);
            }
        };
        loadSupportedCrops();
    }, []);

    // --- UPDATED: Logic to show warning when crops are the same ---
    useEffect(() => {
        if (selectedCrop && previousCrop && selectedCrop === previousCrop) {
            setPreviousCropWarning(`This crop was grown by you previously. Growing it again may not give the best results.`);
        } else {
            setPreviousCropWarning('');
        }
    }, [selectedCrop, previousCrop]);

    const resetForNewSelection = () => {
        setPredictionResult(null);
        setApiError(null);
        setSelectedCrop("");
        setPreviousCrop("");
        setFarmSize("");
    };

    const handleMapClick = (latlng) => { setSelectedLocation(latlng); setSelectedCity(""); resetForNewSelection(); };
    const handleCityChange = (event) => {
        const city = event.target.value;
        setSelectedCity(city);
        const newCoords = punjabLocations[city];
        const newLatLng = { lat: newCoords[0], lng: newCoords[1] };
        setSelectedLocation(newLatLng);
        setMapCenter(newCoords);
        setMapZoom(11);
        resetForNewSelection();
    };

    const handleGetCurrentLocation = () => {
        if (!navigator.geolocation) { setApiError("Geolocation is not supported by your browser."); return; }
        setIsLocating(true);
        resetForNewSelection();
        setSelectedCity("");
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                const newLatLng = { lat: latitude, lng: longitude };
                setSelectedLocation(newLatLng);
                setMapCenter([latitude, longitude]);
                setMapZoom(13);
                setIsLocating(false);
            },
            () => {
                setApiError("Could not retrieve your location. Please enable permissions.");
                setIsLocating(false);
            }
        );
    };

    const handleGetAdvisory = async () => {
        if (!selectedLocation || !selectedCrop || !farmSize) { setApiError('Please select a location, current crop, and farm size.'); return; }
        setLoading(true);
        setApiError(null);
        try {
            const result = await cropAdvisoryService.getCropPrediction({
                latitude: selectedLocation.lat,
                longitude: selectedLocation.lng,
                crop: selectedCrop,
                farmSize: parseFloat(farmSize),
                previous_crop: previousCrop
            });
            setPredictionResult(result);
        } catch (error) {
            setApiError(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="location-advisory-container">
            <header className="location-advisory-header">
                <Typography variant="h4" component="h1">🌾 Smart Crop Advisory</Typography>
                <Button variant="outlined" onClick={() => navigate('/')}>Back to Home</Button>
            </header>

            <main className="location-advisory-main-content">
                <div className="map-panel">
                    <MapContainer center={mapCenter} zoom={mapZoom} className="full-height-map">
                        <ChangeView center={mapCenter} zoom={mapZoom} />
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                        <MapClickHandler onMapClick={handleMapClick} />
                        {selectedLocation && <Marker position={selectedLocation} />}
                    </MapContainer>
                </div>

                <div className="advisory-panel">
                    <Paper elevation={3} sx={{ p: 3, borderRadius: 3, height: '100%', display: 'flex', flexDirection: 'column' }}>
                        <Typography variant="h5" gutterBottom>🌾 Crop Advisory Analysis</Typography>
                        
                        {!predictionResult ? (
                            <>
                                <FormControl fullWidth sx={{ mb: 2 }}>
                                    <InputLabel>Select District</InputLabel>
                                    <Select value={selectedCity} label="Select District" onChange={handleCityChange}>{Object.keys(punjabLocations).map(city => <MenuItem key={city} value={city}>{city}</MenuItem>)}</Select>
                                </FormControl>
                                <Button variant="contained" onClick={handleGetCurrentLocation} disabled={isLocating} fullWidth sx={{ mb: 2 }}>
                                    {isLocating ? <CircularProgress size={24} color="inherit" /> : '📍 Use My Current Location'}
                                </Button>
                                <Divider sx={{ my: 1 }}>Analysis Details</Divider>
                                
                                {/* --- NEW ORDER: Previous Crop First --- */}
                                <FormControl fullWidth sx={{ mt: 2, mb: 2 }} disabled={!selectedLocation}>
                                    <InputLabel>Select Previous Crop (Optional)</InputLabel>
                                    <Select value={previousCrop} label="Select Previous Crop (Optional)" onChange={(e) => setPreviousCrop(e.target.value)}>
                                        {supportedCrops.map(crop => (
                                            <MenuItem key={crop} value={crop}>
                                                {crop.charAt(0).toUpperCase() + crop.slice(1)}
                                            </MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                
                                {/* --- NEW ORDER: Current Crop Second --- */}
                                <FormControl fullWidth sx={{ mb: 2 }} disabled={!selectedLocation}>
                                    <InputLabel>Select Current Crop</InputLabel>
                                    <Select value={selectedCrop} label="Select Current Crop" onChange={(e) => setSelectedCrop(e.target.value)}>
                                        {supportedCrops.map(crop => (
                                            <MenuItem key={crop} value={crop}>
                                                {crop.charAt(0).toUpperCase() + crop.slice(1)}
                                            </MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                
                                {/* --- UPDATED: Display warning message without disabling --- */}
                                {previousCropWarning && <Alert severity="warning" sx={{ mb: 2 }}>{previousCropWarning}</Alert>}

                                <TextField fullWidth label="Farm Size (acres)" type="number" value={farmSize} onChange={(e) => setFarmSize(e.target.value)} inputProps={{ min: 0.1, step: 0.1 }} sx={{ mb: 2 }} disabled={!selectedLocation} />
                            </>
                        ) : null}
                        
                        {apiError && <Alert severity="error" sx={{ mb: 2, mt: 1 }}>{apiError}</Alert>}
                        
                        <Box sx={{ flexGrow: 1, overflowY: 'auto', pr: 1 }}>
                            {loading && <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}><CircularProgress /><Typography sx={{ ml: 2 }}>Analyzing...</Typography></Box>}
                            
                            {!loading && !predictionResult && !selectedLocation && <Alert severity="info" sx={{ mt: 2 }}>Please select a location to begin.</Alert>}
                            
                            {!loading && !predictionResult && selectedLocation && (
                                <Box sx={{ textAlign: 'center', mt: 4 }}>
                                    <Typography gutterBottom><b>Location:</b> {selectedCity || `${selectedLocation.lat.toFixed(4)}, ${selectedLocation.lng.toFixed(4)}`}</Typography>
                                    <Button variant="contained" size="large" onClick={handleGetAdvisory} disabled={!selectedCrop || !farmSize} sx={{ mt: 2 }}>🚀 Get AI Prediction</Button>
                                </Box>
                            )}

                            {/* Corrected results display */}
                            {predictionResult && !loading && (
                                <Box>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                                        <Typography variant="h6">Analysis Results</Typography>
                                        <Button variant="outlined" onClick={resetForNewSelection} startIcon={<CloseIcon />}>New Analysis</Button>
                                    </Box>
                                    <div className="prediction-results-container">
                                        <Card sx={{ mb: 2 }}>
                                            <CardContent>
                                                <Typography variant="h6" color="primary">📊 Yield Prediction</Typography>
                                                <Typography variant="h4" color="success.main" sx={{ my: 1 }}>{predictionResult.predicted_yield} kg/acre</Typography>
                                                <Typography variant="body2">Range: {predictionResult.yield_range.minimum} - {predictionResult.yield_range.maximum} kg/acre</Typography>
                                                <Chip label={`${predictionResult.confidence} Confidence`} color={predictionResult.confidence === 'High' ? 'success' : 'warning'} size="small" sx={{ mt: 1 }} />
                                            </CardContent>
                                        </Card>
                                        
                                        {predictionResult.crop_recommendations?.length > 0 && (
                                            <Card sx={{ mb: 2 }}>
                                                <CardContent>
                                                    <Typography variant="h6" color="primary" gutterBottom>🌱 Alternative Crops</Typography>
                                                    {predictionResult.crop_recommendations.slice(0, 3).map((rec, index) => (
                                                        <Box key={index} sx={{ mb: 1.5, p: 1.5, bgcolor: 'grey.50', borderRadius: 1 }}>
                                                            <Typography variant="subtitle1" fontWeight="bold">{rec.crop_name} - {rec.profitability} Profitability</Typography>
                                                            <Typography variant="body2">Expected: {rec.expected_yield} kg/acre</Typography>
                                                            <Typography variant="caption" color="text.secondary">{rec.reasons?.[0]}</Typography>
                                                        </Box>
                                                    ))}
                                                </CardContent>
                                            </Card>
                                        )}

                                        {predictionResult.farming_tips?.length > 0 && (
                                            <Card sx={{ mb: 2 }}>
                                                <CardContent>
                                                    <Typography variant="h6" color="primary" gutterBottom>💡 Farming Tips</Typography>
                                                    <List dense sx={{ pl: 2 }}>
                                                        {predictionResult.farming_tips.slice(0, 4).map((tip, index) => (
                                                            <ListItem key={index} sx={{ py: 0, display: 'list-item' }}>
                                                                <ListItemText primary={tip} primaryTypographyProps={{ variant: 'body2' }} />
                                                            </ListItem>
                                                        ))}
                                                    </List>
                                                </CardContent>
                                            </Card>
                                        )}
                                        
                                        {predictionResult.seasonal_advice && (
                                            <Card>
                                                <CardContent> 
                                                    <Typography variant="h6" color="primary" gutterBottom>🗓️ Seasonal Advice</Typography>
                                                    <Typography variant="body2">{predictionResult.seasonal_advice}</Typography>
                                                </CardContent>
                                            </Card>
                                        )}
                                    </div>
                                </Box>
                            )}
                        </Box>
                    </Paper>
                </div>
            </main>
        </div>
    );
};

export default LocationAdvisoryPage;
