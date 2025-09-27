import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

const ProtectedRoute = () => {
  // Get the user's token from the Redux store
  const { token } = useSelector((state) => state.auth);
  
  // Get the current URL path the user is trying to access
  const location = useLocation();

  // If the user is NOT logged in...
  if (!token) {
    // ...and they are trying to access the officer's dashboard...
    if (location.pathname.startsWith('/dashboard')) {
      // ...send them to the OFFICER login page.
      return <Navigate to="/officer-login" replace />;
    }
    
    // ...otherwise (if they are trying to access the farmer's dashboard)...
    // ...send them to the FARMER login page.
    return <Navigate to="/farmer-login" replace />;
  }

  // If the user IS logged in, everything is okay.
  // Allow them to see the page they were trying to access.
  return <Outlet />;
};

export default ProtectedRoute;
