import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const prisma = new PrismaClient();

// --- Officer Authentication (Unchanged) ---

export const register = async (req, res) => {
    const { name, email, password } = req.body;
    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const officer = await prisma.extensionOfficer.create({
            data: {
                name,
                email,
                password: hashedPassword,
            },
        });
        res.status(201).json({ message: 'Officer registered successfully', officerId: officer.id });
    } catch (error) {
        res.status(400).json({ message: 'User already exists or invalid data', error: error.message });
    }
};

export const login = async (req, res) => {
    const { email, password } = req.body;
    try {
        const officer = await prisma.extensionOfficer.findUnique({ where: { email } });
        if (!officer) {
            return res.status(404).json({ message: 'Officer not found' });
        }
        const isPasswordCorrect = await bcrypt.compare(password, officer.password);
        if (!isPasswordCorrect) {
            return res.status(400).json({ message: 'Invalid credentials' });
        }
        const token = jwt.sign(
            { id: officer.id, email: officer.email, role: 'officer' },
            process.env.JWT_SECRET,
            { expiresIn: '1h' }
        );
        res.status(200).json({ token, officer: { id: officer.id, name: officer.name, email: officer.email } });
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
};

// --- Buyer Authentication ---

export const registerBuyer = async (req, res) => {
    const { name, email, password } = req.body;
    try {
        const existingBuyer = await prisma.buyer.findUnique({ where: { email } });
        if (existingBuyer) {
            return res.status(400).json({ message: 'Buyer with this email already exists.' });
        }
        const hashedPassword = await bcrypt.hash(password, 10);
        const buyer = await prisma.buyer.create({
            data: {
                name,
                email,
                password: hashedPassword,
            },
        });
        const token = jwt.sign({ id: buyer.id, role: 'buyer' }, process.env.JWT_SECRET, {
            expiresIn: '30d',
        });
        res.status(201).json({
            message: "Buyer registered successfully",
            token,
            buyer: { id: buyer.id, name: buyer.name, email: buyer.email }
        });
    } catch (error) {
        res.status(500).json({ message: 'Server error during buyer registration.', error: error.message });
    }
};

// @desc    Login a buyer (WITH PASSWORD CHECK DISABLED FOR DEBUGGING)
// @route   POST /api/v1/auth/login-buyer
export const loginBuyer = async (req, res) => {
    const { email, password } = req.body;

    // --- DEBUGGING LOG ---
    console.log(`[LOGIN ATTEMPT] Received login request for email: ${email}`);

    try {
        const buyer = await prisma.buyer.findUnique({ where: { email } });

        // Check if the user exists
        if (!buyer) {
            // --- DEBUGGING LOG ---
            console.log(`[LOGIN FAILED] No user found with email: ${email}`);
            return res.status(401).json({ message: 'Invalid credentials.' });
        }

        // --- DEBUGGING LOG ---
        console.log('[LOGIN SUCCESS] User found in database:', buyer);
        console.log(`[LOGIN INFO] Stored password in DB is: ${buyer.password}`);
        console.log(`[LOGIN INFO] Password received from form is: ${password}`);
        
        // --- BCRYPT PASSWORD CHECK IS DISABLED ---
        console.log('[LOGIN BYPASS] Skipping password check for prototype demo.');
        
        // --- If we reach here, login is successful ---
        const token = jwt.sign({ id: buyer.id, role: 'buyer' }, process.env.JWT_SECRET, {
            expiresIn: '30d',
        });
        
        console.log(`[LOGIN SUCCESS] JWT token generated for user: ${buyer.id}`);
        
        res.status(200).json({
            message: "Login successful (Password check disabled)",
            token,
            buyer: { id: buyer.id, name: buyer.name, email: buyer.email }
        });

    } catch (error) {
        console.error('[LOGIN ERROR] An unexpected error occurred:', error);
        res.status(500).json({ message: 'Server error during buyer login.', error: error.message });
    }
};
