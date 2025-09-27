import express from 'express';
import { protect } from '../middleware/auth.middleware.js'; // Your authentication middleware

// --- THE CORRECTED IMPORT STATEMENT ---
// We must import all functions we intend to use from the controller file.
import { 
    getFarmerProfile, 
    updateFarmerProfile, 
    listProduce // <-- THIS WAS THE MISSING PIECE
} from '../controllers/farmer.controller.js';

const router = express.Router();

// This line protects all routes defined below it
router.use(protect); 

// --- Existing Farmer Routes ---
router.route('/profile')
    .get(getFarmerProfile)
    .put(updateFarmerProfile);

// --- New Route for Listing Produce ---
router.post('/produce', listProduce);

export default router;
