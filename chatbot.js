async function getChatBotResponse(userMessage) {
    try {
        const responseData = await api.sendMessage(userMessage);
        return responseData; // Return full object {response, action}
    } catch (error) {
        console.error('Chatbot error:', error);
        return { response: "I'm having trouble connecting. Please try again.", action: null };
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    addUserMessage(message);
    input.value = '';

    addTypingIndicator();

    const data = await getChatBotResponse(message);
    removeTypingIndicator();
    addBotMessage(data.response);

    if (data.action === 'redirect_assessment') {
        setTimeout(() => {
            showPatientView('assessment');
        }, 1500);
    }
}

function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.style.cssText = 'display: flex; justify-content: flex-end; margin-bottom: 16px;';
    div.innerHTML = `<div style="padding: 14px 18px; border-radius: 18px 18px 4px 18px; background: #14b8a6; color: white; max-width: 70%;">${message}</div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.style.cssText = 'display: flex; gap: 10px; margin-bottom: 16px;';
    div.innerHTML = `<div style="font-size: 18px;">🍃</div><div style="padding: 14px 18px; border-radius: 18px 18px 18px 4px; background: var(--bg-card); border: 2px solid #14b8a6; color: var(--text-primary); max-width: 70%;">${message}</div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.id = 'typingIndicator';
    div.style.cssText = 'display: flex; gap: 10px; margin-bottom: 16px;';
    div.innerHTML = `<div style="font-size: 18px;">🍃</div><div style="padding: 14px 18px; border-radius: 18px; background: var(--bg-card); border: 2px solid #14b8a6; color: var(--text-primary);">Typing...</div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

function handleChatEnter(event) {
    if (event.key === 'Enter') sendChatMessage();
}

// UI Functions for Chatbot
function navigateChatFrame(frameId) {
    document.querySelectorAll('.chatbot-frame').forEach(el => el.style.display = 'none');
    document.getElementById(frameId).style.display = 'flex';
}

function handleQuickAction(action) {
    const prompts = {
        'prakriti': 'I want to take the Prakriti Assessment',
        'diet': 'Can you suggest a diet plan?',
        'yoga': 'What yoga should I do?',
        'stress': 'How to manage stress?'
    };
    const message = prompts[action] || action;
    const input = document.getElementById('chatInput');
    input.value = message;
    sendChatMessage();
}