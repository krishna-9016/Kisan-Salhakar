// This function handles the chat logic. We export it so the route can use it.
export const handleChat = async (req, res) => {
  try {
    // 1. Get the message and location from the frontend request body
    const { message, location } = req.body;

    // 2. A simple validation to ensure we received the necessary data
    if (!message || !location) {
      return res.status(400).json({ error: "Message and location are required." });
    }

    // For debugging, let's log what we received from the frontend
    console.log(`Received message: "${message}" from location:`, location);

    // --- IMPORTANT AI LOGIC GOES HERE ---
    // This is where you would connect to your actual trained AI model.
    // For this hackathon prototype, we will create a smart dummy response.

    let textResponse;
    const lowerCaseMessage = message.toLowerCase();

    if (lowerCaseMessage.includes("weather")) {
      textResponse = `Based on your location (Lat: ${location.lat.toFixed(2)}, Lon: ${location.lon.toFixed(2)}), the weather forecast for tomorrow is sunny with a high of 32°C and a slight chance of evening showers.`;
    } else if (lowerCaseMessage.includes("soil")) {
      textResponse = `For your area, the soil is predominantly alluvial, which is excellent for cultivation. It is recommended to test for nitrogen and phosphorus levels before planting your next crop.`;
    } else if (lowerCaseMessage.includes("wheat") || lowerCaseMessage.includes("kanak")) {
      textResponse = `For wheat (ਕਣਕ) crops at your location, ensure proper irrigation during the crown root initiation stage. Be vigilant for signs of yellow rust disease, especially in humid conditions. The ideal sowing time is from late October to mid-November.`;
    } else if (lowerCaseMessage.includes("paddy") || lowerCaseMessage.includes("rice")) {
      textResponse = "For paddy cultivation in Punjab, ensure your field is well-puddled. Consider Direct Seeded Rice (DSR) technology to save water. Basmati varieties are currently fetching a good price in the market.";
    } else {
      textResponse = `Thank you for asking about "${message}". I am analyzing the specific conditions at your farm's location. Please provide more details for a precise recommendation.`;
    }
    
    // 3. Send the generated response back to the frontend
    // The frontend is expecting an object with a 'textResponse' key.
    res.status(200).json({
      textResponse: textResponse,
    });

  } catch (error) {
    // If any other error occurs, log it on the server and send a generic error message
    console.error("Error in chat advisory controller:", error);
    res.status(500).json({ error: "An internal server error occurred on the server." });
  }
};
