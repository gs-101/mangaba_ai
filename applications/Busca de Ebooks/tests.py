#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testes para a aplicação de Busca de Ebooks

Este arquivo contém testes unitários e de integração para a aplicação de busca de ebooks.
"""

import asyncio
import json
import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

# Importa os componentes da aplicação
from ebook_search import EbookSearchAgent, EbookSearchApp, Message
from integration_example import EbookAssistantAgent, IntegratedEbookApp


class TestEbookSearchAgent(unittest.TestCase):
    """
    Testes para o agente de busca de ebooks.
    """

    def setUp(self):
        self.agent = EbookSearchAgent()
        self.loop = asyncio.get_event_loop()

    def test_init(self):
        """
        Testa a inicialização do agente.
        """
        self.assertEqual(self.agent.name, "Ebook Search Agent")
        self.assertEqual(self.agent.version, "1.0.0")
        self.assertEqual(len(self.agent.sources), 5)

    def test_search_ebook(self):
        """
        Testa a função de busca de ebooks.
        """
        query = "Python Programming"
        results = self.loop.run_until_complete(self.agent.search_ebook(query))

        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)

        # Verifica se cada resultado tem os campos esperados
        for result in results:
            self.assertIn("title", result)
            self.assertIn("author", result)
            self.assertIn("format", result)
            self.assertIn("size", result)
            self.assertIn("source", result)
            self.assertIn("url", result)
            self.assertIn("download_url", result)

    def test_process_message(self):
        """
        Testa o processamento de mensagens.
        """
        message = Message(
            content="Python Programming", sender="user", timestamp=datetime.now()
        )

        result = self.loop.run_until_complete(self.agent.process_message(message))

        self.assertIn("query", result)
        self.assertIn("results", result)
        self.assertIn("count", result)
        self.assertIn("timestamp", result)
        self.assertIn("processed", result)

        self.assertEqual(result["query"], "Python Programming")
        self.assertTrue(result["processed"])
        self.assertTrue(len(result["results"]) > 0)


class TestEbookSearchApp(unittest.TestCase):
    """
    Testes para a aplicação de busca de ebooks.
    """

    def setUp(self):
        self.app = EbookSearchApp()
        self.loop = asyncio.get_event_loop()

    def test_search(self):
        """
        Testa a função de busca.
        """
        query = "Python Programming"
        results = self.loop.run_until_complete(self.app.search(query))

        self.assertIn("query", results)
        self.assertIn("results", results)
        self.assertIn("count", results)
        self.assertIn("timestamp", results)
        self.assertIn("processed", results)

        self.assertEqual(results["query"], query)
        self.assertTrue(results["processed"])

    def test_format_results(self):
        """
        Testa a formatação dos resultados.
        """
        query = "Python Programming"
        results = self.loop.run_until_complete(self.app.search(query))
        formatted = self.app.format_results(results)

        self.assertIsInstance(formatted, str)
        self.assertIn(query, formatted)
        self.assertIn("Encontrados", formatted)
        self.assertIn("Autor:", formatted)
        self.assertIn("Formato:", formatted)
        self.assertIn("Fonte:", formatted)
        self.assertIn("Link:", formatted)


class TestEbookAssistantAgent(unittest.TestCase):
    """
    Testes para o agente assistente de ebooks.
    """

    def setUp(self):
        self.agent = EbookAssistantAgent()
        self.loop = asyncio.get_event_loop()

    def test_init(self):
        """
        Testa a inicialização do agente.
        """
        self.assertEqual(self.agent.name, "Ebook Assistant Agent")
        self.assertEqual(self.agent.version, "1.0.0")
        self.assertIsInstance(self.agent.ebook_search_agent, EbookSearchAgent)
        self.assertEqual(self.agent.memory, {})

    def test_process_message_search(self):
        """
        Testa o processamento de mensagens de busca.
        """
        message = Message(
            content="buscar: Python Programming",
            sender="user",
            timestamp=datetime.now(),
        )

        result = self.loop.run_until_complete(self.agent.process_message(message))

        self.assertIn("type", result)
        self.assertEqual(result["type"], "search_results")
        self.assertIn("query", result)
        self.assertIn("results", result)
        self.assertIn("count", result)
        self.assertIn("recommended_formats", result)
        self.assertIn("best_source", result)

    def test_process_message_recommendation(self):
        """
        Testa o processamento de mensagens de recomendação.
        """
        message = Message(
            content="recomendar: Programação", sender="user", timestamp=datetime.now()
        )

        result = self.loop.run_until_complete(self.agent.process_message(message))

        self.assertIn("type", result)
        self.assertEqual(result["type"], "recommendation")
        self.assertIn("topic", result)
        self.assertIn("recommendations", result)
        self.assertIn("count", result)
        self.assertIn("reason", result)

    def test_process_message_details(self):
        """
        Testa o processamento de mensagens de detalhes.
        """
        # Primeiro faz uma busca para popular a memória
        search_message = Message(
            content="Python Programming", sender="user", timestamp=datetime.now()
        )
        self.loop.run_until_complete(self.agent.process_message(search_message))

        # Agora solicita detalhes
        message = Message(
            content="detalhes: Python Programming",
            sender="user",
            timestamp=datetime.now(),
        )

        result = self.loop.run_until_complete(self.agent.process_message(message))

        self.assertIn("type", result)
        self.assertEqual(result["type"], "book_details")
        self.assertIn("title", result)
        self.assertIn("author", result)
        self.assertIn("format", result)
        self.assertIn("size", result)
        self.assertIn("source", result)
        self.assertIn("url", result)
        self.assertIn("download_url", result)
        self.assertIn("language", result)
        self.assertIn("year", result)
        self.assertIn("pages", result)
        self.assertIn("description", result)
        self.assertIn("rating", result)


class TestIntegratedEbookApp(unittest.TestCase):
    """
    Testes para a aplicação integrada de ebooks.
    """

    def setUp(self):
        self.app = IntegratedEbookApp()
        self.loop = asyncio.get_event_loop()

    def test_process_query_search(self):
        """
        Testa o processamento de consultas de busca.
        """
        query = "Python Programming"
        result = self.loop.run_until_complete(self.app.process_query(query))

        self.assertIn("type", result)
        self.assertEqual(result["type"], "search_results")
        self.assertIn("query", result)
        self.assertIn("results", result)

    def test_process_query_recommendation(self):
        """
        Testa o processamento de consultas de recomendação.
        """
        query = "recomendar: Programação"
        result = self.loop.run_until_complete(self.app.process_query(query))

        self.assertIn("type", result)
        self.assertEqual(result["type"], "recommendation")
        self.assertIn("topic", result)
        self.assertIn("recommendations", result)

    def test_process_query_details(self):
        """
        Testa o processamento de consultas de detalhes.
        """
        # Primeiro faz uma busca para popular a memória
        search_query = "Python Programming"
        self.loop.run_until_complete(self.app.process_query(search_query))

        # Agora solicita detalhes
        query = "detalhes: Python Programming"
        result = self.loop.run_until_complete(self.app.process_query(query))

        self.assertIn("type", result)
        self.assertEqual(result["type"], "book_details")
        self.assertIn("title", result)
        self.assertIn("author", result)

    def test_format_response_search(self):
        """
        Testa a formatação de respostas de busca.
        """
        query = "Python Programming"
        result = self.loop.run_until_complete(self.app.process_query(query))
        formatted = self.app.format_response(result)

        self.assertIsInstance(formatted, str)
        self.assertIn(query, formatted)
        self.assertIn("Resultados da busca", formatted)
        self.assertIn("Encontrados", formatted)
        self.assertIn("Formatos recomendados", formatted)

    def test_format_response_recommendation(self):
        """
        Testa a formatação de respostas de recomendação.
        """
        query = "recomendar: Programação"
        result = self.loop.run_until_complete(self.app.process_query(query))
        formatted = self.app.format_response(result)

        self.assertIsInstance(formatted, str)
        self.assertIn("Programação", formatted)
        self.assertIn("Recomendações", formatted)

    def test_format_response_details(self):
        """
        Testa a formatação de respostas de detalhes.
        """
        # Primeiro faz uma busca para popular a memória
        search_query = "Python Programming"
        self.loop.run_until_complete(self.app.process_query(search_query))

        # Agora solicita detalhes
        query = "detalhes: Python Programming"
        result = self.loop.run_until_complete(self.app.process_query(query))
        formatted = self.app.format_response(result)

        self.assertIsInstance(formatted, str)
        self.assertIn("Detalhes do ebook", formatted)
        self.assertIn("Autor:", formatted)
        self.assertIn("Ano:", formatted)
        self.assertIn("Páginas:", formatted)
        self.assertIn("Idioma:", formatted)
        self.assertIn("Formato:", formatted)
        self.assertIn("Tamanho:", formatted)
        self.assertIn("Avaliação:", formatted)
        self.assertIn("Descrição:", formatted)


if __name__ == "__main__":
    unittest.main()
