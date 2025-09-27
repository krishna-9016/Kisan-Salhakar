import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const BuyerProtectedRoute = () => {
  const token = localStorage.getItem('buyerToken');

  // If there's a token, show the page (using <Outlet />).
  // Otherwise, redirect them to the buyer login page.
  return token ? <Outlet /> : <Navigate to="/buyer-login" />;
};

export default BuyerProtectedRoute;
