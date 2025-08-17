# ❓ Perguntas Frequentes (FAQ)

Esta seção contém respostas para as perguntas mais comuns sobre o Mangaba AI. Se sua dúvida não estiver aqui, consulte as [Issues no GitHub](https://github.com/Mangaba-ai/mangaba_ai/issues) ou abra uma nova pergunta.

## 📋 Índice

1. [Instalação e Configuração](#-instalação-e-configuração)
2. [Primeiros Passos](#-primeiros-passos)
3. [Protocolos A2A e MCP](#-protocolos-a2a-e-mcp)
4. [Desenvolvimento e API](#-desenvolvimento-e-api)
5. [Performance e Otimização](#-performance-e-otimização)
6. [Troubleshooting](#-troubleshooting)
7. [Contribuição e Comunidade](#-contribuição-e-comunidade)

---

## 🔧 Instalação e Configuração

### ❓ Quais são os requisitos mínimos de sistema?

**R:** Os requisitos mínimos são:
- **Python 3.8+** (recomendado 3.10+)
- **4GB RAM** (8GB+ recomendado)
- **2GB espaço em disco** 
- **Conexão com internet** (para APIs de IA)

```bash
# Verificar versão do Python
python --version

# Deve retornar Python 3.8.0 ou superior
```

### ❓ Como obter uma API key do Google Gemini?

**R:** Siga estes passos:

1. **Acesse**: [Google AI Studio](https://aistudio.google.com/)
2. **Faça login** com sua conta Google
3. **Clique em "Get API Key"**
4. **Selecione ou crie um projeto**
5. **Copie a chave gerada**
6. **Configure no .env**:
   ```bash
   GEMINI_API_KEY=AIzaSyD...sua_chave_aqui
   ```

### ❓ É possível usar outros modelos de IA além do Gemini?

**R:** Sim! O Mangaba AI suporta múltiplos provedores:

```python
# Configuração para OpenAI
agent = ai.create_agent(
    name="gpt_agent",
    model_provider="openai",
    model_name="gpt-4"
)

# Configuração para modelos locais (Ollama)
agent = ai.create_agent(
    name="local_agent", 
    model_provider="ollama",
    model_name="llama2"
)
```

### ❓ Como configurar o projeto em ambiente Windows?

**R:** Recomendamos usar WSL2:

```bash
# 1. Instale WSL2
wsl --install

# 2. No WSL2, siga instalação normal Linux
git clone https://github.com/Mangaba-ai/mangaba_ai.git
cd mangaba_ai

# 3. Configure ambiente virtual
python -m venv .venv
source .venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt
```

Alternativamente, use PowerShell:
```powershell
# Use .venv\Scripts\activate.ps1 em vez de source
.venv\Scripts\activate.ps1
```

## 🚀 Primeiros Passos

### ❓ Como criar meu primeiro agente?

**R:** Exemplo básico:

```python
from mangaba_ai import MangabaAI
import asyncio

async def primeiro_agente():
    # Inicializar framework
    ai = MangabaAI()
    
    # Criar agente
    agente = ai.create_agent(
        name="assistente",
        role="Assistente Pessoal",
        goal="Ajudar com tarefas gerais"
    )
    
    # Usar o agente
    resposta = await agente.chat("Olá! Como você pode me ajudar?")
    print(resposta)

# Executar
asyncio.run(primeiro_agente())
```

### ❓ Como fazer agentes conversarem entre si?

**R:** Use o protocolo A2A:

```python
# Agente A envia mensagem para Agente B
await agente_a.send_message(
    receiver="agente_b",
    content="Preciso de análise dos dados X",
    priority=2
)

# Agente B recebe e processa
mensagens = await agente_b.receive_messages()
for msg in mensagens:
    resultado = await agente_b.process(msg.content)
    # Enviar resposta de volta
    await agente_b.send_message(
        receiver=msg.sender,
        content=resultado
    )
```

### ❓ Como manter contexto entre conversas?

**R:** O protocolo MCP gerencia isso automaticamente:

```python
# Primeira conversa
resposta1 = await agente.chat("Meu nome é João e trabalho com vendas")

# Segunda conversa (contexto mantido)
resposta2 = await agente.chat("Qual é meu nome?")
# Resposta: "Seu nome é João"

# Para sessões específicas
with agente.mcp_protocol.session("usuario_123"):
    await agente.chat("Conversa isolada por usuário")
```

## 🌐 Protocolos A2A e MCP

### ❓ Qual a diferença entre protocolos A2A e MCP?

**R:** 

**A2A (Agent-to-Agent)**:
- **Finalidade**: Comunicação entre agentes
- **Uso**: Coordenação, troca de mensagens, workflows
- **Exemplo**: Agente pesquisador envia dados para agente analista

**MCP (Model Context Protocol)**:
- **Finalidade**: Gerenciamento de contexto e memória
- **Uso**: Manter histórico, sessões, contexto de conversas
- **Exemplo**: Lembrar informações do usuário entre sessões

### ❓ Como configurar TTL (Time To Live) para mensagens A2A?

**R:** Configure TTL na configuração ou por mensagem:

```python
# Configuração global
agent.a2a_protocol.set_default_ttl(seconds=3600)  # 1 hora

# Por mensagem específica
await agent.send_message(
    receiver="outro_agente",
    content="Mensagem urgente",
    ttl=300  # 5 minutos
)
```

### ❓ Como limpar contexto MCP antigo?

**R:** Várias opções de limpeza:

```python
# Limpeza automática por tempo
agent.mcp_protocol.set_auto_cleanup(
    max_age_hours=24,
    cleanup_interval_minutes=60
)

# Limpeza manual seletiva
agent.mcp_protocol.clear_context(
    context_type="chat_history",
    older_than_hours=12
)

# Limpeza completa (cuidado!)
agent.mcp_protocol.clear_all_context()
```

### ❓ Como implementar broadcast para múltiplos agentes?

**R:** Use o método broadcast:

```python
# Lista de agentes receptores
receptores = ["agente_1", "agente_2", "agente_3"]

# Envio em broadcast
await coordenador.broadcast_message(
    receivers=receptores,
    content={"task": "analyze_data", "deadline": "2024-01-15"},
    message_type="task_assignment",
    priority=2
)

# Coleta de respostas
respostas = []
for agente_nome in receptores:
    agente = ai.get_agent(agente_nome)
    mensagens = await agente.receive_messages()
    if mensagens:
        resposta = await agente.process_task(mensagens[0])
        respostas.append(resposta)
```

## 💻 Desenvolvimento e API

### ❓ Como estender o framework com novas ferramentas?

**R:** Crie uma classe que herda de `BaseTool`:

```python
from mangaba_ai.core.tools import BaseTool

class MinhaFerramentaCustomizada(BaseTool):
    name = "minha_ferramenta"
    description = "Descrição da ferramenta"
    
    async def execute(self, params: dict) -> dict:
        # Implementar lógica da ferramenta
        resultado = self.processar(params)
        return {"resultado": resultado}
    
    def processar(self, params: dict):
        # Lógica específica
        return "Resultado processado"

# Registrar ferramenta
agent.add_tool(MinhaFerramentaCustomizada())
```

### ❓ Como criar agentes especializados?

**R:** Exemplo de agente especializado:

```python
class AgentePesquisador(MangabaAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Researcher",
            goal="Coletar e analisar informações",
            **kwargs
        )
        
        # Adicionar ferramentas específicas
        self.add_tool(GoogleSearchTool())
        self.add_tool(WebScrapingTool())
        
    async def pesquisar_topico(self, topico: str) -> dict:
        # Implementar lógica de pesquisa
        resultados = await self.tools["google_search"].execute({
            "query": topico,
            "num_results": 10
        })
        
        analise = await self.analisar_resultados(resultados)
        return analise
```

### ❓ Como integrar com APIs externas?

**R:** Crie adaptadores para APIs:

```python
class SlackIntegration:
    def __init__(self, token: str):
        self.client = SlackClient(token)
        
    async def enviar_para_slack(self, canal: str, mensagem: str):
        return await self.client.chat_postMessage(
            channel=canal,
            text=mensagem
        )

# Uso no agente
class AgenteSlack(MangabaAgent):
    def __init__(self, slack_token: str, **kwargs):
        super().__init__(**kwargs)
        self.slack = SlackIntegration(slack_token)
        
    async def notificar_slack(self, mensagem: str):
        await self.slack.enviar_para_slack("#geral", mensagem)
```

## ⚡ Performance e Otimização

### ❓ Como otimizar performance com muitos agentes?

**R:** Implementar estratégias de otimização:

```python
# 1. Pool de agentes
class AgentPool:
    def __init__(self, size: int = 10):
        self.agents = [self.create_agent() for _ in range(size)]
        self.queue = asyncio.Queue()
    
    async def get_agent(self):
        return await self.queue.get()
    
    async def return_agent(self, agent):
        await self.queue.put(agent)

# 2. Processamento batch
async def processar_batch(mensagens: List[str], batch_size: int = 5):
    for i in range(0, len(mensagens), batch_size):
        batch = mensagens[i:i + batch_size]
        tasks = [agent.process(msg) for msg in batch]
        await asyncio.gather(*tasks)

# 3. Cache de respostas
@lru_cache(maxsize=1000)
async def cached_ai_call(prompt: str) -> str:
    return await ai_model.generate(prompt)
```

### ❓ Como monitorar uso de recursos?

**R:** Implemente monitoramento:

```python
import psutil
import time

class ResourceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.initial_memory = psutil.virtual_memory().used
    
    def get_stats(self) -> dict:
        current_memory = psutil.virtual_memory().used
        cpu_percent = psutil.cpu_percent()
        
        return {
            "uptime": time.time() - self.start_time,
            "memory_usage_mb": (current_memory - self.initial_memory) / 1024 / 1024,
            "cpu_percent": cpu_percent,
            "active_agents": len(ai.active_agents)
        }

# Uso
monitor = ResourceMonitor()
stats = monitor.get_stats()
print(f"Memória: {stats['memory_usage_mb']:.1f}MB")
```

### ❓ Como configurar rate limiting?

**R:** Configure limites de requisições:

```python
# Rate limiting por agente
agent.set_rate_limit(
    requests_per_minute=30,
    burst_allowance=5
)

# Rate limiting global
ai.set_global_rate_limit(
    total_requests_per_minute=100,
    per_agent_limit=20
)

# Rate limiting customizado
class CustomRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
    
    async def check_limit(self) -> bool:
        now = time.time()
        # Remove requisições antigas
        self.requests = [req for req in self.requests 
                        if now - req < self.window_seconds]
        
        if len(self.requests) >= self.max_requests:
            return False
            
        self.requests.append(now)
        return True
```

## 🔧 Troubleshooting

### ❓ Como debugar problemas de comunicação A2A?

**R:** Use ferramentas de debug:

```python
# 1. Habilitar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. Monitor de mensagens
class A2AMonitor:
    def __init__(self, agent):
        self.agent = agent
        
    async def monitor_messages(self):
        while True:
            stats = await self.agent.a2a_protocol.get_stats()
            print(f"📊 Mensagens pendentes: {stats['pending']}")
            print(f"📈 Total enviadas: {stats['sent']}")
            print(f"📉 Total recebidas: {stats['received']}")
            await asyncio.sleep(10)

# 3. Verificar conectividade
async def test_connectivity():
    try:
        await agent_a.send_message(
            receiver="agent_b",
            content="ping",
            timeout=5
        )
        print("✅ Comunicação A2A funcionando")
    except TimeoutError:
        print("❌ Timeout na comunicação A2A")
    except Exception as e:
        print(f"❌ Erro: {e}")
```

### ❓ Como resolver problemas de memória MCP?

**R:** Estratégias de diagnóstico e solução:

```python
# 1. Diagnóstico de contexto
def diagnosticar_mcp(agent):
    stats = agent.mcp_protocol.get_context_stats()
    print("📊 Estatísticas MCP:")
    for tipo, dados in stats.items():
        print(f"  {tipo}: {len(dados)} itens, {dados.memory_usage_mb:.1f}MB")
    
    # Verificar contextos expirados
    expired = agent.mcp_protocol.get_expired_contexts()
    print(f"⏰ Contextos expirados: {len(expired)}")

# 2. Limpeza inteligente
async def limpeza_inteligente(agent):
    # Remover contextos menos relevantes
    await agent.mcp_protocol.cleanup_by_relevance(
        keep_top_percent=80,
        max_age_hours=24
    )
    
    # Compactar contextos relacionados
    await agent.mcp_protocol.compact_related_contexts()

# 3. Configuração otimizada
agent.mcp_protocol.configure(
    max_context_size_mb=100,
    auto_cleanup_interval=1800,  # 30 minutos
    compression_enabled=True
)
```

### ❓ Como resolver erros de API key?

**R:** Checklist de diagnóstico:

```python
# 1. Verificar configuração
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    print("❌ GEMINI_API_KEY não configurada")
elif len(gemini_key) < 20:
    print("❌ GEMINI_API_KEY parece incompleta")
else:
    print("✅ GEMINI_API_KEY configurada")

# 2. Testar conectividade
async def test_api_key():
    try:
        # Teste simples
        agent = ai.create_agent("test", "Test", "Test")
        response = await agent.chat("Hello")
        print("✅ API key funcionando")
        return True
    except AuthenticationError:
        print("❌ API key inválida")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

# 3. Verificar limites
async def check_api_limits():
    # Implementar verificação de cota/limites
    usage = await ai.get_api_usage()
    print(f"📊 Uso atual: {usage.requests_today}/{usage.daily_limit}")
```

## 🤝 Contribuição e Comunidade

### ❓ Como contribuir com o projeto?

**R:** Siga estes passos:

1. **Fork o repositório**
2. **Crie uma branch para sua feature**:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. **Faça suas alterações e testes**
4. **Commit com mensagem clara**:
   ```bash
   git commit -m "feat: adiciona funcionalidade X"
   ```
5. **Abra um Pull Request**

Veja o [Guia de Contribuição](contribuicao.md) completo.

### ❓ Como reportar bugs?

**R:** Use o template de bug report no GitHub:

1. **Descreva o problema** claramente
2. **Inclua passos para reproduzir**
3. **Adicione informações do ambiente**:
   ```bash
   python --version
   pip list | grep mangaba
   uname -a
   ```
4. **Anexe logs relevantes**
5. **Mencione comportamento esperado vs atual**

### ❓ Onde buscar ajuda?

**R:** Recursos disponíveis:

- 📖 **[Documentação completa](README.md)** - Início aqui
- 🐛 **[Issues no GitHub](https://github.com/Mangaba-ai/mangaba_ai/issues)** - Bugs e problemas
- 💬 **[Discussions](https://github.com/Mangaba-ai/mangaba_ai/discussions)** - Perguntas e ideias
- 📧 **Email**: suporte@mangaba.ai
- 💬 **Discord**: [Link da comunidade]

### ❓ Como sugerir novas funcionalidades?

**R:** Use GitHub Discussions ou Issues:

1. **Verifique se já não existe** solicitação similar
2. **Descreva a funcionalidade** e motivação
3. **Explique o caso de uso** com exemplos
4. **Considere implementação** se possível
5. **Use labels apropriadas**: `enhancement`, `feature-request`

---

## 🔗 Links Úteis

- 📚 [Documentação Principal](README.md)
- 🚀 [Guia de Instalação](instalacao-configuracao.md) 
- 🌐 [Exemplos de Protocolos](exemplos-protocolos.md)
- 🤝 [Como Contribuir](contribuicao.md)
- 📖 [Visão Geral](visao-geral.md)

---

> ❓ **Não encontrou sua resposta?** Abra uma [Issue](https://github.com/Mangaba-ai/mangaba_ai/issues/new) ou [Discussion](https://github.com/Mangaba-ai/mangaba_ai/discussions/new) no GitHub!