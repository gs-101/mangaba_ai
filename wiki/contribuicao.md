# 🤝 Diretrizes de Contribuição

Bem-vindo à comunidade **Mangaba AI**! Este documento contém todas as informações necessárias para contribuir com o projeto de forma efetiva e colaborativa.

## 📋 Índice

1. [🎯 Como Contribuir](#-como-contribuir)
2. [🚀 Configuração do Ambiente de Desenvolvimento](#-configuração-do-ambiente-de-desenvolvimento)
3. [📝 Padrões de Código](#-padrões-de-código)
4. [🧪 Testes e Qualidade](#-testes-e-qualidade)
5. [📚 Documentação](#-documentação)
6. [🔄 Processo de Pull Request](#-processo-de-pull-request)
7. [🐛 Reportando Issues](#-reportando-issues)
8. [💡 Sugestões de Melhorias](#-sugestões-de-melhorias)
9. [🏆 Reconhecimento de Contribuidores](#-reconhecimento-de-contribuidores)

---

## 🎯 Como Contribuir

### 🌟 **Tipos de Contribuição Bem-Vindas**

#### **1. 🐛 Correção de Bugs**
- Identificação e correção de problemas existentes
- Melhoria na estabilidade do sistema
- Otimização de performance

#### **2. ✨ Novas Funcionalidades**
- Implementação de recursos solicitados pela comunidade
- Melhorias nos protocolos A2A e MCP
- Integração com novas APIs e serviços

#### **3. 📚 Documentação**
- Melhoria da documentação existente
- Criação de tutoriais e exemplos
- Tradução para outros idiomas

#### **4. 🧪 Testes**
- Adição de novos casos de teste
- Melhoria da cobertura de testes
- Testes de performance e stress

#### **5. 🎨 UX/UI**
- Melhorias na interface (se aplicável)
- Otimização da experiência do desenvolvedor
- Design de ferramentas visuais

## 🚀 Configuração do Ambiente de Desenvolvimento

### **1. Fork e Clone**

```bash
# 1. Faça fork do repositório no GitHub
# 2. Clone seu fork
git clone https://github.com/SEU_USUARIO/mangaba_ai.git
cd mangaba_ai

# 3. Adicione o repositório original como upstream
git remote add upstream https://github.com/Mangaba-ai/mangaba_ai.git
```

### **2. Configuração Inicial**

```bash
# Crie e ative ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instale dependências de desenvolvimento
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure hooks de pre-commit
pre-commit install
```

### **3. Configuração de Desenvolvimento**

```bash
# Crie arquivo .env para desenvolvimento
cp .env.example .env.dev

# Configure variáveis específicas para desenvolvimento
cat >> .env.dev << EOF
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
USE_MOCK_AI=true  # Para testes sem API keys
EOF
```

### **4. Validação do Setup**

```bash
# Execute testes para validar configuração
pytest tests/test_basic.py -v

# Execute linters
black --check src/
flake8 src/
mypy src/

# Valide pre-commit hooks
pre-commit run --all-files
```

## 📝 Padrões de Código

### **Estilo de Código Python**

#### **Formatação**
- **Black**: Formatação automática
- **isort**: Organização de imports
- **Line length**: Máximo 88 caracteres (padrão Black)

```bash
# Formatação automática
black src/ tests/
isort src/ tests/
```

#### **Linting**
- **flake8**: Verificação de estilo
- **mypy**: Verificação de tipos
- **pylint**: Análise estática avançada

```bash
# Verificação de qualidade
flake8 src/ tests/
mypy src/
pylint src/mangaba_ai/
```

### **Convenções de Nomenclatura**

```python
# Classes: PascalCase
class MangabaAgent:
    pass

# Funções e variáveis: snake_case
def process_message(user_input: str) -> str:
    processed_result = ai_model.generate(user_input)
    return processed_result

# Constantes: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30

# Métodos privados: _snake_case
def _internal_process(self, data: dict) -> dict:
    return data
```

### **Documentação de Código**

```python
def create_agent(
    name: str,
    role: str,
    goal: str,
    tools: Optional[List[str]] = None
) -> MangabaAgent:
    """
    Cria um novo agente Mangaba AI.
    
    Args:
        name: Nome único do agente
        role: Papel/função do agente no sistema
        goal: Objetivo principal do agente
        tools: Lista opcional de ferramentas disponíveis
        
    Returns:
        Instância configurada do MangabaAgent
        
    Raises:
        ValueError: Se name ou role estiverem vazios
        AgentExistsError: Se já existe agente com esse nome
        
    Example:
        >>> agent = create_agent(
        ...     name="assistente",
        ...     role="Customer Support",
        ...     goal="Ajudar usuários com problemas"
        ... )
        >>> print(agent.name)
        assistente
    """
    pass
```

### **Type Hints**

```python
from typing import List, Dict, Optional, Union, Any
from pydantic import BaseModel

# Use type hints sempre
def process_data(
    items: List[Dict[str, Any]],
    config: Optional[Dict[str, str]] = None
) -> Union[str, None]:
    pass

# Para classes, use Pydantic quando apropriado
class AgentConfig(BaseModel):
    name: str
    role: str
    max_tokens: int = 1000
    temperature: float = 0.7
```

## 🧪 Testes e Qualidade

### **Estrutura de Testes**

```
tests/
├── unit/                 # Testes unitários
│   ├── test_agents.py
│   ├── test_protocols.py
│   └── test_utils.py
├── integration/          # Testes de integração
│   ├── test_a2a_mcp.py
│   └── test_workflows.py
├── e2e/                  # Testes end-to-end
│   └── test_full_scenarios.py
├── performance/          # Testes de performance
│   └── test_benchmarks.py
└── conftest.py          # Configurações pytest
```

### **Escrevendo Testes**

#### **Testes Unitários**

```python
import pytest
from unittest.mock import Mock, AsyncMock
from mangaba_ai.core.agents import MangabaAgent

class TestMangabaAgent:
    @pytest.fixture
    def mock_ai_model(self):
        return AsyncMock()
    
    @pytest.fixture
    def agent(self, mock_ai_model):
        return MangabaAgent(
            name="test_agent",
            role="Test Role",
            ai_model=mock_ai_model
        )
    
    async def test_agent_creation(self, agent):
        """Testa criação básica do agente."""
        assert agent.name == "test_agent"
        assert agent.role == "Test Role"
        assert agent.is_active == True
    
    async def test_chat_functionality(self, agent, mock_ai_model):
        """Testa funcionalidade de chat."""
        # Arrange
        mock_ai_model.generate.return_value = "Resposta de teste"
        
        # Act
        response = await agent.chat("Mensagem de teste")
        
        # Assert
        assert response == "Resposta de teste"
        mock_ai_model.generate.assert_called_once()
```

#### **Testes de Integração**

```python
@pytest.mark.integration
class TestA2AMCP:
    async def test_agent_communication_with_context(self):
        """Testa comunicação A2A com contexto MCP."""
        # Setup
        ai = MangabaAI()
        agent1 = ai.create_agent("sender", "Sender", "Send messages")
        agent2 = ai.create_agent("receiver", "Receiver", "Receive messages")
        
        # Test
        await agent1.send_message(
            receiver="receiver",
            content="Test message with context"
        )
        
        messages = await agent2.receive_messages()
        assert len(messages) == 1
        assert "context" in messages[0].content
```

### **Cobertura de Testes**

```bash
# Execute testes com cobertura
pytest --cov=src/mangaba_ai --cov-report=html --cov-report=term

# Meta: manter cobertura > 80%
# Crítico: core modules devem ter > 90%
```

### **Testes de Performance**

```python
@pytest.mark.performance
class TestPerformance:
    async def test_agent_response_time(self):
        """Testa tempo de resposta dos agentes."""
        import time
        
        agent = create_test_agent()
        
        start_time = time.time()
        await agent.chat("Simple question")
        response_time = time.time() - start_time
        
        # Resposta deve ser < 2 segundos
        assert response_time < 2.0
```

## 📚 Documentação

### **Documentação de API**

```python
# Use docstrings completas
def process_request(request: dict) -> dict:
    """
    Processa uma requisição do usuário.
    
    Esta função valida a requisição, aplica transformações necessárias
    e retorna uma resposta estruturada.
    
    Args:
        request: Dicionário contendo:
            - user_id (str): ID único do usuário
            - message (str): Mensagem do usuário
            - context (dict, optional): Contexto adicional
    
    Returns:
        dict: Resposta processada contendo:
            - response (str): Resposta gerada
            - metadata (dict): Metadados do processamento
            - timestamp (str): Timestamp da resposta
    
    Raises:
        ValidationError: Se request não contém campos obrigatórios
        ProcessingError: Se ocorrer erro durante processamento
    
    Example:
        >>> request = {
        ...     "user_id": "user123",
        ...     "message": "Olá!"
        ... }
        >>> response = process_request(request)
        >>> print(response["response"])
        Olá! Como posso ajudar?
    """
    pass
```

### **Documentação Markdown**

- Use templates consistentes
- Inclua exemplos práticos
- Mantenha atualizado com código
- Links internos funcionais

### **Comentários no Código**

```python
# Use comentários para explicar "porquê", não "o quê"
def complex_algorithm(data: list) -> list:
    # Otimização necessária para grandes datasets (>10k items)
    # Usando algoritmo dividir-e-conquistar para reduzir complexidade
    if len(data) > 10000:
        return divide_and_conquer_sort(data)
    
    # Para datasets pequenos, sort padrão é mais eficiente
    return sorted(data)
```

## 🔄 Processo de Pull Request

### **1. Preparação**

```bash
# Certifique-se de estar na branch main atualizada
git checkout main
git pull upstream main

# Crie branch para sua feature
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/descricao-do-bug
```

### **2. Desenvolvimento**

```bash
# Faça commits pequenos e focados
git add specific_file.py
git commit -m "feat: adiciona validação de entrada em process_request"

# Use conventional commits
# feat: nova funcionalidade
# fix: correção de bug
# docs: alterações em documentação
# style: formatação, sem mudanças de código
# refactor: refatoração sem mudança de comportamento
# test: adição/modificação de testes
# chore: mudanças em build, CI/CD, etc.
```

### **3. Antes de Abrir PR**

```bash
# Execute checklist completo
pre-commit run --all-files
pytest tests/ -v
black --check src/
flake8 src/
mypy src/

# Atualize documentação se necessário
# Adicione/atualize testes
# Confirme que todos os testes passam
```

### **4. Abrindo o Pull Request**

#### **Template de PR**

```markdown
## 📝 Descrição

Breve descrição das mudanças implementadas.

## 🎯 Motivação

Por que esta mudança é necessária? Qual problema resolve?

## 🔄 Tipo de Mudança

- [ ] 🐛 Bug fix
- [ ] ✨ Nova funcionalidade
- [ ] 💥 Breaking change
- [ ] 📚 Documentação
- [ ] 🧪 Testes

## 🧪 Como Testar

1. Passos para reproduzir/testar
2. Comandos específicos
3. Resultados esperados

## 📋 Checklist

- [ ] Testes passando
- [ ] Código formatado com black
- [ ] Documentação atualizada
- [ ] Changelog atualizado (se necessário)
- [ ] Sem breaking changes (ou devidamente documentados)

## 📸 Screenshots (se aplicável)

## 🔗 Issues Relacionadas

Fixes #123
Closes #456
```

### **5. Review Process**

- **Auto-checks**: CI/CD deve passar
- **Code Review**: Pelo menos 1 aprovação
- **Documentação**: Verificada e atualizada
- **Testes**: Cobertura mantida/melhorada

## 🐛 Reportando Issues

### **Template de Bug Report**

```markdown
## 🐛 Descrição do Bug

Descrição clara e concisa do problema.

## 🔄 Passos para Reproduzir

1. Vá para '...'
2. Execute '...'
3. Observe '...'

## ✅ Comportamento Esperado

O que deveria acontecer.

## ❌ Comportamento Atual

O que realmente acontece.

## 🖼️ Screenshots

Se aplicável, adicione screenshots.

## 🌍 Ambiente

- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.10.5]
- Mangaba AI: [e.g. 1.0.0]
- Dependências relevantes: [e.g. aiohttp 3.8.0]

## 📋 Informações Adicionais

Logs, configurações, ou qualquer contexto adicional.
```

### **Template de Feature Request**

```markdown
## 🚀 Descrição da Funcionalidade

Descrição clara da funcionalidade solicitada.

## 🎯 Problema/Motivação

Qual problema esta funcionalidade resolveria?

## 💡 Solução Proposta

Como você imagina que deveria funcionar?

## 🔄 Alternativas Consideradas

Outras abordagens que você considerou?

## 📋 Informações Adicionais

Mockups, referências, exemplos, etc.
```

## 💡 Sugestões de Melhorias

### **🌟 Ideias para Contribuição**

#### **1. Funcionalidades Solicitadas**

**📊 Dashboard de Monitoramento**
- Interface web para monitorar agentes
- Métricas em tempo real
- Visualização de contextos MCP

**🔌 Integrações**
- Conectores para bancos de dados
- APIs de terceiros (Slack, Discord, etc.)
- Plugins para IDEs

**🧠 Melhorias de IA**
- Suporte a modelos locais (Ollama, etc.)
- Fine-tuning específico por domínio
- Pipelines de processamento de dados

#### **2. Exemplos e Casos de Uso**
- Tutorials específicos por setor
- Templates de agentes comuns
- Casos de uso empresariais

#### **3. Ferramentas de Desenvolvimento**
- CLI para gerenciamento de agentes
- Ferramentas de debug visual
- Geradores de código

### **🏃‍♂️ Contribuições Rápidas**

- Correção de typos na documentação
- Tradução de documentos
- Adição de exemplos
- Melhoria de mensagens de erro
- Otimização de imports

## 🏆 Reconhecimento de Contribuidores

### **Sistema de Contribuição**

Reconhecemos contribuições através de:

1. **🏷️ Labels no GitHub**: Contribuidores recebem labels especiais
2. **📜 Hall of Fame**: Lista de principais contribuidores
3. **🎖️ Badges**: Emblemas por tipo/quantidade de contribuições
4. **📣 Shout-outs**: Menções em releases e redes sociais

### **Tipos de Reconhecimento**

- 🥇 **Gold Contributor**: 10+ PRs merged
- 🥈 **Silver Contributor**: 5+ PRs merged  
- 🥉 **Bronze Contributor**: 2+ PRs merged
- 🌟 **First Timer**: Primeira contribuição
- 📚 **Documentation Hero**: Contribuições em docs
- 🧪 **Testing Champion**: Contribuições em testes
- 🐛 **Bug Hunter**: Relatórios de bugs de qualidade

---

## 🚀 Primeiros Passos

1. **Leia o [código de conduta](CODE_OF_CONDUCT.md)**
2. **Configure seu [ambiente de desenvolvimento](#-configuração-do-ambiente-de-desenvolvimento)**
3. **Explore [issues marcadas como "good first issue"](https://github.com/Mangaba-ai/mangaba_ai/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)**
4. **Junte-se às [discussões da comunidade](https://github.com/Mangaba-ai/mangaba_ai/discussions)**

## 🤝 Dúvidas?

- 💬 [Discussions](https://github.com/Mangaba-ai/mangaba_ai/discussions)
- 🐛 [Issues](https://github.com/Mangaba-ai/mangaba_ai/issues)
- 📧 Email: [contribuicoes@mangaba.ai](mailto:contribuicoes@mangaba.ai)

---

> 🎉 **Obrigado por contribuir com o Mangaba AI!** Sua ajuda é fundamental para tornar este projeto ainda melhor.