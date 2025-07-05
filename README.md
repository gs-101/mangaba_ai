# 🥭 Mangaba AI

[![PyPI version](https://img.shields.io/pypi/v/mangaba.svg)](https://pypi.org/project/mangaba/)
[![Python](https://img.shields.io/pypi/pyversions/mangaba.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/usuario/mangaba-ai/actions)

Repositório minimalista para criação de agentes de IA inteligentes e versáteis com protocolos **A2A** (Agent-to-Agent) e **MCP** (Model Context Protocol).

## ✨ Características Principais

- 🤖 **Agente de IA Versátil**: Suporte a qualquer provedor de IA
- 🔗 **Protocolo A2A**: Comunicação entre agentes
- 🧠 **Protocolo MCP**: Gerenciamento avançado de contexto
- 📝 **Funcionalidades Integradas**: Chat, análise, tradução e mais
- ⚡ **Configuração Simples**: Apenas 2 passos para começar

## 🚀 Instalação Rápida

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração (Apenas 2 passos!)

1. Copie o arquivo de exemplo:
```bash
copy .env.example .env
```

2. Configure sua chave de API no arquivo `.env`:
```
API_KEY=sua_chave_api_aqui
MODEL=modelo_desejado
```

## 📖 Uso Super Simples

```python
from mangaba_ai import MangabaAgent

# Inicializar com protocolos A2A e MCP habilitados
agent = MangabaAgent()

# Chat com contexto automático
resposta = agent.chat("Olá! Como você pode me ajudar?")
print(resposta)
```

## 🎯 Exemplos Práticos

### Chat Básico com Contexto MCP
```python
from mangaba_ai import MangabaAgent

agent = MangabaAgent()

# O contexto é mantido automaticamente
print(agent.chat("Meu nome é João"))
print(agent.chat("Qual é o meu nome?"))  # Lembra do contexto anterior
```

### Análise de Texto
```python
agent = MangabaAgent()
text = "A inteligência artificial está transformando o mundo."
analysis = agent.analyze_text(text, "Faça uma análise detalhada")
print(analysis)
```

### Tradução
```python
agent = MangabaAgent()
translation = agent.translate("Hello, how are you?", "português")
print(translation)
```

### Resumo do Contexto
```python
agent = MangabaAgent()

# Após algumas interações...
summary = agent.get_context_summary()
print(summary)
```

## 🔗 Protocolo A2A (Agent-to-Agent)

O protocolo A2A permite comunicação entre múltiplos agentes:

### Comunicação entre Agentes
```python
# Criar dois agentes
agent1 = MangabaAgent()
agent2 = MangabaAgent()

# Enviar requisição de um agente para outro
result = agent1.send_agent_request(
    target_agent_id=agent2.agent_id,
    action="chat",
    params={"message": "Olá do Agent 1!"}
)
```

### Broadcast para Múltiplos Agentes
```python
agent = MangabaAgent()

# Enviar mensagem para todos os agentes conectados
result = agent.broadcast_message(
    message="Olá a todos!",
    tags=["general", "announcement"]
)
```

### Tipos de Mensagens A2A
- **REQUEST**: Requisições entre agentes
- **RESPONSE**: Respostas a requisições
- **BROADCAST**: Mensagens para múltiplos agentes
- **NOTIFICATION**: Notificações assíncronas
- **ERROR**: Mensagens de erro

## 🧠 Protocolo MCP (Model Context Protocol)

O protocolo MCP gerencia contexto avançado automaticamente:

### Tipos de Contexto
- **CONVERSATION**: Conversas e diálogos
- **TASK**: Tarefas e operações específicas
- **MEMORY**: Memórias de longo prazo
- **SYSTEM**: Informações do sistema

### Prioridades de Contexto
- **HIGH**: Contexto crítico (sempre preservado)
- **MEDIUM**: Contexto importante
- **LOW**: Contexto opcional

### Funcionalidades MCP
```python
agent = MangabaAgent()

# Chat com contexto automático
response = agent.chat("Mensagem", use_context=True)

# Chat sem contexto
response = agent.chat("Mensagem", use_context=False)

# Obter resumo do contexto atual
summary = agent.get_context_summary()
```

## 🛠️ Exemplo Avançado

```python
from mangaba_ai import MangabaAgent

def demo_completa():
    # Criar agente com protocolos habilitados
    agent = MangabaAgent()
    
    print(f"Agent ID: {agent.agent_id}")
    print(f"MCP Habilitado: {agent.mcp_enabled}")
    
    # Sequência de interações com contexto
    agent.chat("Olá, meu nome é Maria")
    agent.chat("Eu trabalho com programação")
    
    # Análise com contexto preservado
    analysis = agent.analyze_text(
        "Python é uma linguagem versátil",
        "Analise considerando meu perfil profissional"
    )
    
    # Tradução
    translation = agent.translate("Good morning", "português")
    
    # Resumo do contexto acumulado
    context = agent.get_context_summary()
    print("Contexto atual:", context)
    
    # Comunicação A2A
    agent.broadcast_message("Demonstração concluída!")

if __name__ == "__main__":
    demo_completa()
```

## 🎮 Exemplo Interativo

Execute o exemplo interativo:

```bash
python examples/basic_example.py
```

Comandos disponíveis:
- `/analyze <texto>` - Analisa texto
- `/translate <texto>` - Traduz texto
- `/context` - Mostra contexto atual
- `/broadcast <mensagem>` - Envia broadcast
- `/request <agent_id> <action>` - Requisição para outro agente
- `/help` - Ajuda

## 🧪 Demonstração dos Protocolos

Para ver uma demonstração completa dos protocolos A2A e MCP:

```bash
python examples/basic_example.py --demo
```

## 📋 Funcionalidades Principais

### MangabaAgent
- `chat(message, use_context=True)` - Chat com/sem contexto
- `analyze_text(text, instruction)` - Análise de texto
- `translate(text, target_language)` - Tradução
- `get_context_summary()` - Resumo do contexto
- `send_agent_request(agent_id, action, params)` - Requisição A2A
- `broadcast_message(message, tags)` - Broadcast A2A

### Protocolos Integrados
- **A2A Protocol**: Comunicação entre agentes
- **MCP Protocol**: Gerenciamento de contexto
- **Handlers Customizados**: Para requisições específicas
- **Sessões MCP**: Contexto isolado por sessão

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
API_KEY=sua_chave_api_aqui          # Obrigatório
MODEL=modelo_desejado               # Opcional
LOG_LEVEL=INFO                      # Opcional (DEBUG, INFO, WARNING, ERROR)
```

### Personalização
```python
# Agente com configurações customizadas
agent = MangabaAgent()

# Acessar protocolos diretamente
a2a = agent.a2a_protocol
mcp = agent.mcp

# ID único do agente
print(f"Agent ID: {agent.agent_id}")

# Sessão MCP atual
print(f"Session ID: {agent.current_session_id}")
```

agent = MangabaAgent()
resposta = agent.chat_with_context(
    context="Você é um tutor de programação",
    message="Como criar uma lista em Python?"
)
print(resposta)
```

### Análise de Texto
```python
from mangaba_ai import MangabaAgent

agent = MangabaAgent()
texto = "Este é um texto para analisar..."
analise = agent.analyze_text(texto, "Resuma os pontos principais")
print(analise)
```

## 🔧 Personalização

Para usar um modelo diferente, apenas mude no `.env`:
```
MODEL=modelo-avancado     # Modelo mais avançado
MODEL=modelo-multimodal   # Para diferentes tipos de entrada
```

## 📁 Estrutura do Projeto

```
mangaba_ai/
├── README.md              # Este arquivo
├── requirements.txt       # Dependências
├── .env.example          # Exemplo de configuração
├── config.py             # Configuração automática
├── mangaba_agent.py      # Classe principal do agente
├── examples/             # Exemplos de uso
│   └── basic_example.py  # Exemplo básico completo
└── utils/                # Utilitários
    ├── __init__.py
    └── logger.py         # Sistema de logs
```

## 🧪 Testar Rapidamente

```bash
python examples/basic_example.py
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

MIT License

---

**Mangaba AI** - Agentes de IA simples e eficazes! 🤖✨
