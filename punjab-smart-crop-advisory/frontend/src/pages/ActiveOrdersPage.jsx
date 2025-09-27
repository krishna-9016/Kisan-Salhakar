import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress, Alert, Card, CardContent, CardActions, Button, Chip } from '@mui/material';
import { getMyActiveOrders, confirmDelivery } from '../services/buyerApi';

const ActiveOrdersPage = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchOrders = async () => {
        try {
            setLoading(true);
            const { data } = await getMyActiveOrders();
            setOrders(data);
        } catch (err) {
            setError('Failed to fetch active orders.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchOrders();
    }, []);

    const handleConfirmDelivery = async (orderId) => {
        try {
            await confirmDelivery(orderId);
            fetchOrders(); // Re-fetch orders to show updated status
        } catch (err) {
            setError('Failed to confirm delivery.');
        }
    };

    if (loading) return <CircularProgress />;

    return (
        <Box>
            <Typography variant="h4" gutterBottom>My Active Orders</Typography>
            {error && <Alert severity="error">{error}</Alert>}
            {orders.length === 0 && !loading && <Typography>You have no active orders.</Typography>}
            {orders.map((order) => (
                <Card key={order.id} sx={{ mb: 2 }}>
                    <CardContent>
                        <Typography variant="h6">{order.produceName}</Typography>
                        <Typography>Status: <Chip label={order.status} color="primary" /></Typography>
                        <Typography>Order ID: {order.id}</Typography>
                    </CardContent>
                    <CardActions>
                        {/* Show button only if delivery is pending confirmation */}
                        {order.status === 'In-Transit' || order.status === 'Purchased' && (
                            <Button size="small" variant="contained" color="success" onClick={() => handleConfirmDelivery(order.id)}>
                                Confirm Delivery & Trigger Payment
                            </Button>
                        )}
                    </CardActions>
                </Card>
            ))}
        </Box>
    );
};

export default ActiveOrdersPage;
