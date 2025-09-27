// The complete code for: backend/src/controllers/notification.controller.js

import twilio from 'twilio';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const twilioPhoneNumber = process.env.TWILIO_PHONE_NUMBER;

// --- SAFETY CHECK ---
if (!accountSid || !authToken || !twilioPhoneNumber) {
    console.error('❗️FATAL ERROR: Twilio credentials are not set in the .env file.');
}
const client = twilio(accountSid, authToken);

export const sendNotification = async (req, res) => {
    const { district, message } = req.body;
    console.log(`[NOTIFY] Received request for District: "${district}", Message: "${message}"`);

    if (!district || !message) {
        return res.status(400).json({ error: 'District and message are required.' });
    }

    try {
        const farmers = await prisma.farmer.findMany({
            where: { district: { equals: district, mode: 'insensitive' } }
        });

        if (farmers.length === 0) {
            console.log(`[NOTIFY] No farmers found in database for district: "${district}"`);
            return res.status(404).json({ message: `No farmers found in ${district}.` });
        }
        
        console.log(`[NOTIFY] Found ${farmers.length} farmers. Preparing to send SMS...`);
        
        const messagePromises = farmers.map(farmer => {
            console.log(`[NOTIFY] - Queueing SMS for ${farmer.name} at phone number: ${farmer.phone}`);
            return client.messages.create({
                body: `[Kisan Salahkar]: ${message}`,
                from: twilioPhoneNumber,
                to: farmer.phone
            });
        });

        await Promise.all(messagePromises);
        console.log(`[NOTIFY] ✅ Success! All messages have been sent to Twilio.`);
        res.status(200).json({ success: true, message: `Successfully sent alert to ${farmers.length} farmers.` });

    } catch (error) {
        console.error("❗️[NOTIFY] Twilio or Database Error:", error);
        res.status(500).json({ error: 'Failed to send SMS alerts. Check server logs.' });
    }
};

// You can add your getFarmersForNotifications function back here if needed
export const getFarmersForNotifications = async (req, res) => {
    try {
        const farmers = await prisma.farmer.findMany({ select: { id: true, name: true, district: true } });
        res.status(200).json(farmers);
    } catch (error) {
        res.status(500).json({ message: 'Failed to fetch farmers.' });
    }
};
