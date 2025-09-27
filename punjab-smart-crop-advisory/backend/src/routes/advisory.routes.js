import express from 'express';
import { register as registerOfficer, login as loginOfficer } from '../controllers/auth.controller.js';

// Create a new router instance from Express
const router = express.Router();

// --- Define the Officer Registration Route ---
// When a POST request comes to '/register-officer',
// it will be handled by the 'registerOfficer' function from your controller.
// The full path will be: /api/v1/auth/register-officer
router.post('/register-officer', registerOfficer);

// --- Define the Officer Login Route ---
// When a POST request comes to '/login-officer',
// it will be handled by the 'loginOfficer' function.
// The full path will be: /api/v1/auth/login-officer
router.post('/login-officer', loginOfficer);

// Export the configured router so app.js can use it
export default router;
