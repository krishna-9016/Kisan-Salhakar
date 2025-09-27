// The complete code for: backend/src/routes/notification.routes.js

import express from 'express';

// --- MIDDLEWARE IS TEMPORARILY REMOVED FOR TESTING ---
// We are not importing 'protect' because we want to bypass authentication for now.
// import { protect } from '../middleware/auth.middleware.js';

// We import our logic from the controller.
import { getFarmersForNotifications, sendNotification } from '../controllers/notification.controller.js';

const router = express.Router();

// --- AUTHENTICATION BYPASSED ---
// The 'router.use(protect);' line has been removed.
// This means you no longer need to be logged in to access these routes,
// which will stop the 'jwt malformed' error for this feature.

// This route gets the list of farmers for the UI dropdown.
router.get('/farmers', getFarmersForNotifications);

// This route sends the actual notification SMS.
router.post('/send', sendNotification);

export default router;
