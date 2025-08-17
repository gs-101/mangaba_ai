# 🎓 Primeiros Passos

Tutorial prático passo-a-passo para começar a usar o Mangaba AI. Este guia irá levá-lo desde a instalação básica até a criação de seus primeiros agentes inteligentes.

## 📋 O que você vai aprender

- ✅ Configurar o ambiente de desenvolvimento
- ✅ Criar seu primeiro agente
- ✅ Implementar comunicação entre agentes (A2A)
- ✅ Usar contexto inteligente (MCP)
- ✅ Criar um sistema multi-agente básico

---

## 🚀 Passo 1: Configuração Inicial

### **1.1 Verificar Pré-requisitos**

```bash
# Verificar Python (deve ser 3.8+)
python --version

# Verificar pip
pip --version

# Verificar git
git --version
```

### **1.2 Clonar e Configurar Projeto**

```bash
# Clonar repositório
git clone https://github.com/Mangaba-ai/mangaba_ai.git
cd mangaba_ai

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### **1.3 Configurar API Keys**

```bash
# Copiar arquivo de configuração
cp .env.example .env

# Editar arquivo .env
nano .env  # ou seu editor preferido
```

Configure no `.env`:
```bash
# Obrigatório: API key do Google Gemini
GEMINI_API_KEY=sua_chave_api_aqui

# Opcional: Para modelos adicionais
OPENAI_API_KEY=sua_chave_openai

# Configurações básicas
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

### **1.4 Validar Instalação**

```bash
# Teste básico
python -c "from mangaba_ai import MangabaAI; print('✅ Mangaba AI instalado com sucesso!')"

# Executar testes (opcional)
pytest tests/test_basic.py -v
```

---

## 🤖 Passo 2: Primeiro Agente

### **2.1 Criar arquivo `primeiro_agente.py`**

```python
from mangaba_ai import MangabaAI
import asyncio

async def main():
    # Inicializar framework
    print("🚀 Inicializando Mangaba AI...")
    ai = MangabaAI()
    
    # Criar primeiro agente
    print("🤖 Criando primeiro agente...")
    assistente = ai.create_agent(
        name="assistente",
        role="Assistente Pessoal",
        goal="Ajudar usuários com tarefas gerais e responder perguntas"
    )
    
    # Testar o agente
    print("💬 Testando conversa...")
    resposta = await assistente.chat("Olá! Quem é você e como pode me ajudar?")
    print(f"🤖 Assistente: {resposta}")
    
    # Segunda pergunta para testar contexto
    resposta2 = await assistente.chat("Qual foi minha primeira pergunta?")
    print(f"🤖 Assistente: {resposta2}")
    
    print("✅ Primeiro agente funcionando!")

if __name__ == "__main__":
    asyncio.run(main())
```

### **2.2 Executar o exemplo**

```bash
python primeiro_agente.py
```

**Saída esperada:**
```
🚀 Inicializando Mangaba AI...
🤖 Criando primeiro agente...
💬 Testando conversa...
🤖 Assistente: Olá! Eu sou seu assistente pessoal criado com Mangaba AI...
🤖 Assistente: Sua primeira pergunta foi sobre quem eu sou e como posso ajudar...
✅ Primeiro agente funcionando!
```

---

## 🔗 Passo 3: Comunicação Entre Agentes (A2A)

### **3.1 Criar `comunicacao_agentes.py`**

```python
from mangaba_ai import MangabaAI
import asyncio

async def exemplo_comunicacao():
    print("🚀 Inicializando sistema multi-agente...")
    ai = MangabaAI()
    
    # Criar agentes especializados
    pesquisador = ai.create_agent(
        name="pesquisador",
        role="Pesquisador",
        goal="Coletar e organizar informações"
    )
    
    analista = ai.create_agent(
        name="analista",
        role="Analista de Dados", 
        goal="Analisar informações e gerar insights"
    )
    
    # Simulação: Pesquisador coleta dados
    print("🔍 Pesquisador coletando dados...")
    dados_pesquisa = "Dados sobre tendências de IA em 2024: crescimento de 150% em adoção empresarial"
    
    # A2A: Pesquisador envia dados para Analista
    print("📤 Enviando dados via protocolo A2A...")
    await pesquisador.send_message(
        receiver="analista",
        content=dados_pesquisa,
        message_type="research_data",
        priority=2
    )
    
    # Analista recebe e processa dados
    print("📥 Analista processando dados recebidos...")
    mensagens = await analista.receive_messages()
    
    if mensagens:
        dados_recebidos = mensagens[0].content
        print(f"📊 Dados recebidos: {dados_recebidos}")
        
        # Analista gera insights
        analise = await analista.chat(f"Analise os seguintes dados e gere insights: {dados_recebidos}")
        print(f"🧠 Análise: {analise}")
        
        # Responder ao pesquisador
        await analista.send_message(
            receiver="pesquisador",
            content=f"Análise concluída: {analise}",
            message_type="analysis_result"
        )
    
    print("✅ Comunicação A2A funcionando!")

if __name__ == "__main__":
    asyncio.run(exemplo_comunicacao())
```

### **3.2 Executar exemplo A2A**

```bash
python comunicacao_agentes.py
```

---

## 🧠 Passo 4: Contexto Inteligente (MCP)

### **4.1 Criar `contexto_inteligente.py`**

```python
from mangaba_ai import MangabaAI
import asyncio

async def exemplo_contexto():
    print("🧠 Demonstrando protocolo MCP...")
    ai = MangabaAI()
    
    # Criar agente com contexto
    especialista = ai.create_agent(
        name="especialista",
        role="Especialista em IA",
        goal="Fornecer consultoria especializada mantendo contexto"
    )
    
    # Sessão 1: Estabelecer contexto
    print("\n📝 Sessão 1 - Estabelecendo contexto...")
    
    await especialista.chat("Trabalho na empresa TechCorp como CTO")
    await especialista.chat("Estamos implementando IA generativa em nossos produtos")
    await especialista.chat("Temos um orçamento de R$ 500.000 para este projeto")
    
    # Teste de contexto
    resposta = await especialista.chat("Considerando meu perfil e orçamento, que soluções você recomenda?")
    print(f"🤖 Especialista: {resposta}")
    
    # Sessão 2: Usar contexto em nova conversa
    print("\n🔄 Sessão 2 - Usando contexto anterior...")
    
    resposta2 = await especialista.chat("Qual é minha função na empresa mesmo?")
    print(f"🤖 Especialista: {resposta2}")
    
    # Demonstrar busca semântica no contexto
    print("\n🔍 Busca semântica no contexto...")
    resultados = await especialista.mcp_protocol.semantic_search(
        query="orçamento financeiro",
        limit=3
    )
    
    print("📊 Informações relacionadas a orçamento:")
    for resultado in resultados:
        print(f"  - {resultado.content} (relevância: {resultado.relevance:.2f})")
    
    print("✅ Protocolo MCP funcionando!")

if __name__ == "__main__":
    asyncio.run(exemplo_contexto())
```

### **4.2 Executar exemplo MCP**

```bash
python contexto_inteligente.py
```

---

## 🏢 Passo 5: Sistema Multi-Agente Completo

### **5.1 Criar `sistema_completo.py`**

```python
from mangaba_ai import MangabaAI
import asyncio

class SistemaAtendimento:
    def __init__(self):
        self.ai = MangabaAI()
        self._criar_agentes()
    
    def _criar_agentes(self):
        """Cria equipe de agentes especializados."""
        # Recepcionista: primeira linha de atendimento
        self.recepcionista = self.ai.create_agent(
            name="recepcionista",
            role="Atendente de Primeira Linha",
            goal="Receber e classificar solicitações de clientes"
        )
        
        # Técnico: problemas técnicos
        self.tecnico = self.ai.create_agent(
            name="tecnico",
            role="Suporte Técnico",
            goal="Resolver problemas técnicos complexos"
        )
        
        # Vendedor: questões comerciais
        self.vendedor = self.ai.create_agent(
            name="vendedor",
            role="Consultor de Vendas",
            goal="Auxiliar com questões comerciais e vendas"
        )
        
        # Supervisor: escalação e qualidade
        self.supervisor = self.ai.create_agent(
            name="supervisor",
            role="Supervisor de Atendimento",
            goal="Garantir qualidade e resolver casos complexos"
        )
    
    async def processar_solicitacao(self, mensagem_cliente, cliente_id="cliente_123"):
        """Processa solicitação completa do cliente."""
        
        print(f"📞 Nova solicitação do cliente {cliente_id}")
        print(f"📝 Mensagem: {mensagem_cliente}")
        
        # 1. Recepcionista classifica a solicitação
        print("\n🎯 Classificando solicitação...")
        
        classificacao = await self.recepcionista.chat(
            f"Classifique esta solicitação em 'tecnico', 'vendas' ou 'supervisor': {mensagem_cliente}"
        )
        
        # Extrair categoria (simplificado)
        if "tecnico" in classificacao.lower():
            categoria = "tecnico"
        elif "vendas" in classificacao.lower():
            categoria = "vendas"
        else:
            categoria = "supervisor"
        
        print(f"📋 Categoria identificada: {categoria}")
        
        # 2. MCP: Estabelecer contexto do cliente
        agente_especializado = getattr(self, categoria)
        
        with agente_especializado.mcp_protocol.session(cliente_id) as sessao:
            # 3. A2A: Recepcionista envia dados para especialista
            print(f"\n📤 Encaminhando para {categoria}...")
            
            await self.recepcionista.send_message(
                receiver=categoria,
                content={
                    "cliente_id": cliente_id,
                    "solicitacao": mensagem_cliente,
                    "classificacao": classificacao
                },
                message_type="customer_request",
                priority=2
            )
            
            # 4. Especialista processa
            mensagens = await agente_especializado.receive_messages()
            if mensagens:
                dados = mensagens[0].content
                
                resposta = await agente_especializado.chat(
                    f"Atenda esta solicitação: {dados['solicitacao']}"
                )
                
                print(f"🤖 {categoria.title()}: {resposta}")
                
                # 5. Se necessário, escalar para supervisor
                if "complexo" in resposta.lower() or "supervisor" in resposta.lower():
                    print("\n⬆️ Escalando para supervisor...")
                    
                    await agente_especializado.send_message(
                        receiver="supervisor",
                        content={
                            "cliente_id": cliente_id,
                            "solicitacao_original": mensagem_cliente,
                            "tentativa_resolucao": resposta,
                            "agente_anterior": categoria
                        },
                        message_type="escalation",
                        priority=3
                    )
                    
                    # Supervisor trata escalação
                    mensagens_supervisor = await self.supervisor.receive_messages()
                    if mensagens_supervisor:
                        escalacao = mensagens_supervisor[0].content
                        resposta_final = await self.supervisor.chat(
                            f"Resolva esta escalação: {escalacao}"
                        )
                        print(f"👔 Supervisor: {resposta_final}")
                        return resposta_final
                
                return resposta
        
        return "Erro no processamento"

async def main():
    print("🏢 Inicializando Sistema de Atendimento Multi-Agente...")
    
    sistema = SistemaAtendimento()
    
    # Simular diferentes tipos de solicitações
    solicitacoes = [
        "Meu software está apresentando erro 500 constantemente",
        "Gostaria de saber sobre os planos Enterprise disponíveis",
        "Preciso cancelar minha assinatura imediatamente"
    ]
    
    for i, solicitacao in enumerate(solicitacoes, 1):
        print(f"\n{'='*60}")
        print(f"📋 SOLICITAÇÃO {i}")
        print(f"{'='*60}")
        
        resposta = await sistema.processar_solicitacao(
            solicitacao, 
            f"cliente_{i:03d}"
        )
        
        print(f"\n✅ Solicitação {i} processada!")
        await asyncio.sleep(1)  # Pausa entre solicitações
    
    print(f"\n{'='*60}")
    print("🎉 Sistema Multi-Agente funcionando perfeitamente!")
    print("✅ Protocolos A2A e MCP integrados com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
```

### **5.2 Executar sistema completo**

```bash
python sistema_completo.py
```

---

## 🎯 Próximos Passos

Parabéns! 🎉 Você concluiu o tutorial básico. Agora você pode:

### **📚 Aprofundar Conhecimentos**
- **[🌐 Exemplos Avançados de Protocolos](exemplos-protocolos.md)** - A2A e MCP detalhados
- **[⭐ Melhores Práticas](melhores-praticas.md)** - Otimização e padrões
- **[🏗️ Arquitetura Avançada](arquitetura-avancada.md)** - Detalhes técnicos

### **🛠️ Expandir Funcionalidades**
- Adicionar novas ferramentas aos agentes
- Integrar com APIs externas (Slack, Discord, etc.)
- Implementar persistent storage
- Criar interfaces web

### **🤝 Contribuir**
- **[📋 Como Contribuir](contribuicao.md)** - Junte-se à comunidade
- Reporte bugs ou solicite features
- Melhore a documentação
- Compartilhe seus casos de uso

### **🆘 Obter Ajuda**
- **[❓ FAQ](faq.md)** - Perguntas frequentes
- **[GitHub Issues](https://github.com/Mangaba-ai/mangaba_ai/issues)** - Problemas técnicos
- **[Discussions](https://github.com/Mangaba-ai/mangaba_ai/discussions)** - Comunidade

---

## 🎓 Resumo do que Aprendeu

✅ **Configuração**: Ambiente e API keys  
✅ **Agentes**: Criação e configuração básica  
✅ **A2A**: Comunicação entre agentes  
✅ **MCP**: Contexto e memória inteligente  
✅ **Sistema Multi-Agente**: Integração completa  

---

> 🚀 **Próximo Passo Recomendado**: Explore os [Exemplos de Protocolos](exemplos-protocolos.md) para casos de uso mais avançados!