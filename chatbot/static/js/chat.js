/**
 * Healthcare Chatbot JavaScript
 * Handles WebSocket communication and UI interactions
 */

class HealthcareChatbot {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.messageHistory = [];
        
        this.initializeElements();
        this.initializeSocket();
        this.bindEvents();
        this.updateConnectionStatus(false);
    }
    
    initializeElements() {
        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.chatForm = document.getElementById('chat-form');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.connectionStatus = document.getElementById('connection-status');
        this.clearChatButton = document.getElementById('clear-chat');
        this.quickActionButtons = document.querySelectorAll('.quick-action');
    }
    
    initializeSocket() {
        try {
            this.socket = io();
            
            this.socket.on('connect', () => {
                console.log('Connected to server');
                this.isConnected = true;
                this.updateConnectionStatus(true);
            });
            
            this.socket.on('disconnect', () => {
                console.log('Disconnected from server');
                this.isConnected = false;
                this.updateConnectionStatus(false);
            });
            
            this.socket.on('status', (data) => {
                console.log('Status:', data.message);
            });
            
            this.socket.on('chat_response', (data) => {
                this.hideTypingIndicator();
                this.enableInput();
                
                if (data.status === 'success') {
                    this.addMessage(data.response, 'bot');
                } else {
                    this.addMessage(data.error || 'An error occurred', 'bot', 'error');
                }
            });
            
        } catch (error) {
            console.error('Socket initialization failed:', error);
            this.fallbackToAjax();
        }
    }
    
    bindEvents() {
        // Chat form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Enter key handling
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Clear chat button
        this.clearChatButton.addEventListener('click', () => {
            this.clearChatWithHistory();
        });
        
        // Quick action buttons
        this.quickActionButtons.forEach(button => {
            button.addEventListener('click', () => {
                const message = button.getAttribute('data-message');
                this.messageInput.value = message;
                this.sendMessage();
            });
        });
        
        // Auto-resize input
        this.messageInput.addEventListener('input', () => {
            this.autoResizeInput();
        });
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            this.showError('Please enter a message');
            return;
        }
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageHistory.push({ type: 'user', content: message, timestamp: new Date() });
        
        // Clear input and disable
        this.messageInput.value = '';
        this.disableInput();
        this.showTypingIndicator();
        
        // Send message
        if (this.isConnected && this.socket) {
            this.socket.emit('chat_message', { message: message });
        } else {
            this.sendMessageAjax(message);
        }
    }
    
    sendMessageAjax(message) {
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            this.hideTypingIndicator();
            this.enableInput();
            
            if (data.status === 'success') {
                this.addMessage(data.response, 'bot');
            } else {
                this.addMessage(data.error || 'An error occurred', 'bot', 'error');
            }
        })
        .catch(error => {
            console.error('Ajax request failed:', error);
            this.hideTypingIndicator();
            this.enableInput();
            this.addMessage('Connection error. Please try again.', 'bot', 'error');
        });
    }
    
    addMessage(content, sender, type = 'normal') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user' ? '<i class="bi bi-person"></i>' : '<i class="bi bi-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = `message-bubble ${type === 'error' ? 'error' : ''}`;
        
        // Format content (preserve line breaks and handle pre-formatted text)
        const formattedContent = this.formatMessageContent(content);
        bubbleDiv.innerHTML = formattedContent;
        
        const timeSpan = document.createElement('small');
        timeSpan.className = 'message-time text-muted';
        timeSpan.textContent = this.formatTime(new Date());
        
        contentDiv.appendChild(bubbleDiv);
        contentDiv.appendChild(timeSpan);
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({
            type: sender,
            content: content,
            timestamp: new Date(),
            messageType: type
        });
    }
    
    formatMessageContent(content) {
        // Convert line breaks to HTML
        let formatted = content.replace(/\n/g, '<br>');

        // Handle code blocks or pre-formatted sections
        if (content.includes('Available MCP Tools:') || content.includes('Examples:') || content.includes('Found') && content.includes('patient')) {
            // Check if it's patient data that should be formatted nicely
            if (content.includes('Found') && content.includes('patient')) {
                formatted = this.formatPatientData(content);
            } else {
                formatted = `<pre>${content}</pre>`;
            }
        }

        // Handle bullet points
        formatted = formatted.replace(/^• /gm, '• ');

        // Handle emojis and special formatting
        formatted = formatted.replace(/❌/g, '<span class="text-danger">❌</span>');
        formatted = formatted.replace(/✅/g, '<span class="text-success">✅</span>');
        formatted = formatted.replace(/🏥/g, '<span class="text-primary">🏥</span>');
        formatted = formatted.replace(/👥/g, '<span class="text-info">👥</span>');

        return formatted;
    }

    formatPatientData(content) {
        // Enhanced formatting for comprehensive patient data
        let formatted = content;

        // Format patient headers
        formatted = formatted.replace(/📋 Patient #(\d+)/g, '<div class="patient-header">📋 <strong>Patient #$1</strong></div>');

        // Format patient information with icons and styling
        formatted = formatted.replace(/👤 Name: ([^\n]+)/g, '👤 <strong>Name:</strong> <span class="patient-name">$1</span>');
        formatted = formatted.replace(/🆔 ID: ([^\n]+)/g, '🆔 <strong>ID:</strong> <span class="badge bg-secondary">$1</span>');
        formatted = formatted.replace(/🎂 Age: (\d+)/g, '🎂 <strong>Age:</strong> <span class="text-info">$1</span>');

        // Format medical information
        formatted = formatted.replace(/🏥 Diagnosis: ([^\n]+)/g, '🏥 <strong>Diagnosis:</strong> <span class="text-warning">$1</span>');
        formatted = formatted.replace(/💊 Medications: ([^\n]+)/g, '💊 <strong>Medications:</strong> <span class="text-success">$1</span>');
        formatted = formatted.replace(/⚠️  Allergies: ([^\n]+)/g, '⚠️ <strong>Allergies:</strong> <span class="text-danger">$1</span>');
        formatted = formatted.replace(/📅 Last Updated: ([^\n]+)/g, '📅 <strong>Last Updated:</strong> <span class="text-muted">$1</span>');

        // Format legacy fields
        formatted = formatted.replace(/🏢 Department: ([^\n]+)/g, '🏢 <strong>Department:</strong> <span class="text-primary">$1</span>');
        formatted = formatted.replace(/📊 Status: ([^\n]+)/g, '📊 <strong>Status:</strong> <span class="badge bg-success">$1</span>');
        formatted = formatted.replace(/📆 Admitted: ([^\n]+)/g, '📆 <strong>Admitted:</strong> <span class="text-info">$1</span>');

        return `<div class="patient-data">${formatted}</div>`;
    }
    
    formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'block';
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    disableInput() {
        this.messageInput.disabled = true;
        this.sendButton.disabled = true;
        this.sendButton.innerHTML = '<i class="bi bi-hourglass-split"></i>';
    }
    
    enableInput() {
        this.messageInput.disabled = false;
        this.sendButton.disabled = false;
        this.sendButton.innerHTML = '<i class="bi bi-send"></i>';
        this.messageInput.focus();
    }
    
    updateConnectionStatus(connected) {
        if (connected) {
            this.connectionStatus.className = 'badge bg-success';
            this.connectionStatus.innerHTML = '<i class="bi bi-circle-fill"></i> Connected';
        } else {
            this.connectionStatus.className = 'badge bg-warning';
            this.connectionStatus.innerHTML = '<i class="bi bi-circle-fill"></i> Connecting...';
        }
    }
    
    clearChat() {
        // Keep only the welcome message
        const welcomeMessage = this.chatMessages.querySelector('.message');
        this.chatMessages.innerHTML = '';
        if (welcomeMessage) {
            this.chatMessages.appendChild(welcomeMessage);
        }

        // Clear history except welcome message
        this.messageHistory = this.messageHistory.slice(0, 1);

        this.messageInput.focus();
    }

    clearChatWithHistory() {
        // Clear chat UI
        this.clearChat();

        // Clear conversation history on server
        fetch('/api/clear-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Conversation history cleared on server');
            } else {
                console.error('Error clearing server history:', data.error);
            }
        })
        .catch(error => {
            console.error('Error clearing server history:', error);
        });
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    autoResizeInput() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
    }
    
    showError(message) {
        // Create a temporary error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
        errorDiv.style.top = '20px';
        errorDiv.style.right = '20px';
        errorDiv.style.zIndex = '9999';
        errorDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 3000);
    }
    
    fallbackToAjax() {
        console.log('Falling back to AJAX communication');
        this.updateConnectionStatus(true); // Show as connected for AJAX mode
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new HealthcareChatbot();
    
    // Focus on input initially
    setTimeout(() => {
        document.getElementById('message-input').focus();
    }, 500);
});

// Handle mobile sidebar toggle (if needed)
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('show');
}

// Add mobile menu button if on small screen
if (window.innerWidth <= 768) {
    const header = document.querySelector('.chat-header');
    const menuButton = document.createElement('button');
    menuButton.className = 'btn btn-outline-secondary btn-sm me-2';
    menuButton.innerHTML = '<i class="bi bi-list"></i>';
    menuButton.onclick = toggleSidebar;
    header.querySelector('.d-flex').insertBefore(menuButton, header.querySelector('.avatar'));
}
