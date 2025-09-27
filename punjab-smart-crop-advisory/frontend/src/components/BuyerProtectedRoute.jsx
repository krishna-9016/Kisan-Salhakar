import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const BuyerProtectedRoute = () => {
  const token = localStorage.getItem('buyerToken');

  // If the buyer token exists, allow access to the nested routes (the dashboard).
  // Otherwise, redirect to the buyer login page.
  return token ? <Outlet /> : <Navigate to="/buyer-login" replace />;
};

export default BuyerProtectedRoute;
