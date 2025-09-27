import axios from 'axios';


const API_URL = 'http://localhost:5000/api/buyer'; // Backend URL

// Helper to get the token from localStorage
const getAuthToken = () => localStorage.getItem('buyerToken');

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor to add the token to every request
api.interceptors.request.use(config => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getMarketplaceListings = () => api.get('/marketplace');
export const getMyActiveOrders = () => api.get('/active-orders');
export const purchaseListing = (orderId) => api.post(`/purchase/${orderId}`);
export const confirmDelivery = (orderId) => api.put(`/confirm-delivery/${orderId}`);

// You'll also need a login function
// export const loginBuyer = (credentials) => axios.post('http://localhost:5000/api/auth/buyer-login', credentials);
