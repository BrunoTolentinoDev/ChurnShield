/** Lógica do chat: mensagens, auto-scroll, loading. */

export class ChatUI {
    constructor(container, loadingEl, form, inputEl, timeEl, onSend) {
        this.container = container;
        this.loadingEl = loadingEl;
        this.form = form;
        this.inputEl = inputEl;
        this.timeEl = timeEl;
        this.onSend = onSend;
        this.conversationId = null;

        this.form.addEventListener('submit', (e) => this._handleSubmit(e));
    }

    async _handleSubmit(event) {
        event.preventDefault();
        const content = this.inputEl.value.trim();
        if (!content) return;

        const responseTime = this.timeEl.value ? parseFloat(this.timeEl.value) : null;

        this.addMessage(content, 'user');
        this.inputEl.value = '';
        this.setLoading(true);

        try {
            await this.onSend({
                conversation_id: this.conversationId,
                content,
                response_time_seconds: responseTime,
            });
        } catch (error) {
            this.addMessage(`Erro: ${error.message}`, 'system');
        } finally {
            this.setLoading(false);
        }
    }

    addMessage(text, role = 'user') {
        const div = document.createElement('div');
        div.className = `message ${role}`;
        div.textContent = text;
        this.container.appendChild(div);
        this.scrollToBottom();
    }

    setConversationId(id) {
        this.conversationId = id;
    }

    setLoading(active) {
        this.loadingEl.classList.toggle('hidden', !active);
        this.form.querySelector('button').disabled = active;
        if (active) this.scrollToBottom();
    }

    scrollToBottom() {
        this.container.scrollTop = this.container.scrollHeight;
    }
}
