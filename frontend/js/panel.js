/** Painel lateral: status da IA, regras, resumo, métricas. */

export class PanelUI {
    constructor() {
        this.els = {
            iaCalled: document.getElementById('panel-ia-called'),
            callReason: document.getElementById('panel-call-reason'),
            rules: document.getElementById('panel-rules'),
            summary: document.getElementById('panel-summary'),
            risk: document.getElementById('panel-risk'),
            confidence: document.getElementById('panel-confidence'),
            action: document.getElementById('panel-action'),
            tokens: document.getElementById('panel-tokens'),
            cost: document.getElementById('panel-cost'),
            economy: document.getElementById('panel-economy'),
        };
        this.accumulatedEconomy = 0;
    }

    update(analysis) {
        const { ia_called, call_reason, rules_triggered, summary,
                risco_de_churn, confianca, acao, tokens_used,
                cost_usd, economy_usd } = analysis;

        this._setBadge(this.els.iaCalled, ia_called ? 'Sim' : 'Não',
            ia_called ? 'yes' : 'no');

        this.els.callReason.textContent = call_reason || '—';
        this._renderRules(rules_triggered);
        this.els.summary.textContent = summary || '—';

        if (risco_de_churn) {
            this._setBadge(this.els.risk, risco_de_churn, risco_de_churn.toLowerCase());
        } else {
            this._setBadge(this.els.risk, 'N/A', 'neutral');
        }

        this.els.confidence.textContent = confianca != null
            ? `${(confianca * 100).toFixed(0)}%` : '—';
        this.els.action.textContent = acao || '—';
        this.els.tokens.textContent = tokens_used || 0;
        this.els.cost.textContent = `$${(cost_usd || 0).toFixed(6)}`;

        if (economy_usd) this.accumulatedEconomy += economy_usd;
        this.els.economy.textContent = `$${this.accumulatedEconomy.toFixed(6)}`;
    }

    syncEconomy(total) {
        this.accumulatedEconomy = total;
        this.els.economy.textContent = `$${total.toFixed(6)}`;
    }

    _setBadge(el, text, variant) {
        el.textContent = text;
        el.className = `badge ${variant}`;
    }

    _renderRules(rules) {
        this.els.rules.innerHTML = '';
        if (!rules || rules.length === 0) {
            const li = document.createElement('li');
            li.className = 'empty';
            li.textContent = 'Nenhuma';
            this.els.rules.appendChild(li);
            return;
        }
        rules.forEach((rule) => {
            const li = document.createElement('li');
            li.textContent = rule;
            this.els.rules.appendChild(li);
        });
    }
}
