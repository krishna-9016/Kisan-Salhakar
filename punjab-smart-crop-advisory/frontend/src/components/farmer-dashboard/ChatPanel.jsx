import React from 'react';
import { Box } from '@mui/material';
import FarmerChatbot from '../FarmerChatbot'; // We will reuse our existing chatbot

const ChatPanel = () => {
  return (
    <Box sx={{ p: { xs: 1, sm: 2, md: 3 } }}>
      <FarmerChatbot />
    </Box>
  );
};

export default ChatPanel;
