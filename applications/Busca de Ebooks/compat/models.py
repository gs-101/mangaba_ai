"""Modelos base do framework Mangaba.AI (compatibilidade)."""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Agent:
    """Modelo de um agente autônomo."""

    name: str
    role: str
    goal: str
    tools: List[Any] = field(default_factory=list)
    memory: Optional[Any] = None

    async def execute_task(self, task: "Task", context: Optional[Dict] = None) -> Any:
        """Executa uma tarefa.

        Args:
            task: Tarefa a ser executada
            context: Contexto adicional

        Returns:
            Resultado da execução da tarefa
        """
        logger.info(f"Agente '{self.name}' executando tarefa: {task.description}")

        # Por enquanto, retorna uma resposta simples
        return f"Tarefa '{task.description}' executada pelo agente '{self.name}'"


@dataclass
class Task:
    """Modelo de uma tarefa a ser executada."""

    description: str
    agent: Agent
    context: Dict = field(default_factory=dict)
    priority: int = 0
    dependencies: List["Task"] = field(default_factory=list)

    async def execute(self, context: Optional[Dict] = None) -> Any:
        """Executa a tarefa usando o agente designado.

        Args:
            context: Contexto adicional

        Returns:
            Resultado da execução da tarefa
        """
        logger.info(f"Executando tarefa: {self.description}")
        return await self.agent.execute_task(self, context or self.context)


class GeminiModel:
    """Modelo Gemini para geração de texto (compatibilidade)."""

    def __init__(self, config: Dict[str, Any]):
        """Inicializa o modelo Gemini.

        Args:
            config: Dicionário com configurações do modelo
        """
        self.config = config
        logger.info("Modelo Gemini inicializado (compatibilidade)")

    async def generate_content(self, prompt: str) -> Dict[str, Any]:
        """Gera conteúdo a partir de um prompt (simulação).

        Args:
            prompt: O prompt para geração de conteúdo

        Returns:
            Dicionário com o conteúdo gerado
        """
        return {
            "text": f"[Simulação] Resposta para: {prompt[:50]}...",
            "status": "success",
        }
