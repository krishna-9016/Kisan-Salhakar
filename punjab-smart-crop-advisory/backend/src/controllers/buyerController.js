import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();
// import { createTransaction, triggerPayment } from '../services/blockchainService.js'; // Your blockchain service

// @desc    Fetch all produce available for sale (status: 'Listed')
// @route   GET /api/buyer/marketplace
export const getMarketplace = async (req, res) => {
  try {
    const produce = await prisma.order.findMany({
      where: { status: 'Listed' },
      // include: { farmer: { select: { name: true, location: true } } } // Include farmer details
    });
    res.json(produce);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// @desc    Get active orders for the logged-in buyer
// @route   GET /api/buyer/active-orders
export const getActiveOrders = async (req, res) => {
  try {
    const activeOrders = await prisma.order.findMany({
      where: {
        buyerId: req.user.id, // Comes from your auth middleware
        status: { in: ['Purchased', 'In-Transit', 'Delivered'] }
      },
      orderBy: { createdAt: 'desc' }
    });
    res.json(activeOrders);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// @desc    Initiate a purchase
// @route   POST /api/buyer/purchase/:orderId
export const initiatePurchase = async (req, res) => {
  const { orderId } = req.params;
  const buyerId = req.user.id;

  try {
    const order = await prisma.order.findUnique({ where: { id: orderId } });

    if (!order || order.status !== 'Listed') {
      return res.status(404).json({ message: 'Produce not available for purchase.' });
    }

    // --- BLOCKCHAIN INTEGRATION POINT ---
    // const transaction = await createTransaction(order, buyerId);

    const updatedOrder = await prisma.order.update({
      where: { id: orderId },
      data: {
        buyerId: buyerId,
        status: 'Purchased',
        // transactionHash: transaction.hash, // Save the hash from your blockchain service
      },
    });

    res.status(200).json(updatedOrder);
  } catch (error) {
    res.status(500).json({ message: 'Purchase failed', error: error.message });
  }
};

// @desc    Confirm delivery of an order
// @route   PUT /api/buyer/confirm-delivery/:orderId
export const confirmDelivery = async (req, res) => {
  const { orderId } = req.params;

  try {
    const order = await prisma.order.findFirst({
        where: { id: orderId, buyerId: req.user.id }
    });

    if (!order) {
      return res.status(401).json({ message: 'Order not found or you are not authorized.' });
    }

    // --- BLOCKCHAIN INTEGRATION POINT ---
    // This call triggers the smart contract to pay the farmer
    // const paymentResult = await triggerPayment(order.transactionHash);

    // if (paymentResult.success) {
    //     const finalOrder = await prisma.order.update({
    //         where: { id: orderId },
    //         data: { status: 'Payment-Complete' }
    //     });
    //     res.status(200).json({ message: 'Delivery confirmed and payment completed.', order: finalOrder });
    // } else {
    //      throw new Error("Blockchain payment failed");
    // }

    // For now, we'll just mark it as delivered
    const updatedOrder = await prisma.order.update({
        where: { id: orderId },
        data: { status: 'Delivered' }
    });
    res.status(200).json({ message: 'Delivery confirmed. Payment process initiated.', order: updatedOrder });

  } catch (error) {
    res.status(500).json({ message: 'Confirmation failed', error: error.message });
  }
};
