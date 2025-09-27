import axios from 'axios';

// The base URL and API key for the new Punjab Crop Advisory API
const CROP_API_BASE_URL = 'http://localhost:9090';
const API_KEY = 'punjab_crop_api_2024';

// Create an axios instance with a default configuration
const cropApiClient = axios.create({
  baseURL: CROP_API_BASE_URL,
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  }
});

/**
 * Service object for interacting with the Punjab Crop Advisory API.
 */
export const cropAdvisoryService = {
  /**
   * Fetches crop yield prediction and detailed recommendations.
   * @param {object} locationData - Contains latitude, longitude, crop, and farmSize.
   * @returns {Promise<object>} The prediction data from the API.
   */
  async getCropPrediction(locationData) {
    try {
      const response = await cropApiClient.post('/api/v1/predict', {
        crop: locationData.crop,
        acres: locationData.farmSize,
        latitude: locationData.latitude,
        longitude: locationData.longitude
      });
      return response.data;
    } catch (error) {
      console.error('Crop prediction failed:', error);
      // Provide a more descriptive error message
      throw new Error(error.response?.data?.detail || 'Failed to get crop prediction');
    }
  },

  /**
   * Fetches the list of crops supported by the prediction model.
   * @returns {Promise<object>} A list of supported crops.
   */
  async getSupportedCrops() {
    try {
      const response = await cropApiClient.get('/api/v1/crops');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch crops:', error);
      throw error;
    }
  },

  /**
   * Fetches the list of districts in Punjab.
   * @returns {Promise<object>} A list of districts.
   */
  async getPunjabDistricts() {
    try {
      const response = await cropApiClient.get('/api/v1/districts');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch districts:', error);
      throw error;
    }
  },

  /**
   * Checks the health status of the API.
   * @returns {Promise<object>} The health status.
   */
  async checkApiHealth() {
    try {
      const response = await cropApiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('API health check failed:', error);
      return { status: 'unavailable' };
    }
  }
};
