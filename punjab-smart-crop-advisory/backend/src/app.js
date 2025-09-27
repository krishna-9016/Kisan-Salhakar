import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv'; // Import dotenv

// In app.js
import notificationRoutes from './routes/notification.routes.js';

dotenv.config();

// Import your modular route handlers
import authRoutes from './routes/auth.routes.js';
import farmerRoutes from './routes/farmer.routes.js';
import advisoryRoutes from './routes/advisory.routes.js';
import weatherRoutes from './routes/weather.routes.js';
import buyerRoutes from './routes/buyer.routes.js'; // 1. IMPORT THE NEW BUYER ROUTES

// Initialize the Express application
const app = express();

// --- Middlewares ---

const corsOptions = {
  origin: 'http://localhost:5173', // Only allow requests from your React app
  methods: "GET,POST,PUT,DELETE,PATCH,HEAD", // Specify allowed methods
  credentials: true // Allow cookies to be sent
};

app.use(cors(corsOptions));
app.use(express.json());

// --- Health Check and Root Routes ---
app.get('/', (req, res) => {
  res.status(200).send('Punjab Smart Crop Advisory API is running successfully!');
});

// --- API Route Registration ---
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/farmers', farmerRoutes);
app.use('/api/v1/notifications', notificationRoutes);
app.use('/api/v1/advisory', advisoryRoutes);
app.use('/api/v1/weather', weatherRoutes);
app.use('/api/v1/buyer', buyerRoutes); // 2. REGISTER THE BUYER ROUTES

// Export the configured app
export default app;
