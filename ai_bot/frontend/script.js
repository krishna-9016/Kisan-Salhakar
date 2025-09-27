// frontend/script.js

document.addEventListener('DOMContentLoaded', () => {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const chatBox = document.getElementById('chat-box');

    // The URL of the backend API. Change this if your backend is running elsewhere.
    const API_URL = 'http://127.0.0.1:7860/chat';

    messageForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the form from reloading the page

        const userMessage = messageInput.value.trim();
        if (!userMessage) return;

        // Display the user's message in the chat box
        appendMessage(userMessage, 'user-message');

        // Clear the input field
        messageInput.value = '';

        // Show a typing indicator while waiting for the AI's response
        const typingIndicator = showTypingIndicator();

        try {
            // Send the user's message to the backend API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: userMessage }),
            });

            // Remove the typing indicator once we have a response
            hideTypingIndicator(typingIndicator);

            if (!response.ok) {
                // Handle HTTP errors
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const aiMessage = data.answer;

            // Display the AI's response
            appendMessage(aiMessage, 'ai-message');

        } catch (error) {
            console.error('Error:', error);
            // Display an error message in the chat box
            appendMessage(`An error occurred: ${error.message}`, 'ai-message error');
        }
    });

    function appendMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        
        const p = document.createElement('p');
        p.textContent = message;
        messageElement.appendChild(p);
        
        chatBox.appendChild(messageElement);
        
        // Automatically scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        const indicatorElement = document.createElement('div');
        indicatorElement.classList.add('message', 'ai-message', 'typing-indicator');
        indicatorElement.innerHTML = `<span></span><span></span><span></span>`;
        chatBox.appendChild(indicatorElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        return indicatorElement;
    }

    function hideTypingIndicator(indicatorElement) {
        if (indicatorElement) {
            chatBox.removeChild(indicatorElement);
        }
    }
});