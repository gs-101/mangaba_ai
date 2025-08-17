# 📝 Glossário Técnico

Definições e explicações dos principais termos utilizados no Mangaba AI. Este glossário irá ajudá-lo a entender melhor a documentação e os conceitos do framework.

## 📋 Índice Alfabético

[A](#a) | [B](#b) | [C](#c) | [D](#d) | [E](#e) | [F](#f) | [G](#g) | [H](#h) | [I](#i) | [J](#j) | [K](#k) | [L](#l) | [M](#m) | [N](#n) | [O](#o) | [P](#p) | [Q](#q) | [R](#r) | [S](#s) | [T](#t) | [U](#u) | [V](#v) | [W](#w) | [X](#x) | [Y](#y) | [Z](#z)

---

## A

### **A2A (Agent-to-Agent)**
**Definição**: Protocolo de comunicação entre agentes que permite troca estruturada de mensagens, coordenação de tarefas e sincronização de workflows.

**Características**:
- Mensagens com prioridade e TTL
- Broadcast para múltiplos agentes
- Handlers customizáveis
- Rate limiting integrado

**Exemplo**:
```python
await agente_a.send_message(
    receiver="agente_b",
    content="dados_processados",
    priority=2,
    ttl=300
)
```

### **Agente (Agent)**
**Definição**: Entidade autônoma de IA que possui uma função específica, pode executar tarefas, manter contexto e comunicar-se com outros agentes.

**Componentes**:
- Nome único
- Role (papel/função)
- Goal (objetivo)
- Tools (ferramentas)
- Model (modelo de IA)

### **API Key**
**Definição**: Chave de autenticação necessária para acessar serviços de IA como Google Gemini, OpenAI, etc.

**Configuração**:
```bash
GEMINI_API_KEY=AIzaSyD...sua_chave_aqui
OPENAI_API_KEY=sk-...sua_chave_aqui
```

### **AsyncIO**
**Definição**: Biblioteca Python para programação assíncrona, fundamental para o funcionamento eficiente do Mangaba AI.

**Uso**:
```python
async def funcao_assincrona():
    resultado = await operacao_demorada()
    return resultado
```

---

## B

### **Broadcast**
**Definição**: Envio simultâneo de mensagem para múltiplos agentes via protocolo A2A.

**Exemplo**:
```python
await coordenador.broadcast_message(
    receivers=["agente1", "agente2", "agente3"],
    content="nova_tarefa",
    priority=2
)
```

### **Busca Semântica**
**Definição**: Funcionalidade do protocolo MCP que permite encontrar contextos relacionados usando similaridade semântica em vez de correspondência exata.

---

## C

### **Cache**
**Definição**: Mecanismo de armazenamento temporário que acelera respostas repetitivas e reduz chamadas desnecessárias para APIs de IA.

**Configuração**:
```bash
CACHE_TTL=3600  # 1 hora
CACHE_ENABLED=true
```

### **Contexto (Context)**
**Definição**: Informações mantidas pelo protocolo MCP sobre conversas, interações e dados relevantes para um agente ou sessão.

**Tipos**:
- Chat history
- User profile  
- Task context
- Session data

### **Conventional Commits**
**Definição**: Padrão de mensagens de commit que facilita automação e clareza no histórico.

**Formato**:
```bash
tipo(escopo): descrição

feat: nova funcionalidade
fix: correção de bug
docs: alteração em documentação
```

---

## D

### **Debug**
**Definição**: Processo de identificação e correção de problemas no código ou comportamento dos agentes.

**Ferramentas**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Deployment**
**Definição**: Processo de colocar o sistema em produção, incluindo configuração de servidores, containers ou serviços de nuvem.

---

## E

### **Environment Variables**
**Definição**: Variáveis de configuração definidas no sistema operacional ou arquivo `.env` que controlam comportamento da aplicação.

**Exemplos**:
```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
```

---

## F

### **Framework**
**Definição**: Estrutura de software que fornece base comum para desenvolvimento de aplicações. O Mangaba AI é um framework para agentes de IA.

### **Fine-tuning**
**Definição**: Processo de treinar um modelo de IA pré-existente com dados específicos para melhorar performance em tarefas particulares.

---

## G

### **Gemini**
**Definição**: Modelo de IA generativa do Google, usado como modelo principal padrão no Mangaba AI.

**Configuração**:
```python
agent = ai.create_agent(
    name="assistente",
    model_provider="gemini",
    model_name="gemini-pro"
)
```

---

## H

### **Handler**
**Definição**: Função que processa mensagens específicas no protocolo A2A, permitindo comportamentos customizados.

**Exemplo**:
```python
async def message_handler(message):
    if message.type == "urgent":
        await process_immediately(message)

agent.a2a_protocol.register_handler(
    message_type="urgent",
    handler=message_handler
)
```

---

## I

### **Integration**
**Definição**: Conexão do Mangaba AI com sistemas externos como Slack, Discord, bancos de dados, APIs, etc.

### **Issue**
**Definição**: Relatório de bug, solicitação de feature ou pergunta registrada no sistema de tracking (GitHub Issues).

---

## J

### **JSON**
**Definição**: Formato de dados usado para configuração, troca de mensagens entre agentes e armazenamento de contexto.

---

## L

### **Log Level**
**Definição**: Configuração que determina verbosidade dos logs do sistema.

**Níveis**:
- `DEBUG`: Informações detalhadas
- `INFO`: Informações gerais
- `WARNING`: Avisos importantes
- `ERROR`: Apenas erros

### **LLM (Large Language Model)**
**Definição**: Modelo de linguagem de grande escala, como GPT, Gemini, Claude, etc., usado pelos agentes para processamento de linguagem natural.

---

## M

### **MCP (Model Context Protocol)**
**Definição**: Protocolo proprietário do Mangaba AI para gerenciamento inteligente de contexto e memória entre modelos e agentes.

**Funcionalidades**:
- Sessões isoladas
- Busca semântica
- Limpeza automática
- Backup/restore

### **Multi-Agent System**
**Definição**: Sistema composto por múltiplos agentes que colaboram para resolver problemas complexos através de comunicação e coordenação.

---

## P

### **Pipeline**
**Definição**: Sequência automatizada de etapas de processamento, desde entrada de dados até saída de resultados.

### **Prioridade (Priority)**
**Definição**: Valor numérico (1-3) que determina urgência de processamento de mensagens A2A.

**Valores**:
- `1`: Baixa prioridade
- `2`: Prioridade normal  
- `3`: Alta prioridade

### **Pull Request (PR)**
**Definição**: Solicitação para incorporar mudanças de código ao repositório principal.

---

## R

### **Rate Limiting**
**Definição**: Controle de quantidade de requisições ou mensagens processadas por unidade de tempo para evitar sobrecarga.

```python
agent.set_rate_limit(
    requests_per_minute=30,
    burst_allowance=5
)
```

### **Role**
**Definição**: Função ou papel específico atribuído a um agente (ex: "Researcher", "Analyst", "Customer Support").

---

## S

### **Sessão (Session)**
**Definição**: Contexto isolado no protocolo MCP que mantém informações específicas de um usuário ou interação.

```python
with agent.mcp_protocol.session("user_123") as session:
    response = await agent.chat("Mensagem", session=session)
```

### **Semantic Search**
**Definição**: Busca baseada em significado e contexto em vez de correspondência literal de texto.

---

## T

### **TTL (Time To Live)**
**Definição**: Tempo de vida de uma mensagem A2A após o qual ela expira e é removida automaticamente.

```python
await agent.send_message(
    receiver="outro_agente",
    content="mensagem",
    ttl=300  # 5 minutos
)
```

### **Tool**
**Definição**: Ferramenta externa que um agente pode usar para executar tarefas específicas (ex: Google Search, calculadora, API externa).

---

## W

### **Workflow**
**Definição**: Sequência estruturada de tarefas executadas por um ou múltiplos agentes para atingir um objetivo específico.

---

## 🔧 Termos Técnicos Específicos

### **Context Fusion**
**Definição**: Processo do MCP que combina múltiplos contextos relacionados em uma representação unificada.

### **Agent Pool**
**Definição**: Conjunto de agentes pré-inicializados mantidos em memória para reutilização eficiente.

### **Message Queue**
**Definição**: Fila de mensagens A2A aguardando processamento, organizada por prioridade.

### **Context Compaction**
**Definição**: Processo de otimização que reduz tamanho do contexto MCP removendo redundâncias.

### **Escalation**
**Definição**: Processo de encaminhar uma tarefa para agente com maior autoridade ou especialização.

---

## 🏗️ Termos de Arquitetura

### **Modular Architecture**
**Definição**: Design que organiza código em módulos independentes e reutilizáveis.

### **Asynchronous Processing**
**Definição**: Processamento que não bloqueia execução, permitindo múltiplas operações simultâneas.

### **Event-Driven Architecture**
**Definição**: Arquitetura baseada em eventos e reações, usada na comunicação A2A.

### **Microservices**
**Definição**: Arquitetura onde agentes podem ser deployados como serviços independentes.

---

## 📊 Termos de Performance

### **Throughput**
**Definição**: Quantidade de mensagens ou tarefas processadas por unidade de tempo.

### **Latency**
**Definição**: Tempo entre envio de requisição e recebimento de resposta.

### **Concurrency**
**Definição**: Capacidade de processar múltiplas tarefas simultaneamente.

### **Resource Pool**
**Definição**: Conjunto de recursos (agentes, conexões, etc.) mantidos para reutilização.

---

## 🔗 Links Relacionados

- **[📖 Visão Geral](visao-geral.md)** - Conceitos fundamentais
- **[🌐 Exemplos de Protocolos](exemplos-protocolos.md)** - A2A e MCP na prática
- **[❓ FAQ](faq.md)** - Perguntas frequentes
- **[🤝 Como Contribuir](contribuicao.md)** - Diretrizes de desenvolvimento

---

> 📝 **Termo não encontrado?** Abra uma [Issue](https://github.com/Mangaba-ai/mangaba_ai/issues/new) ou [Discussion](https://github.com/Mangaba-ai/mangaba_ai/discussions/new) para solicitar a adição de novos termos!