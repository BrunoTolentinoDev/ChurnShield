/** Dashboard de métricas e históricos. */

import { fetchMetrics, fetchDecisionHistory, fetchAutomationHistory } from './api.js';

export class DashboardUI {
    constructor() {
        this.metricEls = {
            messages: document.getElementById('metric-messages'),
            aiCalls: document.getElementById('metric-ai-calls'),
            avoided: document.getElementById('metric-avoided'),
            economyPct: document.getElementById('metric-economy-pct'),
            tokens: document.getElementById('metric-tokens'),
            cost: document.getElementById('metric-cost'),
            saved: document.getElementById('metric-saved'),
        };
        this.decisionsTable = document.getElementById('decisions-table');
        this.automationsTable = document.getElementById('automations-table');
    }

    async refresh() {
        const [metrics, decisions, automations] = await Promise.all([
            fetchMetrics(),
            fetchDecisionHistory(),
            fetchAutomationHistory(),
        ]);

        this._renderMetrics(metrics);
        this._renderDecisions(decisions);
        this._renderAutomations(automations);

        return metrics;
    }

    _renderMetrics(m) {
        this.metricEls.messages.textContent = m.total_messages;
        this.metricEls.aiCalls.textContent = m.ai_calls;
        this.metricEls.avoided.textContent = m.ai_calls_avoided;
        this.metricEls.economyPct.textContent = `${m.economy_percent}%`;
        this.metricEls.tokens.textContent = m.tokens_used;
        this.metricEls.cost.textContent = `$${m.total_cost_usd.toFixed(4)}`;
        this.metricEls.saved.textContent = `$${m.total_economy_usd.toFixed(4)}`;
    }

    _renderDecisions(decisions) {
        this.decisionsTable.innerHTML = decisions.length === 0
            ? '<tr><td colspan="6" style="text-align:center;color:var(--text-muted)">Sem dados</td></tr>'
            : decisions.map((d) => `
                <tr>
                    <td>${this._formatDate(d.created_at)}</td>
                    <td>${d.ai_called ? '✅' : '❌'}</td>
                    <td>${d.rules_triggered.join(', ') || '—'}</td>
                    <td>${d.risco_de_churn || '—'}</td>
                    <td>$${d.cost_usd.toFixed(6)}</td>
                    <td>$${d.economy_usd.toFixed(6)}</td>
                </tr>
            `).join('');
    }

    _renderAutomations(logs) {
        this.automationsTable.innerHTML = logs.length === 0
            ? '<tr><td colspan="3" style="text-align:center;color:var(--text-muted)">Sem dados</td></tr>'
            : logs.map((l) => `
                <tr>
                    <td>${this._formatDate(l.created_at)}</td>
                    <td>${l.action_type}</td>
                    <td>${l.details}</td>
                </tr>
            `).join('');
    }

    _formatDate(iso) {
        return new Date(iso).toLocaleString('pt-BR', {
            day: '2-digit', month: '2-digit',
            hour: '2-digit', minute: '2-digit',
        });
    }
}
