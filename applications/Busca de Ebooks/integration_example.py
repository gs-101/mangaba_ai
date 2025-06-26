#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de integração da aplicação de Busca de Ebooks com o framework Mangaba.AI

Este exemplo demonstra como integrar a aplicação de busca de ebooks com outros
componentes do framework Mangaba.AI, como o sistema de memória e comunicação.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

# Importações do framework Mangaba.AI
try:
    # Tenta importar do caminho principal
    from mangaba_ai.core.models import Agent, Task
    from mangaba_ai.main import MangabaAI
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


# Importa o módulo de compatibilidade
from compat import get_model_implementation
# Importa a aplicação de busca de ebooks
from ebook_search import EbookSearchAgent, EbookSearchApp

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EbookAssistantAgent(Agent):
    """
    Agente assistente que utiliza o agente de busca de ebooks para fornecer
    recomendações e informações adicionais sobre os ebooks encontrados.
    """

    def __init__(self):
        # Inicializa a classe pai com os parâmetros obrigatórios
        super().__init__(
            name="Ebook Assistant Agent",
            role="Assistente de recomendação de ebooks",
            goal="Fornecer recomendações e informações sobre ebooks",
        )
        self.version = "1.0.0"
        self.ebook_search_agent = EbookSearchAgent()
        self.memory = {}

    async def process_message(self, message: Message) -> Dict[str, Any]:
        """
        Processa a mensagem do usuário, identifica a intenção e executa a ação apropriada.

        Args:
            message: Objeto Message contendo a mensagem do usuário

        Returns:
            Dicionário com a resposta processada
        """
        content = message.content.strip()

        # Verifica se é uma busca direta de ebook
        if content.startswith("buscar:") or content.startswith("busca:"):
            query = content.split(":", 1)[1].strip()
            return await self._handle_search(query)

        # Verifica se é um pedido de recomendação
        elif content.startswith("recomendar:") or content.startswith("recomendação:"):
            topic = content.split(":", 1)[1].strip()
            return await self._handle_recommendation(topic)

        # Verifica se é uma solicitação de detalhes sobre um ebook específico
        elif content.startswith("detalhes:") or content.startswith("detalhe:"):
            book_title = content.split(":", 1)[1].strip()
            return await self._handle_details(book_title)

        # Caso contrário, trata como uma busca normal
        else:
            return await self._handle_search(content)

    async def _handle_search(self, query: str) -> Dict[str, Any]:
        """
        Manipula uma solicitação de busca de ebook.

        Args:
            query: Nome do ebook a ser buscado

        Returns:
            Dicionário com os resultados da busca
        """
        # Cria uma mensagem para o agente de busca
        search_message = Message(
            content=query, sender="assistant", timestamp=datetime.now()
        )

        # Realiza a busca
        search_results = await self.ebook_search_agent.process_message(search_message)

        # Armazena os resultados na memória para uso futuro
        self.memory[query] = search_results

        # Adiciona informações adicionais à resposta
        response = {
            "type": "search_results",
            "query": query,
            "results": search_results["results"],
            "count": search_results["count"],
            "recommended_formats": self._get_recommended_formats(
                search_results["results"]
            ),
            "best_source": self._get_best_source(search_results["results"]),
            "timestamp": datetime.now().isoformat(),
            "processed": True,
        }

        return response

    async def _handle_recommendation(self, topic: str) -> Dict[str, Any]:
        """
        Manipula uma solicitação de recomendação de ebooks sobre um tópico.

        Args:
            topic: Tópico para recomendação

        Returns:
            Dicionário com as recomendações
        """
        # Em uma implementação real, aqui seria feita uma busca mais sofisticada
        # ou consultada uma base de conhecimento para recomendações

        # Para este exemplo, vamos apenas fazer uma busca normal e adicionar
        # informações de recomendação
        search_results = await self._handle_search(topic)

        # Filtra apenas os melhores resultados para recomendação
        if search_results["count"] > 0:
            top_results = sorted(
                search_results["results"],
                key=lambda x: len(x["title"]) + len(x["author"]),
            )[:3]
        else:
            top_results = []

        response = {
            "type": "recommendation",
            "topic": topic,
            "recommendations": top_results,
            "count": len(top_results),
            "reason": f"Ebooks mais relevantes sobre {topic}",
            "timestamp": datetime.now().isoformat(),
            "processed": True,
        }

        return response

    async def _handle_details(self, book_title: str) -> Dict[str, Any]:
        """
        Manipula uma solicitação de detalhes sobre um ebook específico.

        Args:
            book_title: Título do ebook

        Returns:
            Dicionário com os detalhes do ebook
        """
        # Verifica se já temos informações sobre este livro na memória
        for query, results in self.memory.items():
            for result in results.get("results", []):
                if book_title.lower() in result["title"].lower():
                    # Simula informações adicionais que seriam obtidas
                    # de uma fonte externa
                    details = {
                        "type": "book_details",
                        "title": result["title"],
                        "author": result["author"],
                        "format": result["format"],
                        "size": result["size"],
                        "source": result["source"],
                        "url": result["url"],
                        "download_url": result["download_url"],
                        "language": (
                            "Português" if "BR" in result["title"] else "Inglês"
                        ),
                        "year": 2020 - (hash(result["title"]) % 20),
                        "pages": 100 + (hash(result["title"]) % 300),
                        "description": f"Este é um ebook sobre {book_title}. Contém informações detalhadas e é uma excelente referência para estudantes e profissionais.",
                        "rating": round((hash(result["title"]) % 50) / 10 + 3, 1),
                        "timestamp": datetime.now().isoformat(),
                        "processed": True,
                    }
                    return details

        # Se não encontrou na memória, faz uma nova busca
        search_results = await self._handle_search(book_title)

        if search_results["count"] > 0:
            result = search_results["results"][0]
            details = {
                "type": "book_details",
                "title": result["title"],
                "author": result["author"],
                "format": result["format"],
                "size": result["size"],
                "source": result["source"],
                "url": result["url"],
                "download_url": result["download_url"],
                "language": "Português" if "BR" in result["title"] else "Inglês",
                "year": 2020 - (hash(result["title"]) % 20),
                "pages": 100 + (hash(result["title"]) % 300),
                "description": f"Este é um ebook sobre {book_title}. Contém informações detalhadas e é uma excelente referência para estudantes e profissionais.",
                "rating": round((hash(result["title"]) % 50) / 10 + 3, 1),
                "timestamp": datetime.now().isoformat(),
                "processed": True,
            }
            return details
        else:
            return {
                "type": "error",
                "message": f"Não foi possível encontrar detalhes sobre o ebook '{book_title}'",
                "timestamp": datetime.now().isoformat(),
                "processed": True,
            }

    def _get_recommended_formats(self, results: List[Dict[str, str]]) -> List[str]:
        """
        Determina os formatos recomendados com base nos resultados.

        Args:
            results: Lista de resultados da busca

        Returns:
            Lista de formatos recomendados
        """
        formats = {}
        for result in results:
            format_name = result.get("format", "")
            if format_name:
                formats[format_name] = formats.get(format_name, 0) + 1

        # Retorna os formatos ordenados por frequência
        return [f for f, _ in sorted(formats.items(), key=lambda x: x[1], reverse=True)]

    def _get_best_source(self, results: List[Dict[str, str]]) -> str:
        """
        Determina a melhor fonte com base nos resultados.

        Args:
            results: Lista de resultados da busca

        Returns:
            Nome da melhor fonte
        """
        sources = {}
        for result in results:
            source = result.get("source", "")
            if source:
                sources[source] = sources.get(source, 0) + 1

        # Retorna a fonte com mais resultados
        if sources:
            return max(sources.items(), key=lambda x: x[1])[0]
        return ""


class IntegratedEbookApp:
    """
    Aplicação integrada que utiliza o framework Mangaba.AI para busca de ebooks.
    """

    def __init__(self):
        self.ai = MangabaAI()
        self.assistant_agent = EbookAssistantAgent()

    async def process_query(self, query: str) -> Dict[str, Any]:
        """
        Processa uma consulta do usuário.

        Args:
            query: Consulta do usuário

        Returns:
            Dicionário com a resposta processada
        """
        message = Message(content=query, sender="user", timestamp=datetime.now())

        result = await self.assistant_agent.process_message(message)
        return result

    def format_response(self, response: Dict[str, Any]) -> str:
        """
        Formata a resposta para exibição ao usuário.

        Args:
            response: Dicionário com a resposta processada

        Returns:
            String formatada com a resposta
        """
        response_type = response.get("type", "")

        if response_type == "search_results":
            return self._format_search_results(response)
        elif response_type == "recommendation":
            return self._format_recommendations(response)
        elif response_type == "book_details":
            return self._format_book_details(response)
        elif response_type == "error":
            return f"Erro: {response.get('message', 'Ocorreu um erro desconhecido')}\n"
        else:
            return f"Resposta não reconhecida: {json.dumps(response, indent=2)}\n"

    def _format_search_results(self, response: Dict[str, Any]) -> str:
        """
        Formata os resultados da busca.

        Args:
            response: Dicionário com os resultados da busca

        Returns:
            String formatada com os resultados
        """
        output = f"Resultados da busca por '{response['query']}'\n"
        output += f"Encontrados {response['count']} resultados\n\n"

        if response["recommended_formats"]:
            output += (
                f"Formatos recomendados: {', '.join(response['recommended_formats'])}\n"
            )

        if response["best_source"]:
            output += f"Melhor fonte: {response['best_source']}\n\n"

        for i, result in enumerate(response["results"], 1):
            output += f"{i}. {result['title']}\n"
            output += f"   Autor: {result['author']}\n"
            output += f"   Formato: {result['format']} | Tamanho: {result['size']}\n"
            output += f"   Fonte: {result['source']}\n"
            output += f"   Link: {result['download_url']}\n\n"

        return output

    def _format_recommendations(self, response: Dict[str, Any]) -> str:
        """
        Formata as recomendações.

        Args:
            response: Dicionário com as recomendações

        Returns:
            String formatada com as recomendações
        """
        output = f"Recomendações para o tópico '{response['topic']}'\n"
        output += f"{response['reason']}\n\n"

        if response["count"] == 0:
            output += "Nenhuma recomendação encontrada.\n"
            return output

        for i, result in enumerate(response["recommendations"], 1):
            output += f"{i}. {result['title']}\n"
            output += f"   Autor: {result['author']}\n"
            output += f"   Formato: {result['format']} | Tamanho: {result['size']}\n"
            output += f"   Fonte: {result['source']}\n"
            output += f"   Link: {result['download_url']}\n\n"

        return output

    def _format_book_details(self, response: Dict[str, Any]) -> str:
        """
        Formata os detalhes de um ebook.

        Args:
            response: Dicionário com os detalhes do ebook

        Returns:
            String formatada com os detalhes
        """
        output = f"Detalhes do ebook: {response['title']}\n\n"
        output += f"Autor: {response['author']}\n"
        output += f"Ano: {response['year']}\n"
        output += f"Páginas: {response['pages']}\n"
        output += f"Idioma: {response['language']}\n"
        output += f"Formato: {response['format']}\n"
        output += f"Tamanho: {response['size']}\n"
        output += f"Avaliação: {response['rating']}/5.0\n\n"
        output += f"Descrição:\n{response['description']}\n\n"
        output += f"Fonte: {response['source']}\n"
        output += f"Link para download: {response['download_url']}\n"

        return output


async def main():
    """
    Função principal para execução da aplicação integrada.
    """
    app = IntegratedEbookApp()

    print("=== Aplicação Integrada de Busca de Ebooks - Mangaba.AI ===")
    print("Comandos disponíveis:")
    print("  - Digite o nome do ebook para busca simples")
    print("  - Digite 'buscar: [nome do ebook]' para busca específica")
    print("  - Digite 'recomendar: [tópico]' para obter recomendações")
    print("  - Digite 'detalhes: [nome do ebook]' para ver detalhes")
    print("  - Digite 'sair' para encerrar")
    print()

    while True:
        query = input("> ")

        if query.lower() == "sair":
            break

        result = await app.process_query(query)
        formatted_response = app.format_response(result)

        print("\n" + formatted_response)

    print("Aplicação encerrada.")


if __name__ == "__main__":
    asyncio.run(main())
