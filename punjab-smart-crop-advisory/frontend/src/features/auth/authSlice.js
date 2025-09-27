import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  user: null, // The currently logged-in user
  token: null,
  registeredFarmers: [], // An array to store registered farmer data for the prototype
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // Action to add a new farmer to our list
    registerFarmer: (state, action) => {
      state.registeredFarmers.push(action.payload);
    },
    // Action to set the logged-in user
    setCredentials: (state, action) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
    },
    // Action to log out
    logOut: (state) => {
      state.user = null;
      state.token = null;
    },
  },
});

export const { registerFarmer, setCredentials, logOut } = authSlice.actions;

// Helper to easily access the data in our components
export const selectCurrentUser = (state) => state.auth.user;
export const selectRegisteredFarmers = (state) => state.auth.registeredFarmers;

export default authSlice.reducer;
