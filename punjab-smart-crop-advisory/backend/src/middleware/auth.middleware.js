// In backend/src/middleware/auth.middleware.js (or your equivalent file)

import jwt from 'jsonwebtoken';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const protect = async (req, res, next) => {
    let token;

    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
        try {
            // 1. Get token from header
            token = req.headers.authorization.split(' ')[1];

            // 2. Verify the token
            const decoded = jwt.verify(token, process.env.JWT_SECRET);

            // 3. Find the user and attach them to the request object
            // This is the crucial step that was likely missing
            if (decoded.role === 'farmer') {
                req.user = await prisma.farmer.findUnique({
                    where: { id: decoded.id },
                    select: { id: true, name: true, email: true } // Don't select the password
                });
            } else if (decoded.role === 'buyer') {
                req.user = await prisma.buyer.findUnique({
                    where: { id: decoded.id },
                    select: { id: true, name: true, email: true }
                });
            }
            // ... you can add 'officer' role here too

            if (!req.user) {
                return res.status(401).json({ message: 'User not found.' });
            }

            // 4. Call the next middleware/controller
            next();

        } catch (error) {
            console.error('Token verification failed:', error);
            res.status(401).json({ message: 'Not authorized, token failed' });
        }
    }

    if (!token) {
        res.status(401).json({ message: 'Not authorized, no token' });
    }
};
