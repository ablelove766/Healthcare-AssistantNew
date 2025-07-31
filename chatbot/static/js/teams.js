class TeamsHealthcareChatbot {
    constructor() {
        // Initialize Teams SDK
        microsoftTeams.app.initialize();

        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.chatForm = document.getElementById('chat-form');
        this.clearChatButton = document.getElementById('clear-chat');
        this.socket = null;
        this.isConnected = false;
        this.messageHistory = [];

        this.initializeTeamsContext();
        this.initializeSocket();
        this.bindEvents();
    }

    async initializeTeamsContext() {
        try {
            const context = await microsoftTeams.app.getContext();
            console.log('Teams context:', context);

            // Notify Teams that app is ready
            microsoftTeams.app.notifySuccess();
        } catch (error) {
            console.error('Teams initialization error:', error);
        }
    }

    initializeSocket() {
        try {
            this.socket = io();

            this.socket.on('connect', () => {
                console.log('Connected to server');
                this.isConnected = true;
            });

            this.socket.on('disconnect', () => {
                console.log('Disconnected from server');
                this.isConnected = false;
            });

            this.socket.on('chat_response', (data) => {
                if (data.error) {
                    this.addMessage('Error: ' + data.error, 'bot');
                } else {
                    this.addMessage(data.response, 'bot');
                }
                this.enableInput();
            });
        } catch (error) {
            console.error('Socket initialization error:', error);
        }
    }

    bindEvents() {
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        this.clearChatButton.addEventListener('click', () => {
            this.clearChat();
        });

        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.isConnected) return;

        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.disableInput();

        this.socket.emit('chat_message', { message: message });
        this.messageHistory.push({ type: 'user', content: message });
    }

    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        const messageBubble = document.createElement('div');
        messageBubble.className = 'message-bubble';
        messageBubble.innerHTML = this.formatMessage(content);

        messageContent.appendChild(messageBubble);
        messageDiv.appendChild(messageContent);
        this.chatMessages.appendChild(messageDiv);

        this.scrollToBottom();
    }

    formatMessage(content) {
        return content.replace(/\n/g, '<br>');
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    disableInput() {
        this.messageInput.disabled = true;
        this.messageInput.placeholder = 'Processing...';
    }

    enableInput() {
        this.messageInput.disabled = false;
        this.messageInput.placeholder = 'Ask about patients...';
        this.messageInput.focus();
    }

    clearChat() {
        // Clear messages except welcome message
        const messages = this.chatMessages.querySelectorAll('.message:not(:first-child)');
        messages.forEach(msg => msg.remove());

        // Clear history
        this.messageHistory = [];

        // Call API to clear server-side history
        fetch('/api/clear-chat', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('Chat cleared:', data.message);
            })
            .catch(error => {
                console.error('Error clearing chat:', error);
            });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.teamsChatbot = new TeamsHealthcareChatbot();
});