import express from 'express';
import axios from 'axios';
const router = express.Router();

// It's very important to store your API key in an environment variable
// and not directly in the code for security.
const OPENWEATHER_API_KEY = process.env.OPENWEATHER_API_KEY;

// This route will be accessible at GET /api/v1/weather/:city
router.get('/:city', async (req, res) => {
  const { city } = req.params;
  
  if (!OPENWEATHER_API_KEY) {
    return res.status(500).json({ error: 'Weather API key is not configured on the server.' });
  }

  const url = `https://api.openweathermap.org/data/2.5/weather?q=${city},IN&appid=${OPENWEATHER_API_KEY}&units=metric`;

  try {
    const weatherResponse = await axios.get(url);
    res.status(200).json(weatherResponse.data);
  } catch (error) {
    console.error("OpenWeather API Error:", error.response?.data || error.message);
    res.status(500).json({ error: 'Failed to fetch weather data.' });
  }
});

export default router;
