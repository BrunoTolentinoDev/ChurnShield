/** Comunicação com a API REST via Fetch. */

const API_BASE = '';

export async function sendMessage(payload) {
    const response = await fetch(`${API_BASE}/api/chat/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `Erro ${response.status}`);
    }
    return response.json();
}

export async function fetchMetrics() {
    const response = await fetch(`${API_BASE}/api/dashboard/metrics`);
    if (!response.ok) throw new Error('Falha ao carregar métricas');
    return response.json();
}

export async function fetchDecisionHistory(limit = 50) {
    const response = await fetch(`${API_BASE}/api/dashboard/history/decisions?limit=${limit}`);
    if (!response.ok) throw new Error('Falha ao carregar decisões');
    return response.json();
}

export async function fetchAutomationHistory(limit = 50) {
    const response = await fetch(`${API_BASE}/api/dashboard/history/automations?limit=${limit}`);
    if (!response.ok) throw new Error('Falha ao carregar automações');
    return response.json();
}

export async function checkHealth() {
    const response = await fetch(`${API_BASE}/health`);
    return response.json();
}
