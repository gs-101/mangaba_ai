#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aplicação de Busca de Ebooks - Mangaba.AI

Esta aplicação permite buscar ebooks em diversas fontes online e retornar links para download.
A entrada é o nome do ebook desejado e a saída são links para download do ebook.
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Any, Dict, List
from urllib.parse import quote_plus

# Importações do framework Mangaba.AI
try:
    # Tenta importar do caminho principal
    from mangaba_ai.core.models import Agent, Task
    from mangaba_ai.main import MangabaAI
    from mangaba_ai.schemas.analysis import AnalysisResult
    from mangaba_ai.schemas.message import Message
except ImportError as e:
    # Se falhar, tenta importar do caminho alternativo (src)
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    # Importações simuladas para schemas que podem não existir no caminho alternativo
    from dataclasses import dataclass

    from src.mangaba_ai import MangabaAI
    from src.mangaba_ai.core.models import Agent, Task

    @dataclass
    class Message:
        content: str
        role: str = "user"
        sender: str = "user"
        timestamp: datetime = None

        def __post_init__(self):
            if self.timestamp is None:
                self.timestamp = datetime.now()

    @dataclass
    class AnalysisResult:
        content: str
        score: float = 0.0


# Importa o módulo de compatibilidade
# Usa o arquivo compat.py em vez do diretório compat/
import compat
from compat import get_model_implementation

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EbookSearchAgent(Agent):
    """
    Agente especializado em busca de ebooks em diversas fontes online.
    """

    def __init__(self):
        # Inicializa a classe pai com os parâmetros obrigatórios
        super().__init__(
            name="Ebook Search Agent",
            role="Especialista em busca de ebooks",
            goal="Encontrar ebooks em diversas fontes online",
        )
        self.version = "1.0.0"
        self.sources = [
            "https://libgen.is/search.php?req={query}",
            "https://b-ok.lat/s/{query}",
            "https://archive.org/search.php?query={query}",
            "https://www.pdfdrive.com/search?q={query}",
            "https://www.gutenberg.org/ebooks/search/?query={query}",
        ]

    async def search_ebook(self, query: str) -> List[Dict[str, str]]:
        """
        Busca o ebook nas fontes disponíveis.

        Args:
            query: Nome do ebook a ser buscado

        Returns:
            Lista de dicionários contendo informações sobre os ebooks encontrados
        """
        logger.info(f"Buscando ebook: {query}")

        # Em uma implementação real, aqui seria feita a busca nas fontes
        # usando bibliotecas como requests, aiohttp, ou selenium
        # Para este exemplo, vamos simular resultados

        encoded_query = quote_plus(query)
        results = []

        # Simula resultados de diferentes fontes
        for source in self.sources:
            source_url = source.format(query=encoded_query)

            # Simula 1-3 resultados por fonte
            for i in range(1, 4):
                if i == 1 or (i < 3 and hash(source + query) % 3 > 0):
                    result = {
                        "title": f"{query} - {'Edição ' + str(i) if i > 1 else 'Completo'}",
                        "author": f"Autor {'A' if i == 1 else 'B' if i == 2 else 'C'}",
                        "format": "PDF" if i % 2 == 0 else "EPUB",
                        "size": f"{(i * 3) + (hash(source) % 5):.1f} MB",
                        "source": source.split("/")[2],
                        "url": source_url,
                        "download_url": f"{source_url}&download=true&id={hash(source + query) % 1000}",
                    }
                    results.append(result)

        return results

    async def process_message(self, message: Message) -> Dict[str, Any]:
        """
        Processa a mensagem contendo o nome do ebook a ser buscado.

        Args:
            message: Objeto Message contendo o nome do ebook

        Returns:
            Dicionário com os resultados da busca
        """
        query = message.content.strip()
        results = await self.search_ebook(query)

        return {
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": message.timestamp,
            "processed": True,
        }


class EbookSearchApp:
    """
    Aplicação principal para busca de ebooks.
    """

    def __init__(self):
        self.ai = MangabaAI()
        self.agent = EbookSearchAgent()

    async def search(self, ebook_name: str) -> Dict[str, Any]:
        """
        Realiza a busca do ebook e retorna os resultados.

        Args:
            ebook_name: Nome do ebook a ser buscado

        Returns:
            Dicionário com os resultados da busca
        """
        message = Message(
            content=ebook_name,
            sender="user",
            timestamp=None,  # Será preenchido automaticamente
        )

        result = await self.agent.process_message(message)
        return result

    def format_results(self, results: Dict[str, Any]) -> str:
        """
        Formata os resultados da busca para exibição.

        Args:
            results: Dicionário com os resultados da busca

        Returns:
            String formatada com os resultados
        """
        output = f"Resultados da busca por '{results['query']}'\n"
        output += f"Encontrados {results['count']} resultados\n\n"

        for i, result in enumerate(results["results"], 1):
            output += f"{i}. {result['title']}\n"
            output += f"   Autor: {result['author']}\n"
            output += f"   Formato: {result['format']} | Tamanho: {result['size']}\n"
            output += f"   Fonte: {result['source']}\n"
            output += f"   Link: {result['download_url']}\n\n"

        return output


async def main():
    """
    Função principal para execução da aplicação.
    """
    app = EbookSearchApp()

    print("=== Aplicação de Busca de Ebooks - Mangaba.AI ===")
    print("Digite o nome do ebook que deseja buscar:")
    ebook_name = input("> ")

    results = await app.search(ebook_name)
    formatted_results = app.format_results(results)

    print("\n" + formatted_results)

    # Salva os resultados em um arquivo
    filename = f"resultados_busca_{ebook_name.replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(formatted_results)

    print(f"Resultados salvos no arquivo: {filename}")


if __name__ == "__main__":
    asyncio.run(main())
