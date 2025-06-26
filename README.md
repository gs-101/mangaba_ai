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

The project has a comprehensive test suite with **22 passing tests** and **54% code coverage**.

### Test Types

- **Basic Tests** (`test_basic.py`): Verify package import and version
- **Core Tests** (`test_core.py`): Test main components like Agent, Task, and GoogleSearchTool
- **API Tests** (`test_mangaba_api.py`): Validate asynchronous Agent and MCP functionalities
- **Integration Tests** (`test_integration.py`): Complete usage scenarios including:
  - Message processing by agents
  - Conversation analysis by MCP
  - Multi-agent processing
  - Empty and large conversation handling
  - Message creation with metadata
- **Performance Tests** (`test_performance_extended.py`): Performance benchmarks:
  - Processing speed (100 messages)
  - Conversation analysis (50 messages)
  - Concurrent processing (5 agents)
  - Memory stability
  - Scalability with large conversations
  - Agent initialization speed
- **Slack API Tests** (`test_slack_api.py`): Slack integration validation (mocked)

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific tests
pytest tests/test_integration.py -v
pytest tests/test_performance_extended.py -v

# Run with coverage
pytest tests/ --cov=src/mangaba_ai --cov-report=html
```

### Performance Metrics

- **Processing**: >20 messages/second
- **MCP Analysis**: <3 seconds for 50 messages
- **Concurrent Throughput**: >10 messages/second
- **Initialization**: >100 agents/second
- **Memory Usage**: <50MB increase during intensive processing

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

