const messageContainer = document.getElementById('message-container');
const messagesList = document.getElementById('messages-list');
const messageInput = document.getElementById('Message');
const usernameInput = document.getElementById('Username');
const sendButton = document.getElementById('send');
let messageOffset = 0; // To keep track of the loaded messages
const messageLimit = 15; // Number of messages to load at a time
let websocket;

    // Function to fetch messages from the server
async function fetchMessages() {
        const response = await fetch(`/messages?offset=${messageOffset}&limit=${messageLimit}`);
        const data = await response.json();
        messageOffset += data.length; // Update the offset

        data.forEach(msg => {
            const messageElement = document.createElement('li');
            messageElement.className = 'list-group-item p-1 bg-dark border-bottom border-top mt-1';
            messageElement.innerHTML = `<span style="color:${msg.color}">${msg.username}:</span> ${msg.content}`;
            messagesList.appendChild(messageElement);
        });

        // Scroll to the bottom of the message container
        // messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    // Function to send a message via WebSocket
function sendMessage() {
        const messageContent = messageInput.value;
        if (messageContent === '') return;

        const messageData = {
            color: '{{user.color}}',
            username: '{{user.username}}',
            content: messageContent
        };

        websocket.send(JSON.stringify(messageData)); // Send message through WebSocket
        messageInput.value = ''; // Reset the input field
    }

    // Function to initialize WebSocket connection
function initWebSocket() {
        websocket = new WebSocket('ws://localhost:8000/ws/globe/'); // Replace with your WebSocket URL

        websocket.onmessage = function(event) {
            const msg = JSON.parse(event.data);
            const messageElement = document.createElement('li');
            messageElement.className = 'list-group-item p-1 bg-dark border-bottom border-top mt-2';
            messageElement.innerHTML = `<span style="color:${msg.color}">${msg.username}:</span> ${msg.content}`;
            if (messagesList.firstChild) {
                messagesList.insertBefore(messageElement, messagesList.firstChild);
            } else {
                messagesList.appendChild(messageElement); // If no children, just append
            }
            // messagesList.appendChild(messageElement); // Add new message at the bottom
            messageContainer.scrollTop = 0 // Scroll to the bottom
        };

        websocket.onclose = function(event) {
            console.log('WebSocket connection closed:', event);
        };

        websocket.onerror = function(error) {
            console.error('WebSocket error:', error);
        };
    }

    // Event listener for scrolling to load more messages
messageContainer.addEventListener('scroll', () => {
        if (messageContainer.scrollTop + messageContainer.clientHeight >= messageContainer.scrollHeight) {
            fetchMessages(); // Load more messages when scrolled to the top
        }
    });

    // Event listener for sending message on Enter key press
messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage(); // Send message on Enter key press
        }
    });

    // Event listener for the send button
sendButton.addEventListener('click', sendMessage); // Send message on button click

    // Initial fetch of messages and WebSocket connection
fetchMessages();
initWebSocket();
