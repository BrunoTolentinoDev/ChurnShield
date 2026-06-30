# ChurnShield

Projeto de portfólio que analisa conversas de clientes e tenta identificar sinais de churn (cancelamento).

A ideia principal: **não chamar IA em toda mensagem**. Primeiro roda regras simples em Python. Só se algo parecer estranho é que a API da DeepSeek entra.

## O que tem aqui

- Chat web para simular o atendimento
- Painel lateral mostrando se a IA foi chamada, regras acionadas, risco, custo etc.
- Dashboard com métricas e histórico
- Backend em FastAPI com 5 etapas: Vigia → Despertador → Memória → IA → Automação

## Stack

Python, FastAPI, SQLite, JavaScript (sem framework), DeepSeek API, Pytest.

## Como rodar

```bash
git clone https://github.com/BrunoTolentinoDev/FlowBot-.git
cd FlowBot-

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
```

No `.env`, coloque sua chave da DeepSeek ou use `MOCK_AI=true` para testar sem gastar crédito.

```bash
uvicorn app.main:app --reload
```

Abre no navegador: http://localhost:8000

## Testes

```bash
python -m pytest tests/ -v
```

## Estrutura

```
app/          backend (API + lógica)
frontend/     interface do chat
tests/        testes automatizados
```

A pasta `app/layers/` é onde fica a lógica principal — cada subpasta é uma etapa do pipeline.

## Próximos passos (ideias)

- Integração com WhatsApp via webhook
- Alertas em tempo real quando o risco for alto
- Gráficos no dashboard
- Conexão com CRM (HubSpot, Salesforce)
- Docker e deploy

O chat do site hoje é só uma demo. O motor de análise foi feito separado justamente para facilitar plugar outros canais depois.

## Autor

Bruno Tolentino — projeto para portfólio.
