import express from 'express';
import { 
    getMarketplace, 
    getActiveOrders, 
    initiatePurchase, 
    confirmDelivery 
} from '../controllers/buyerController.js';
import { protect } from '../middleware/auth.middleware.js'; // The corrected import path

const router = express.Router();

// All routes here are protected and require a logged-in buyer
router.use(protect);

router.get('/marketplace', getMarketplace);
router.get('/active-orders', getActiveOrders);
router.post('/purchase/:orderId', initiatePurchase);
router.put('/confirm-delivery/:orderId', confirmDelivery);

export default router;
