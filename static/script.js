 document.addEventListener('DOMContentLoaded', function() {
    console.log('Brainware Chatbot loaded!');
    // Set initial time
    const initialTime = document.getElementById('initialTime');
    const suggestionTime = document.getElementById('suggestionTime');
    if (initialTime) initialTime.textContent = getCurrentTime();
    if (suggestionTime) suggestionTime.textContent = getCurrentTime();
});

function getCurrentTime() {
    return new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false 
    });
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendSuggestion(text) {
    document.getElementById('messageInput').value = text;
    sendMessage();
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) {
        alert('Please type a message first!');
        return;
    }
    
    console.log('Sending message:', message);
    
    // Add user message to chat
    addUserMessage(message);
    messageInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message 
            })
        });
        
        console.log('Response status:', response.status);
        
        const data = await response.json();
        console.log('Response data:', data);
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Add bot response to chat
        if (data.bot_response && data.bot_response.text) {
            addBotMessage(data.bot_response);
        } else {
            throw new Error('Invalid response format');
        }
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addBotMessage({
            text: 'Sorry, I encountered an error. Please try again.',
            actions: []
        });
    }
}

function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${escapeHtml(message)}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addBotMessage(response) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    let actionsHtml = '';
    if (response.actions && response.actions.length > 0) {
        actionsHtml = `
            <div class="action-buttons">
                ${response.actions.map(action => `
                    <button class="action-btn ${action.type}-btn" 
                            onclick="handleAction('${action.type}', '${escapeHtml(action.value)}')">
                        ${action.label}
                    </button>
                `).join('')}
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${formatMessage(response.text)}</div>
            ${actionsHtml}
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function handleAction(type, value) {
    console.log(`Action: ${type}, Value: ${value}`);
    
    switch(type) {
        case 'email':
            window.location.href = `mailto:${value}`;
            break;
        case 'phone':
            window.location.href = `tel:${value}`;
            break;
        case 'website':
        case 'maps':
        case 'gallery':  // New gallery action
            window.open(value, '_blank');
            break;
        default:
            console.log('Unknown action type:', type);
    }
}

function formatMessage(text) {
    // Convert line breaks and basic formatting
    return escapeHtml(text).replace(/\n/g, '<br>');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typingIndicator';
    
    typingDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

function removeTypingIndicator() {
    const typing = document.getElementById('typingIndicator');
    if (typing) typing.remove();
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add CSS for typing animation and gallery button
const style = document.createElement('style');
style.textContent = `
    .typing-dots {
        display: flex;
        gap: 4px;
        padding: 8px 0;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    .typing-dots span:nth-child(3) { animation-delay: 0s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    
    .gallery-btn {
        background: #fff8e1 !important;
        color: #ff8f00 !important;
        border: 1px solid #ffecb3 !important;
    }
    
    .gallery-btn:hover {
        background: #ffecb3 !important;
        transform: translateY(-2px);
    }
`;
document.head.appendChild(style);