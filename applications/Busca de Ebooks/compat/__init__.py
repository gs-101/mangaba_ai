"""Módulo de compatibilidade para a aplicação de Busca de Ebooks."""

# Importa diretamente do arquivo models.py no mesmo diretório
import logging
import os
import sys
from typing import Any, Dict

# Configuração de logging
logger = logging.getLogger(__name__)

# Adiciona o diretório atual ao path para importações relativas
sys.path.append(os.path.dirname(__file__))

# Importa as classes do arquivo models.py
from models import Agent, GeminiModel, Task


def get_model_implementation(model_name: str):
    """
    Retorna a implementação apropriada para o modelo especificado.

    Esta função tenta importar a implementação original do modelo.
    Se não estiver disponível, retorna a implementação de compatibilidade.

    Args:
        model_name: Nome do modelo a ser importado

    Returns:
        Classe de implementação do modelo
    """
    if model_name == "GeminiModel":
        try:
            # Tenta importar a implementação original
            from mangaba_ai.core.models import \
                GeminiModel as OriginalGeminiModel

            return OriginalGeminiModel
        except ImportError:
            # Se não encontrar, retorna a implementação de compatibilidade
            return GeminiModel

    # Para outros modelos, pode-se adicionar mais casos aqui

    # Se não encontrar nenhuma implementação, lança exceção
    raise ImportError(
        f"Não foi possível encontrar implementação para o modelo {model_name}"
    )
