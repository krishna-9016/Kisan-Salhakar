import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setCredentials } from './features/auth/authSlice';

// --- Your existing page imports ---
import HomePage from './pages/HomePage';
import FarmerLoginPage from './pages/FarmerLoginPage';
import OfficerLoginPage from './pages/OfficerLoginPage';
import VerifyOtpPage from './pages/VerifyOtpPage';
import FarmerDashboard from './pages/FarmerDashboard';
import CropDoctorPage from './pages/CropDoctorPage';
import LocationAdvisoryPage from './pages/LocationAdvisoryPage';
import SatelliteViewPage from './pages/SatelliteViewPage';
import MarketplacePage from './pages/MarketplacePage';
import DashboardLayout from './layouts/DashboardLayout';
import DashboardHomePage from './pages/DashboardHomePage';
import MapPlottingPage from './pages/MapPlottingPage';
import SendNotificationPage from './pages/SendNotificationPage';
import ProtectedRoute from './components/ProtectedRoute';

// --- NEW: Import the Buyer components ---
import BuyerLoginPage from './pages/BuyerLoginPage';
import BuyerDashboardLayout from './layouts/BuyerDashboardLayout';
import ActiveOrdersPage from './pages/ActiveOrdersPage';
import BuyerProtectedRoute from './components/BuyerProtectedRoute';


function App() {
  const dispatch = useDispatch();

  // Your existing Redux hydration logic (unchanged)
  useEffect(() => {
    const userData = localStorage.getItem('userData');
    if (userData) {
      const { user, token } = JSON.parse(userData);
      if (user && token) {
        dispatch(setCredentials({ user, token }));
      }
    }
  }, [dispatch]);

  return (
    <Router>
      <Routes>
        {/* --- Public Routes (unchanged) --- */}
        <Route path="/" element={<HomePage />} />
        <Route path="/farmer-login" element={<FarmerLoginPage />} />
        <Route path="/officer-login" element={<OfficerLoginPage />} />
        <Route path="/verify-otp" element={<VerifyOtpPage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/crop-doctor" element={<CropDoctorPage />} />
        <Route path="/location-advisory" element={<LocationAdvisoryPage />} />
        <Route path="/satellite-view" element={<SatelliteViewPage />} />
        
        {/* --- NEW: Public Route for Buyer Login --- */}
        <Route path="/buyer-login" element={<BuyerLoginPage />} />
        
        {/* --- Existing Protected Routes (unchanged) --- */}
        <Route element={<ProtectedRoute />}>
          <Route path="/farmer-dashboard" element={<FarmerDashboard />} />
          <Route path="/officer" element={<DashboardLayout />}>
            <Route index element={<DashboardHomePage />} />
            <Route path="map-plotting" element={<MapPlottingPage />} />
            <Route path="send-notification" element={<SendNotificationPage />} />
          </Route>
        </Route>

        {/* --- NEW: Protected Buyer Routes --- */}
        <Route element={<BuyerProtectedRoute />}>
          <Route path="/buyer" element={<BuyerDashboardLayout />}>
            <Route path="marketplace" element={<MarketplacePage />} />
            <Route path="active-orders" element={<ActiveOrdersPage />} />
          </Route>
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
