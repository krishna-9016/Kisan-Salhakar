import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Paper, Typography, CircularProgress, IconButton } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import MicOffIcon from '@mui/icons-material/MicOff';
import StopCircleIcon from '@mui/icons-material/StopCircle'; // *** NEW: Import stop icon ***
import axios from 'axios';
import './FarmerChatbot.css';

const FarmerChatbot = () => {
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਆਪਣੀ ਫ਼ਸਲ, ਮੌਸਮ, ਜਾਂ ਮਿੱਟੀ ਬਾਰੇ ਪੁੱਛੋ।' },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false); // *** NEW: State to track audio playback ***

  const recognitionRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("Speech Recognition API is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'pa-IN';

    recognition.onresult = (event) => {
      const spokenText = event.results[0][0].transcript;
      setInput(spokenText);
      setIsListening(false);
      handleSend(spokenText);
    };

    recognition.onend = () => setIsListening(false);
    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  }, []);

  // *** NEW: Function to manually stop the audio ***
  const handleStopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0; // Reset audio to the beginning
      setIsSpeaking(false);
    }
  };

  const handleToggleListening = () => {
    if (!recognitionRef.current) return;

    // *** MODIFIED: Stop speaking before listening ***
    handleStopAudio();

    if (isListening) {
      recognitionRef.current.stop();
    } else {
      setInput('');
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const handleSend = async (queryText = input) => {
    if (!queryText.trim() || loading) return;

    // *** MODIFIED: Stop any previous audio before sending a new request ***
    handleStopAudio();

    const userMessage = { from: 'user', text: queryText };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const chatResponse = await axios.post('http://localhost:7860/chat', {
        query: queryText
      });
      const botTextAnswer = chatResponse.data.answer;
      const botMessage = { from: 'bot', text: botTextAnswer };
      setMessages(prev => [...prev, botMessage]);

      const ttsResponse = await axios.post('http://localhost:7860/synthesize-speech', {
        text: botTextAnswer,
        lang: 'pa'
      }, {
        responseType: 'blob'
      });

      const audioUrl = URL.createObjectURL(ttsResponse.data);
      const audio = new Audio(audioUrl);

      // *** NEW: Add event listeners to track audio state ***
      audio.onplay = () => setIsSpeaking(true);
      audio.onended = () => setIsSpeaking(false);
      audio.onpause = () => setIsSpeaking(false); // Handles manual stop

      audioRef.current = audio;
      audio.play();

    } catch (error) {
      console.error("Error connecting to backend:", error);
      const errorMessage = { from: 'bot', text: 'Sorry, there was an error connecting to the AI service.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} className="chatbot-container">
      <Box className="chatbot-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.from}`}>
            <Typography>{msg.text}</Typography>
          </div>
        ))}
        {loading && <div className="loading-spinner"><CircularProgress size={20} /></div>}
      </Box>
      <Box className="chatbot-input-area">
        <TextField
          fullWidth
          variant="outlined"
          placeholder="ਟਾਈਪ ਕਰੋ ਜਾਂ ਗੱਲ ਕਰਨ ਲਈ ਮਾਈਕ ਦਬਾਓ..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          disabled={loading}
        />

        {/* *** MODIFIED: Conditional rendering for Stop button *** */}
        {isSpeaking ? (
          <IconButton
            color="secondary"
            onClick={handleStopAudio}
            sx={{ ml: 1 }}
          >
            <StopCircleIcon />
          </IconButton>
        ) : (
          <IconButton
            color={isListening ? 'error' : 'primary'}
            onClick={handleToggleListening}
            disabled={loading || !recognitionRef.current}
            sx={{ ml: 1 }}
          >
            {isListening ? <MicOffIcon /> : <MicIcon />}
          </IconButton>
        )}

        <Button variant="contained" onClick={() => handleSend()} disabled={loading || !input.trim()}>
          Send
        </Button>
      </Box>
    </Paper>
  );
};

export default FarmerChatbot;
