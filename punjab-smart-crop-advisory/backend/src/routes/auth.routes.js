import express from 'express';
import { 
    register as registerOfficer, 
    login as loginOfficer,
    registerBuyer, // <-- IMPORT
    loginBuyer     // <-- IMPORT
} from '../controllers/auth.controller.js';

const router = express.Router();

// --- Officer Routes ---
router.post('/register-officer', registerOfficer);
router.post('/login-officer', loginOfficer);

// --- ADD NEW BUYER AUTH ROUTES ---
router.post('/register-buyer', registerBuyer);
router.post('/login-buyer', loginBuyer);

// Export the configured router
export default router;
