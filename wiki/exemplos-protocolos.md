# 🌐 Exemplos dos Protocolos A2A e MCP

Este guia fornece exemplos práticos e detalhados dos protocolos A2A (Agent-to-Agent) e MCP (Model Context Protocol) utilizados no Mangaba AI.

## 📋 Índice

1. [Protocolo MCP](#-protocolo-mcp)
2. [Protocolo A2A](#-protocolo-a2a)
3. [Integração dos Protocolos](#-integração-dos-protocolos)
4. [Casos de Uso Avançados](#-casos-de-uso-avançados)
5. [Troubleshooting](#-troubleshooting)

---

## 🧠 Protocolo MCP

O **Model Context Protocol (MCP)** gerencia o contexto e a memória dos agentes de forma inteligente e estruturada.

### Exemplo Básico - Chat com Contexto

```python
from mangaba_ai import MangabaAI
import asyncio

async def exemplo_mcp_basico():
    # Inicializa o agente com MCP
    ai = MangabaAI()
    agent = ai.create_agent(
        name="assistente",
        role="Assistente Pessoal",
        goal="Ajudar com tarefas diversas mantendo contexto"
    )
    
    # Primeira interação - estabelece contexto
    resposta1 = await agent.chat("Olá! Estou aprendendo Python.")
    print(f"Agente: {resposta1}")
    
    # Segunda interação - usa contexto anterior
    resposta2 = await agent.chat("Que bibliotecas você recomenda?")
    print(f"Agente: {resposta2}")
    # Resultado: "Para Python, recomendo pandas, numpy e matplotlib..."
```

### Gerenciamento de Sessões MCP

```python
async def exemplo_sessoes_mcp():
    ai = MangabaAI()
    agent = ai.create_agent(name="multi_user", role="Atendente")
    
    # Sessão do usuário A
    with agent.mcp_protocol.session("usuario_a") as sessao_a:
        await agent.chat("Sou João, trabalho com vendas", session=sessao_a)
        resposta_a = await agent.chat("Qual meu nome?", session=sessao_a)
        print(f"Para João: {resposta_a}")  # "Seu nome é João"
    
    # Sessão do usuário B (contexto isolado)
    with agent.mcp_protocol.session("usuario_b") as sessao_b:
        await agent.chat("Sou Maria, trabalho com marketing", session=sessao_b)
        resposta_b = await agent.chat("Qual meu nome?", session=sessao_b)
        print(f"Para Maria: {resposta_b}")  # "Seu nome é Maria"
```

### Resumo e Gestão de Contexto

```python
# Obter resumo do contexto atual
resumo = agent.get_context_summary()
print("📝 Resumo do Contexto:")
for tipo, dados in resumo.items():
    print(f"  {tipo}: {len(dados)} itens")

# Exemplo de saída:
# 📝 Resumo do Contexto:
#   chat_history: 5 itens
#   analysis_results: 2 itens
#   user_profile: 1 itens
#   project_info: 1 itens

# Limpeza seletiva de contexto
agent.mcp_protocol.clear_context(context_type="chat_history")

# Exportar contexto para backup
contexto_backup = agent.mcp_protocol.export_context()
```

### Busca Semântica no Contexto

```python
async def exemplo_busca_semantica():
    # Adiciona várias informações ao contexto
    await agent.chat("Trabalho na empresa TechCorp desde 2020")
    await agent.chat("Meu projeto atual é sobre IA generativa")
    await agent.chat("Tenho mestrado em Ciência da Computação")
    
    # Busca por informações relacionadas
    resultados = await agent.mcp_protocol.semantic_search(
        query="formação acadêmica",
        limit=3
    )
    
    for resultado in resultados:
        print(f"📚 {resultado.content} (score: {resultado.relevance})")
    # Saída: "Tenho mestrado em Ciência da Computação (score: 0.85)"
```

---

## 🔗 Protocolo A2A

O **Agent-to-Agent Protocol (A2A)** permite comunicação estruturada entre agentes.

### Comunicação Básica Entre Agentes

```python
async def exemplo_a2a_basico():
    ai = MangabaAI()
    
    # Cria agentes especializados
    pesquisador = ai.create_agent(
        name="pesquisador",
        role="Researcher",
        goal="Coletar informações"
    )
    
    analista = ai.create_agent(
        name="analista", 
        role="Analyst",
        goal="Analisar dados"
    )
    
    # Pesquisador coleta dados
    dados = await pesquisador.research("tendências de IA em 2024")
    
    # Envia dados para o analista via A2A
    await pesquisador.send_message(
        receiver="analista",
        content=dados,
        message_type="research_data",
        priority=1
    )
    
    # Analista processa os dados recebidos
    analise = await analista.receive_and_process()
    print(f"📊 Análise: {analise}")
```

### Sistema de Mensagens com Prioridade

```python
async def exemplo_priorizacao_a2a():
    # Configuração de handlers por prioridade
    async def handler_urgente(message):
        print(f"🚨 URGENTE: {message.content}")
        # Processa imediatamente
        
    async def handler_normal(message):
        print(f"📝 Normal: {message.content}")
        # Adiciona à fila de processamento
        
    async def handler_baixa(message):
        print(f"ℹ️ Info: {message.content}")
        # Processa quando há recursos disponíveis
    
    # Registra handlers
    analista.a2a_protocol.register_handler(
        priority=3, handler=handler_urgente
    )
    analista.a2a_protocol.register_handler(
        priority=2, handler=handler_normal
    )
    analista.a2a_protocol.register_handler(
        priority=1, handler=handler_baixa
    )
    
    # Envia mensagens com diferentes prioridades
    await pesquisador.send_message(
        receiver="analista",
        content="Sistema fora do ar!",
        priority=3,  # Urgente
        ttl=300      # 5 minutos TTL
    )
```

### Broadcast para Múltiplos Agentes

```python
async def exemplo_broadcast():
    # Cria equipe de agentes
    equipe = [
        ai.create_agent(name=f"agente_{i}", role="Worker")
        for i in range(3)
    ]
    
    coordenador = ai.create_agent(name="coordenador", role="Coordinator")
    
    # Coordenador envia tarefa para toda equipe
    await coordenador.broadcast_message(
        receivers=["agente_0", "agente_1", "agente_2"],
        content={
            "task": "analyze_document",
            "document_id": "doc_123",
            "deadline": "2024-01-15"
        },
        message_type="task_assignment"
    )
    
    # Coleta respostas de todos os agentes
    respostas = []
    for agente in equipe:
        resposta = await agente.receive_messages()
        if resposta:
            resultado = await agente.process_task(resposta[0])
            respostas.append(resultado)
    
    return respostas
```

### Sistema Multi-Agente Complexo

```python
class SistemaAnaliseDocumentos:
    def __init__(self):
        self.ai = MangabaAI()
        self.extrator = self.ai.create_agent(
            name="extrator", role="Text Extractor"
        )
        self.analisador = self.ai.create_agent(
            name="analisador", role="Content Analyzer"
        )
        self.sumarizador = self.ai.create_agent(
            name="sumarizador", role="Summarizer"
        )
    
    async def processar_documento(self, documento):
        # 1. Extração de texto
        await self.extrator.send_message(
            receiver="analisador",
            content={"raw_document": documento},
            message_type="extract_text"
        )
        
        # 2. Análise de conteúdo
        texto_extraido = await self.analisador.receive_and_process()
        await self.analisador.send_message(
            receiver="sumarizador",
            content={"analyzed_text": texto_extraido},
            message_type="analyze_content"
        )
        
        # 3. Sumarização final
        relatorio_final = await self.sumarizador.receive_and_process()
        
        return relatorio_final

# Uso
sistema = SistemaAnaliseDocumentos()
documento = "Este é um documento muito bom sobre IA..."
resultado = sistema.processar_documento(documento)
print(f"📄 Relatório: {resultado}")
```

---

## 🔄 Integração dos Protocolos

### Exemplo Completo: Sistema de Atendimento Inteligente

```python
class AtendimentoInteligente:
    def __init__(self):
        self.ai = MangabaAI()
        
        # Agente principal com MCP para contexto do cliente
        self.atendente = self.ai.create_agent(
            name="atendente",
            role="Customer Service",
            goal="Atender clientes com excelência"
        )
        
        # Agente especialista para casos complexos
        self.especialista = self.ai.create_agent(
            name="especialista",
            role="Technical Specialist",
            goal="Resolver problemas técnicos"
        )
        
        # Supervisor para escalonamento
        self.supervisor = self.ai.create_agent(
            name="supervisor",
            role="Service Supervisor",
            goal="Garantir qualidade do atendimento"
        )
    
    async def atender_cliente(self, mensagem_cliente, historico_cliente=None):
        # 1. MCP: Carrega contexto do cliente
        if historico_cliente:
            await self.atendente.mcp_protocol.add_context(
                context_type="customer_history",
                content=historico_cliente
            )
        
        # 2. Atendimento inicial
        resposta_inicial = await self.atendente.chat(mensagem_cliente)
        
        # 3. A2A: Verifica se precisa de especialista
        if self.atendente.analysis.complexity_score > 0.7:
            await self.atendente.send_message(
                receiver="especialista",
                content={
                    "customer_message": mensagem_cliente,
                    "context": historico_cliente,
                    "initial_analysis": resposta_inicial
                },
                message_type="escalation_request",
                priority=2
            )
            
            resposta_especialista = await self.especialista.receive_and_process()
            
            # 4. A2A: Supervisor avalia a solução
            resposta = await self.supervisor.send_request(
                "Supervisor", "avaliar_caso",
                {"caso": mensagem_cliente, "contexto": historico_cliente}
            )
        
        return resposta

# Uso
atendimento = AtendimentoInteligente()
resposta = atendimento.atender_cliente(
    "Meu software não está funcionando após a atualização",
    historico_cliente="Cliente premium há 2 anos, última compra em dezembro"
)
```

---

## 🚀 Casos de Uso Avançados

### 1. Sistema de Atendimento Multi-Agente

```python
class SistemaAtendimento:
    async def processar_ticket(self, ticket):
        # Triagem automática
        categoria = await self.triagem.classify(ticket.content)
        
        # Roteamento baseado em especialização
        agente_especializado = self.get_agente_by_category(categoria)
        
        # Processamento com contexto
        with agente_especializado.mcp_protocol.session(ticket.user_id):
            resposta = await agente_especializado.process(ticket)
        
        return resposta
```

### 2. Rede de Agentes de Pesquisa

```python
class RedeIAdePesquisa:
    def __init__(self):
        self.coordenador = self.create_coordinator()
        self.pesquisadores = self.create_research_team()
        self.sintetizador = self.create_synthesizer()
    
    async def pesquisar_topico(self, topico, profundidade="media"):
        # 1. Coordenador divide a pesquisa
        subtopicos = await self.coordenador.divide_research(topico)
        
        # 2. A2A: Distribui subtópicos para pesquisadores
        tarefas = []
        for i, subtopico in enumerate(subtopicos):
            pesquisador = self.pesquisadores[i % len(self.pesquisadores)]
            tarefa = pesquisador.research_async(subtopico)
            tarefas.append(tarefa)
        
        # 3. Coleta resultados
        resultados = await asyncio.gather(*tarefas)
        
        # 4. MCP: Síntese com contexto completo
        await self.sintetizador.mcp_protocol.add_bulk_context(resultados)
        sintese_final = await self.sintetizador.synthesize(topico)
        
        return {
            "topico": topico,
            "resultados_individuais": resultados,
            "sintese": sintese_final
        }

# Uso
rede = RedeIAdePesquisa()
relatorio = rede.pesquisar_topico(
    "Impacto da IA Generativa no Mercado de Trabalho",
    profundidade="alta"
)
```

---

## 🔍 Troubleshooting

### Problemas Comuns MCP

#### **Contexto Perdido**
```python
# Diagnóstico
stats = agent.mcp_protocol.get_context_stats()
print(f"Contextos ativos: {stats}")

# Solução: Verificar TTL e limpeza automática
agent.mcp_protocol.set_context_ttl(seconds=3600)  # 1 hora
```

#### **Memória Excessiva**
```python
# Limpar contextos antigos
agent.mcp_protocol.cleanup_expired_contexts()

# Configurar limpeza automática
agent.mcp_protocol.enable_auto_cleanup(interval=1800)  # 30 min
```

### Problemas Comuns A2A

#### **Mensagens Perdidas**
```python
# Verificar fila de mensagens
pending = agent.a2a_protocol.get_pending_messages()
print(f"Mensagens pendentes: {len(pending)}")

# Reprocessar mensagens perdidas
for msg in pending:
    await agent.a2a_protocol.retry_message(msg.id)
```

#### **Sobrecarga de Comunicação**
```python
# Configurar rate limiting
agent.a2a_protocol.set_rate_limit(
    messages_per_minute=60,
    burst_size=10
)

# Priorização inteligente
agent.a2a_protocol.enable_smart_prioritization()
```

### Debug e Monitoramento

```python
# Ativar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)

# Monitor de contexto MCP
def monitor_mcp(agent):
    contextos = agent.mcp_protocol.get_context_stats()
    print(f"📊 Contextos: {contextos}")

# Monitor de conexões A2A
def monitor_a2a(agent):
    conexoes = agent.protocols["a2a"].get_connection_status()
    print(f"🔗 Conexões A2A: {conexoes}")
```

---

> 🎯 **Próximos Passos**: Agora que você domina os protocolos, explore as [Melhores Práticas](melhores-praticas.md) para otimizar seus agentes!