/**
 * Ponto de entrada do frontend.
 * Coordena chat, painel lateral e dashboard.
 */

import { sendMessage, checkHealth } from './api.js';
import { ChatUI } from './chat.js';
import { PanelUI } from './panel.js';
import { DashboardUI } from './dashboard.js';

const chat = new ChatUI(
    document.getElementById('chat-messages'),
    document.getElementById('ia-loading'),
    document.getElementById('chat-form'),
    document.getElementById('message-input'),
    document.getElementById('response-time'),
    handleSend,
);

const panel = new PanelUI();
const dashboard = new DashboardUI();

async function handleSend(payload) {
    const result = await sendMessage(payload);
    chat.setConversationId(result.conversation_id);
    panel.update(result.analysis);

    if (result.bot_reply) {
        chat.addMessage(result.bot_reply, 'bot');
    }
}

function setupTabs() {
    const tabs = document.querySelectorAll('.tab');
    const views = {
        chat: document.getElementById('chat-view'),
        dashboard: document.getElementById('dashboard-view'),
    };

    tabs.forEach((tab) => {
        tab.addEventListener('click', async () => {
            tabs.forEach((t) => t.classList.remove('active'));
            tab.classList.add('active');

            Object.values(views).forEach((v) => v.classList.remove('active'));
            const target = tab.dataset.tab;
            views[target].classList.add('active');

            if (target === 'dashboard') {
                const metrics = await dashboard.refresh();
                panel.syncEconomy(metrics.total_economy_usd);
            }
        });
    });
}

async function init() {
    setupTabs();
    try {
        const health = await checkHealth();
        chat.addMessage(`Conectado ao ${health.app_name} v${health.version}`, 'system');
    } catch {
        chat.addMessage('API offline — inicie o servidor com: uvicorn app.main:app --reload', 'system');
    }
}

init();
