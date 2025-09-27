import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

// @desc    Get the profile of the logged-in farmer
// @route   GET /api/v1/farmers/profile
export const getFarmerProfile = async (req, res) => {
    try {
        // req.user is attached by the 'protect' middleware
        const farmer = await prisma.farmer.findUnique({
            where: { id: req.user.id },
            select: { id: true, name: true, email: true, phone: true } // Exclude password
        });

        if (!farmer) {
            return res.status(404).json({ message: 'Farmer not found.' });
        }

        res.status(200).json(farmer);
    } catch (error) {
        res.status(500).json({ message: 'Server error fetching profile.' });
    }
};

// @desc    Update the profile of the logged-in farmer
// @route   PUT /api/v1/farmers/profile
export const updateFarmerProfile = async (req, res) => {
    const { name, phone } = req.body;
    try {
        const updatedFarmer = await prisma.farmer.update({
            where: { id: req.user.id },
            data: { name, phone },
            select: { id: true, name: true, email: true, phone: true }
        });
        res.status(200).json({ message: 'Profile updated successfully', farmer: updatedFarmer });
    } catch (error) {
        res.status(500).json({ message: 'Server error updating profile.' });
    }
};

// @desc    Allow a farmer to list new produce for sale
// @route   POST /api/v1/farmers/produce
export const listProduce = async (req, res) => {
    const { produceName, quantity, pricePerKg } = req.body;

    if (!req.user || !req.user.id) {
        return res.status(401).json({ message: 'Authentication Error: You must be logged in as a farmer.' });
    }
    const farmerId = req.user.id;

    if (!produceName || !quantity || !pricePerKg) {
        return res.status(400).json({ message: 'Please provide all required fields.' });
    }

    try {
        const newListing = await prisma.order.create({
            data: {
                produceName,
                quantity: parseFloat(quantity),
                pricePerKg: parseFloat(pricePerKg),
                farmerId: farmerId,
                status: 'Listed',
            },
        });

        res.status(201).json({ message: 'Produce listed successfully!', listing: newListing });
    } catch (error) {
        console.error('[BACKEND /produce] DATABASE ERROR:', error);
        res.status(500).json({ message: 'Server error while saving produce.' });
    }
};
