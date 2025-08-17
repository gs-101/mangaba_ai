# ⚙️ Instalação e Configuração

Guia completo para instalar e configurar o Mangaba AI em seu ambiente de desenvolvimento ou produção.

## 📋 Pré-requisitos

### **Sistema Operacional**
- ✅ Linux (Ubuntu 20.04+ recomendado)
- ✅ macOS (10.15+ recomendado)  
- ✅ Windows 10+ (com WSL2 recomendado)

### **Software Base**
- **Python 3.8+** (Python 3.10+ recomendado)
- **pip** (gerenciador de pacotes Python)
- **git** (controle de versão)
- **curl** (para downloads e testes)

### **Recursos Mínimos**
- **RAM**: 4GB (8GB+ recomendado)
- **Espaço em Disco**: 2GB livres
- **CPU**: 2 cores (4+ recomendado)
- **Conexão com Internet**: Para APIs de IA

## 🚀 Instalação Rápida

### 1. **Clone o Repositório**

```bash
# Clone o projeto
git clone https://github.com/Mangaba-ai/mangaba_ai.git
cd mangaba_ai

# Verifique a versão mais recente
git checkout main
```

### 2. **Configure o Ambiente Virtual**

```bash
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# Linux/Mac:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Verifique se está ativo
which python  # deve apontar para .venv/bin/python
```

### 3. **Instale as Dependências**

```bash
# Atualize pip para a versão mais recente
pip install --upgrade pip

# Instale as dependências do projeto
pip install -r requirements.txt

# Verifique a instalação
pip list | grep mangaba
```

### 4. **Configure as Variáveis de Ambiente**

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
nano .env  # ou use seu editor preferido
```

### 5. **Configuração Básica do .env**

```bash
# === CONFIGURAÇÕES OBRIGATÓRIAS ===

# API Key do Google Gemini (obrigatória)
GEMINI_API_KEY=sua_chave_api_aqui

# Configurações básicas
PROJECT_NAME=mangaba_ai
ENVIRONMENT=development
DEBUG=true

# === CONFIGURAÇÕES OPCIONAIS ===

# OpenAI (opcional, para modelos secundários)
OPENAI_API_KEY=sua_chave_openai

# Configurações de logging
LOG_LEVEL=INFO
LOG_DIR=./logs
```

### 6. **Validação da Instalação**

```bash
# Teste a instalação
python -c "from mangaba_ai import MangabaAI; print('✅ Instalação bem-sucedida!')"

# Execute o script de validação (se disponível)
python scripts/validate_env.py

# Execute os testes básicos
python -m pytest tests/test_basic.py -v
```

## 🔧 Configuração Detalhada

### **Obtendo a API Key do Google Gemini**

1. **Acesse o Google AI Studio**:
   - Vá para [https://aistudio.google.com/](https://aistudio.google.com/)
   - Faça login com sua conta Google

2. **Crie uma API Key**:
   - Clique em "Get API Key"
   - Selecione ou crie um projeto
   - Copie a chave gerada

3. **Configure no .env**:
   ```bash
   GEMINI_API_KEY=AIzaSyD...sua_chave_completa_aqui
   ```

### Variáveis de Ambiente Opcionais

```bash
# === PROTOCOLOS ===

# Habilitar protocolo MCP (padrão: true)
USE_MCP=true

# Habilitar protocolo A2A (padrão: true)
USE_A2A=true

# Porta para comunicação A2A (padrão: 8080)
A2A_PORT=8080

# === LOGGING E DEBUGGING ===

# Nível de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Diretório de logs (padrão: ./logs)
LOG_DIR=./logs

# Formato dos logs (json, text)
LOG_FORMAT=text

# === CONTEXTO MCP ===

# Máximo de contextos armazenados (padrão: 1000)
MAX_CONTEXTS=1000

# Diretório do banco de contexto (padrão: ./data)
CONTEXT_DB_PATH=./data/contexts.db

# === PERFORMANCE ===

# Timeout para requisições de IA (segundos)
AI_REQUEST_TIMEOUT=30

# Máximo de requisições simultâneas
MAX_CONCURRENT_REQUESTS=10

# Cache TTL em segundos (padrão: 3600 = 1 hora)
CACHE_TTL=3600
```

## 📊 Configurações Avançadas

### Configuração para Desenvolvimento

```bash
# Instale hooks de pre-commit
pip install pre-commit
pre-commit install

# Configure ambiente de desenvolvimento
export ENVIRONMENT=development
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### Configuração para Produção

```bash
# Configurações otimizadas para produção
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=WARNING
export RATE_LIMIT_PER_MINUTE=120
export CACHE_TTL=7200
```

### Configuração Multi-Agente

```bash
# Configure múltiplos agentes
export A2A_ENABLED=true
export A2A_DISCOVERY_PORT=8081
export A2A_CLUSTER_NAME=meu-cluster

# Agente específico
export AGENT_ROLE=coordinator
export AGENT_SPECIALIZATION=data_analysis
```

## 🐳 Instalação com Docker

### **Dockerfile Básico**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "mangaba_ai"]
```

### **Docker Compose**

```yaml
version: '3.8'

services:
  mangaba-ai:
    build: .
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - ENVIRONMENT=production
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

### **Comandos Docker**

```bash
# Build da imagem
docker build -t mangaba-ai .

# Execute o container
docker run -d \
  --name mangaba-ai \
  -e GEMINI_API_KEY=sua_chave \
  -p 8080:8080 \
  mangaba-ai

# Usando Docker Compose
docker-compose up -d
```

## 🔄 Atualizações

### Atualizando o Projeto
```bash
# Atualize o código
git pull origin main

# Atualize dependências
pip install -r requirements.txt --upgrade

# Re-execute validação
python scripts/validate_env.py
```

### Migrações de Dados
```bash
# Execute scripts de migração quando necessário
python scripts/migrate_data.py
```

## 🔍 Troubleshooting

### Problemas Comuns

#### **1. Erro de API Key**
```bash
# Sintomas: "Invalid API key" ou "Authentication failed"
# Solução:
# 1. Verifique se a GEMINI_API_KEY está correta
# 2. Confirme que a chave tem permissões adequadas
# 3. Teste a chave diretamente:
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
     https://generativelanguage.googleapis.com/v1/models
```

#### **2. Erro de Importação**
```bash
# Sintomas: "ModuleNotFoundError: No module named 'mangaba_ai'"
# Solução:
# 1. Verifique se o ambiente virtual está ativo
source .venv/bin/activate

# 2. Reinstale as dependências
pip install -r requirements.txt

# 3. Verifique o PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

#### **3. Erro de Permissões**
```bash
# Sintomas: "Permission denied" ao executar
# Solução:
chmod +x scripts/*.py
sudo chown -R $USER:$USER ./logs ./data
```

#### **4. Problemas de Conectividade**
```bash
# Teste conectividade com APIs
curl -I https://generativelanguage.googleapis.com/

# Verifique proxy/firewall
export HTTP_PROXY=http://seu-proxy:porta
export HTTPS_PROXY=http://seu-proxy:porta
```

### Logs de Debug

```bash
# Ative logs detalhados
export LOG_LEVEL=DEBUG

# Monitore logs em tempo real
tail -f logs/mangaba_ai.log

# Busque por erros específicos
grep -i error logs/mangaba_ai.log
```

## 🆘 Suporte

### Se encontrar problemas:

1. **Consulte o [FAQ](faq.md)** para soluções rápidas
2. **Verifique os [Issues](https://github.com/Mangaba-ai/mangaba_ai/issues)** existentes
3. **Abra um [novo Issue](https://github.com/Mangaba-ai/mangaba_ai/issues/new)** com detalhes

### Informações para Support

Ao reportar problemas, inclua:

```bash
# Informações do sistema
python --version
pip --version
uname -a

# Logs relevantes
grep -A 10 -B 10 "ERROR" logs/mangaba_ai.log

# Configuração (sem chaves sensíveis)
cat .env | grep -v "_KEY"
```

---

## 🔗 Próximos Passos

1. **[🎓 Primeiros Passos](primeiros-passos.md)** - Tutorial prático
2. **[🌐 Explorar Protocolos](exemplos-protocolos.md)** - A2A e MCP
3. **[⭐ Melhores Práticas](melhores-praticas.md)** - Dicas avançadas

> 🚀 **Instalação Concluída?** Vá para [Primeiros Passos](primeiros-passos.md) e crie seu primeiro agente!