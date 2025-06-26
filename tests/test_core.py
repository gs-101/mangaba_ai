"""
Testes para os componentes principais do Mangaba.AI
"""

import asyncio

import pytest

from mangaba_ai.core.agent import Agent
from mangaba_ai.core.models import GeminiModel, Task
from mangaba_ai.tools import GoogleSearchTool


@pytest.fixture
def search_tool():
    return GoogleSearchTool()


@pytest.fixture
def agent():
    return Agent()


@pytest.fixture
def task(agent):
    return Task(description="Test task description", agent=agent)


def test_agent_initialization(agent):
    """Testa a inicialização correta de um agente"""
    assert agent.name == "Mangaba.AI Agent"
    assert agent.version == "1.0.0"


def test_task_initialization(task):
    """Testa a inicialização correta de uma tarefa"""
    assert task.description == "Test task description"
    assert task.agent is not None
    assert task.status == "pending"
    assert task.context == {}


def test_search_tool_initialization(search_tool):
    """Testa a inicialização da ferramenta de busca"""
    assert search_tool is not None
    assert hasattr(search_tool, 'search')
