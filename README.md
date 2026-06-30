# ChurnShield 🛡️

Plataforma Full Stack que monitora conversas de clientes e identifica sinais de **churn** (cancelamento/desistência) usando **IA sob demanda** — reduzindo drasticamente custos com APIs de LLM.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)
![Tests](https://img.shields.io/badge/Tests-30%20passing-brightgreen)

---

## Problema Resolvido

Empresas que usam IA em **todas** as mensagens de suporte gastam muito e têm latência alta. O ChurnShield resolve isso com um **pipeline em 5 camadas**:

1. **Regras locais** filtram mensagens sem risco (custo zero)
2. **Decisão inteligente** só chama IA quando necessário
3. **Resumo incremental** envia menos tokens à IA
4. **Análise JSON** estruturada para automação
5. **Pipeline automático** sem intervenção manual

---

## Arquitetura

```
┌─────────────┐     ┌──────────────────────────────────────────────────┐
│  Frontend   │────▶│  FastAPI (REST)                                  │
│  Chat +     │     │  /api/chat/message  /api/dashboard/*  /health   │
│  Dashboard  │◀────│                                                  │
└─────────────┘     └──────────────────────┬───────────────────────────┘
                                           │
                    ┌──────────────────────▼───────────────────────────┐
                    │              MessageService (Orquestrador)          │
                    └──────────────────────┬───────────────────────────┘
                                           │
         ┌─────────────┬───────────┬───────┴───────┬─────────────┐
         ▼             ▼           ▼               ▼             ▼
    ┌─────────┐  ┌───────────┐ ┌─────────┐  ┌──────────┐ ┌───────────┐
    │  VIGIA  │─▶│DESPERTADOR│─▶│ MEMÓRIA │─▶│    IA    │─▶│ AUTOMAÇÃO │
    │ Regras  │  │  Decisão  │ │ Resumo  │  │ DeepSeek │ │  Pipeline │
    └─────────┘  └───────────┘ └─────────┘  └──────────┘ └───────────┘
                                           │
                                    ┌──────▼──────┐
                                    │   SQLite    │
                                    └─────────────┘
```

### Fluxo Completo

```
Mensagem do cliente
       │
       ▼
[VIGIA] ── regras: demora >60s, msg curta, palavras-chave
       │
       ▼
[DESPERTADOR] ── sem regras? → economia registrada, FIM
       │         com regras? → continua
       ▼
[MEMÓRIA] ── atualiza resumo a cada 5 mensagens
       │
       ▼
[IA] ── recebe apenas: resumo + última mensagem → JSON
       │
       ▼
[AUTOMAÇÃO] ── log, DB, sugestão ao cliente, custo, tokens
```

---

## Tecnologias

| Camada | Stack |
|--------|-------|
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| Frontend | HTML5, CSS3, JavaScript ES6+, Fetch API |
| Banco | SQLite |
| IA | DeepSeek API (`deepseek-chat`) |
| Testes | Pytest (30 testes) |
| DevOps | Git, `.env`, Logging |

---

## Estrutura de Pastas

```
FlowBot-/
├── app/
│   ├── main.py                 # Entry point FastAPI
│   ├── config.py               # Settings (.env)
│   ├── api/routes/             # Endpoints REST
│   ├── core/                   # Logging, exceções
│   ├── layers/                 # 5 camadas de inteligência
│   │   ├── vigia/              # Regras locais
│   │   ├── despertador/        # Decisão de chamar IA
│   │   ├── memoria/            # Resumo incremental
│   │   ├── ia/                 # Cliente DeepSeek
│   │   └── automacao/          # Pipeline automático
│   ├── models/                 # ORM + Schemas Pydantic
│   ├── repositories/             # Acesso ao banco
│   └── services/               # Orquestração
├── frontend/
│   ├── index.html              # Chat + Painel + Dashboard
│   ├── css/styles.css
│   └── js/                     # Módulos ES6
├── tests/                      # 30 testes automatizados
├── data/                       # SQLite (runtime)
├── logs/                       # Logs da aplicação
├── .env.example
└── requirements.txt
```

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/BrunoTolentinoDev/FlowBot-.git
cd FlowBot-

# Ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Dependências
pip install -r requirements.txt

# Configuração
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/Mac
```

Edite o `.env`:

```env
DEEPSEEK_API_KEY=sua_chave_aqui   # Opcional: use MOCK_AI=true para testes
MOCK_AI=true                       # Simula IA sem gastar tokens
```

---

## Execução

```bash
# Subir o servidor
uvicorn app.main:app --reload

# Acessar
# http://localhost:8000        → Interface (Chat + Dashboard)
# http://localhost:8000/health → Health check
# http://localhost:8000/docs   → Swagger UI
```

### Rodar Testes

```bash
python -m pytest tests/ -v
```

Resultado esperado: **30 passed**

---

## API Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Status da aplicação |
| POST | `/api/chat/message` | Envia mensagem e executa pipeline |
| GET | `/api/dashboard/metrics` | Métricas agregadas |
| GET | `/api/dashboard/history/decisions` | Histórico de decisões |
| GET | `/api/dashboard/history/automations` | Histórico de automações |

### Exemplo — Enviar Mensagem

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Quero cancelar, está muito caro", "response_time_seconds": 90}'
```

Resposta (resumida):

```json
{
  "conversation_id": "uuid",
  "analysis": {
    "ia_called": true,
    "rules_triggered": ["delay", "keywords"],
    "risco_de_churn": "alto",
    "confianca": 0.91,
    "acao": "Oferecer 15% de desconto e escalonar para retenção"
  }
}
```

---

## Decisões Técnicas

| Decisão | Por quê |
|---------|---------|
| **Regras antes da IA** | 70–90% das mensagens não precisam de LLM — economia real |
| **Resumo incremental** | Reduz tokens enviados à API em até 80% |
| **JSON obrigatório da IA** | Permite automação confiável sem parsing frágil |
| **Repository Pattern** | Desacopla negócio do SQLite — fácil migrar para PostgreSQL |
| **MOCK_AI** | Desenvolvimento e testes sem custo de API |
| **Frontend modular (ES6)** | Separação chat/panel/dashboard sem framework pesado |

---

## Próximas Implementações

O ChurnShield foi arquitetado como **motor de análise desacoplado do canal**. O chat web atual é um adaptador de demonstração — o pipeline central (`MessageService`) pode receber mensagens de qualquer origem sem reescrever a lógica.

### Integrações de Canal (alta prioridade)

- [ ] **Webhook WhatsApp Business API** — receber mensagens via Meta Cloud API ou provedores (Twilio, Z-API, Evolution API) e alimentar o mesmo pipeline
- [ ] **Camada de adaptadores** — padrão Adapter para normalizar mensagens de WhatsApp, chat do site, Instagram DM e e-mail em um único formato interno
- [ ] **Resposta automática no WhatsApp** — quando risco = alto, enviar sugestão de retenção diretamente ao cliente ou alertar atendente humano

### Inteligência e Automação

- [ ] **Score de churn histórico por cliente** — combinar análises ao longo do tempo para prever cancelamento antes da mensagem explícita
- [ ] **Regras configuráveis via painel** — permitir que gestores adicionem palavras-chave e limites sem alterar código
- [ ] **Fila assíncrona (Celery + Redis)** — processar análises de IA em background para alto volume de mensagens
- [ ] **A/B de prompts** — testar diferentes prompts de IA e medir qual gera mais retenção

### Painel e Operação

- [ ] **Dashboard com gráficos** — Chart.js: economia ao longo do tempo, taxa de churn, custo por conversa
- [ ] **Alertas em tempo real** — WebSocket ou SSE para notificar atendentes quando risco alto é detectado
- [ ] **Integração CRM** — HubSpot / Salesforce: criar ticket automático quando churn é identificado
- [ ] **Multi-tenant** — suporte a múltiplas empresas com isolamento de dados e API keys por cliente

### Infraestrutura e Produção

- [ ] **Docker + docker-compose** — subir API, Redis e PostgreSQL com um comando
- [ ] **CI/CD com GitHub Actions** — rodar testes automaticamente em cada push
- [ ] **Migrar SQLite → PostgreSQL** — preparado pela camada Repository, sem alterar regras de negócio
- [ ] **Autenticação JWT** — proteger API e dashboard para uso interno em empresas
- [ ] **Rate limiting e observabilidade** — limitar chamadas à IA e exportar métricas (Prometheus/Grafana)

### Visão de arquitetura futura

```
WhatsApp ──┐
Chat Site ─┼──▶ Adaptadores ──▶ MessageService (cérebro) ──▶ CRM / Alertas
Instagram ─┘         (webhook)         (5 camadas)
```

---

## Perguntas de Entrevista

**P: Por que não usar IA em todas as mensagens?**
> Custo e latência. Regras heurísticas resolvem a maioria dos casos em microssegundos, gratuitamente.

**P: Como você garante que a IA retorna dados utilizáveis?**
> Prompt exige JSON, `response_format: json_object`, validação Pydantic e fallback de parse com regex.

**P: O que acontece se a API DeepSeek cair?**
> Exceção `AIClientError` capturável; em dev, `MOCK_AI=true` simula respostas.

**P: Como escalaria isso?**
> Camadas desacopladas → cada uma vira microserviço; fila (RabbitMQ) entre Despertador e IA; PostgreSQL + read replicas.

**P: Como mede economia?**
> Estima tokens que *seriam* gastos quando IA é evitada, usando mesma fórmula de custo da chamada real.

**P: Dá para integrar com WhatsApp?**
> Sim. O motor já está desacoplado do canal. Basta criar um webhook que converte mensagens do WhatsApp para o formato da API e reutiliza o `MessageService` sem alterar as 5 camadas.

---

## Licença

Projeto de portfólio — uso livre para fins educacionais.
