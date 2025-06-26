# Mangaba.AI

Framework for developing intelligent autonomous agents.

## Project Structure

```
mangaba_ai/
├── .github/                    # GitHub configurations
├── docs/                       # Documentation
│   ├── api/                   # API documentation
│   ├── guides/                # Usage guides
│   └── examples/              # Documented examples
├── src/                       # Source code
│   ├── core/                  # Framework core
│   │   ├── agents/           # Agent implementations
│   │   ├── models/           # Data models
│   │   ├── protocols/        # Protocols and interfaces
│   │   └── tools/            # Base tools
│   ├── integrations/         # Optional integrations
│   └── utils/                # General utilities
├── tests/                     # Tests
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
├── examples/                  # Examples
│   ├── basic/                # Basic examples
│   └── advanced/             # Advanced examples
└── scripts/                   # Utility scripts
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/mangaba_ai.git
cd mangaba_ai
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit the .env file with your settings
```

## Basic Usage

```python
from mangaba_ai import MangabaAI

# Initialize the framework
ai = MangabaAI()

# Create an agent
agent = ai.create_agent(
    name="my_agent",
    role="Analyst",
    goal="Analyze data and generate insights"
)

# Create a task
task = ai.create_task(
    description="Analyze sales data",
    agent=agent
)

# Execute the task
result = await ai.execute([task])
```

## Documentation

- [Quick Start Guide](docs/guides/quickstart.md)
- [API Documentation](docs/api/README.md)
- [Examples](docs/examples/README.md)

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Configure pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
pytest
```

## Test Results

O projeto possui uma suíte de testes abrangente com **22 testes passando** e **54% de cobertura de código**.

### Tipos de Testes

- **Testes Básicos** (`test_basic.py`): Verificam importação e versão do pacote
- **Testes Core** (`test_core.py`): Testam componentes principais como Agent, Task e GoogleSearchTool
- **Testes de API** (`test_mangaba_api.py`): Validam funcionalidades assíncronas do Agent e MCP
- **Testes de Integração** (`test_integration.py`): Cenários completos de uso incluindo:
  - Processamento de mensagens por agentes
  - Análise de conversas pelo MCP
  - Processamento com múltiplos agentes
  - Tratamento de conversas vazias e grandes
  - Criação de mensagens com metadados
- **Testes de Performance** (`test_performance_extended.py`): Benchmarks de desempenho:
  - Velocidade de processamento (100 mensagens)
  - Análise de conversas (50 mensagens)
  - Processamento concorrente (5 agentes)
  - Estabilidade de memória
  - Escalabilidade com conversas grandes
  - Velocidade de inicialização de agentes
- **Testes de API Slack** (`test_slack_api.py`): Validação de integração com Slack (mockado)

### Executar Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Executar testes específicos
pytest tests/test_integration.py -v
pytest tests/test_performance_extended.py -v

# Executar com cobertura
pytest tests/ --cov=src/mangaba_ai --cov-report=html
```

### Métricas de Performance

- **Processamento**: >20 mensagens/segundo
- **Análise MCP**: <3 segundos para 50 mensagens
- **Throughput Concorrente**: >10 mensagens/segundo
- **Inicialização**: >100 agentes/segundo
- **Uso de Memória**: <50MB de aumento durante processamento intenso

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

