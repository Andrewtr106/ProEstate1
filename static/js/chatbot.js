document.addEventListener('DOMContentLoaded', function() {
    // Chatbot elements
    const chatbotWidget = document.getElementById('chatbot-widget');
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotMinimize = document.getElementById('chatbot-minimize');
    const chatbotClose = document.getElementById('chatbot-close');
    const typingIndicator = document.getElementById('typing-indicator');

    let isOpen = false;
    let isMinimized = false;

    // Toggle chatbot window
    chatbotToggle.addEventListener('click', function() {
        if (!isOpen) {
            openChatbot();
        } else {
            closeChatbot();
        }
    });

    // Minimize chatbot
    chatbotMinimize.addEventListener('click', function() {
        if (isMinimized) {
            maximizeChatbot();
        } else {
            minimizeChatbot();
        }
    });

    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        closeChatbot();
    });

    // Send message on button click
    chatbotSend.addEventListener('click', sendMessage);

    // Send message on Enter key
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function openChatbot() {
        chatbotWindow.style.display = 'flex';
        chatbotWidget.classList.add('active');
        isOpen = true;
        isMinimized = false;
        chatbotInput.focus();

        // Add welcome message if no messages exist
        if (chatbotMessages.children.length === 0) {
            addMessage('assistant', 'Hello! I\'m your ProEstate assistant. How can I help you find your perfect property today?');
        }
    }

    function closeChatbot() {
        chatbotWindow.style.display = 'none';
        chatbotWidget.classList.remove('active');
        isOpen = false;
        isMinimized = false;
    }

    function minimizeChatbot() {
        chatbotWindow.classList.add('minimized');
        isMinimized = true;
    }

    function maximizeChatbot() {
        chatbotWindow.classList.remove('minimized');
        isMinimized = false;
        chatbotInput.focus();
    }

    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage('user', message);
        chatbotInput.value = '';

        // Show typing indicator
        showTypingIndicator();

        // Send message to server
        fetch('/chat_api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            hideTypingIndicator();

            if (data.success) {
                addMessage('assistant', data.response);
            } else {
                addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
            }
        })
        .catch(error => {
            hideTypingIndicator();
            console.error('Error:', error);
            addMessage('assistant', 'Sorry, I\'m having trouble connecting. Please check your internet connection and try again.');
        });
    }

    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;

        messageDiv.appendChild(messageContent);
        chatbotMessages.appendChild(messageDiv);

        // Scroll to bottom
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function showTypingIndicator() {
        typingIndicator.classList.remove('d-none');
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function hideTypingIndicator() {
        typingIndicator.classList.add('d-none');
    }

    // Close chatbot when clicking outside
    document.addEventListener('click', function(e) {
        if (!chatbotWidget.contains(e.target) && isOpen) {
            closeChatbot();
        }
    });

    // Prevent closing when clicking inside chatbot
    chatbotWindow.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});
