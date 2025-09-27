// In frontend/src/services/api.js

import axios from 'axios';

// Create a new axios instance
const api = axios.create({
    baseURL: 'http://localhost:5000/api/v1', // Your backend's base URL
});

// --- IMPORTANT: The Axios Interceptor ---
// This code runs BEFORE every single request that is sent using this 'api' instance.
api.interceptors.request.use(
    (config) => {
        // Try to get the token from localStorage
        // We check for both buyer and farmer tokens to make this instance reusable
        const token = localStorage.getItem('buyerToken') || localStorage.getItem('farmerToken');
        
        if (token) {
            // If a token exists, add it to the 'Authorization' header
            config.headers['Authorization'] = `Bearer ${token}`;
            console.log('Token attached to request headers:', config.headers['Authorization']);
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
